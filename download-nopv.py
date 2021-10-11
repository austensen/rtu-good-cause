#!/usr/bin/env python

import requests
import random
import os
from time import sleep
from pathlib import Path
import pandas as pd

stmtDate = '20210115'
n_bbls = 1000
bbls_csv = 'pluto-extract.csv'

HERE = Path(__file__).parent
RAW_DIR = HERE / 'data-raw'
PDF_DIR = RAW_DIR / f'pdf-{stmtDate}'

PDF_DIR.mkdir(parents=True, exist_ok=True)


all_bbls = (
    pd.read_csv(RAW_DIR / bbls_csv, usecols=['bbl'], dtype=str)
    .bbl
    .unique()
    .tolist()
)

bbl_file = RAW_DIR / f'downloaded-bbls_{stmtDate}.csv'

if not bbl_file.exists():
    with open(bbl_file, 'w') as f:
        pass

downloaded_bbls = (
    pd.read_csv(bbl_file, names=['bbl'], dtype={'bbl': str})
    .bbl
    .tolist()
)

bbls_to_download = list(set(all_bbls) - set(downloaded_bbls))[0:n_bbls]

url_template = f'https://a836-edms.nyc.gov/dctm-rest/repositories/dofedmspts/StatementSearch?bbl=%s&stmtDate={stmtDate}&stmtType=NPV'

bbls_left = n_bbls
for bbl in bbls_to_download:
    os.system('clear')
    bbls_left -= 1
    print(bbls_left)

    sleep(random.uniform(0.5, 2.5))

    url = url_template % (bbl)
    r = requests.get(url)

    file = PDF_DIR / f'nopv_{bbl}.pdf'

    with open(file, 'wb') as f:
        f.write(r.content)

    with open(bbl_file, 'a') as f:
        f.write(bbl + '\n')
