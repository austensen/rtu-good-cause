#!/usr/bin/env python

import pandas as pd
import subprocess
import re
from pathlib import Path

stmtDate = '20210115'

HERE = Path(__file__).parent
RAW_DIR = HERE / 'data-raw'
PDF_DIR = RAW_DIR / f'pdf-{stmtDate}'
TXT_DIR = RAW_DIR / f'txt-{stmtDate}'
CLEAN_DIR = HERE / 'data-clean'
CLEAN_FILE = CLEAN_DIR / f'dof-nopv-{stmtDate}.csv'

TXT_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_DIR.mkdir(parents=True, exist_ok=True)


def pdfs_to_txts(pdf_dir, txt_dir):
    for pdf_file in pdf_dir.glob('*.pdf'):
        txt_file = txt_dir.joinpath(pdf_file.stem + '.txt')
        subprocess.call(['pdftotext', '-table', '-enc',
                        'UTF-8', pdf_file, txt_file])


def txts_to_csv(txt_dir, csv_file):
    fields = ['bbl', 'star']
    with open(csv_file, 'w') as f:
        f.write(','.join(fields) + '\n')
    for txt_file in txt_dir.glob('*.txt'):
        txt_file_to_csv_line(txt_file, csv_file)


def extract_matches(pattern, text, strip_commas=False):
    pattern = re.compile(pattern, re.MULTILINE)
    match = re.search(pattern, text)
    vals = []
    for i in range(pattern.groups):
        val = match.group(i+1).strip() if match else ''
        if strip_commas:
            val = val.replace(',', '')
        vals.append(val)
    if pattern.groups == 1:
        return vals[0]
    else:
        return vals


def txt_file_to_csv_line(txt_file, csv_file):
    with open(txt_file, 'r') as f:
        nopv_text = f.read()

    bbl = re.search(r'(\d+)\.txt$', str(txt_file)).group(1)

    exemptions = extract_matches(
        r'^\s*Your property tax exemptions:(.*?)$', nopv_text)

    if exemptions:
        match = re.search(r'STAR', exemptions)
        star = 'true' if match else 'false'
    else:
        star = ''

    with open(csv_file, 'a') as f:
        fields = [bbl, star]
        csv_line = '"' + '","'.join(fields) + '"\n'
        f.write(csv_line)


def main():
    pdfs_to_txts(PDF_DIR, TXT_DIR)
    txts_to_csv(TXT_DIR, CLEAN_FILE)


if __name__ == '__main__':
    main()
