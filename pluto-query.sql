-- set of BBLs to start with
select 
	bbl, address, zipcode, unitsres, numfloors, latitude, longitude
from pluto_20v8
where 
	zipcode in ('11385', '11378', '11379')
	and unitsres between 1 and 	5;

-- get the most recent respondent (owner?) address for each bbl in our set, 
-- geocode these to bbl and compare against pluto bbl
-- could do multiple (eg. all for last x years), might be overkill
select distinct on (bbl)
	bbl,
	(respondenthousenumber || ' ' || 
	 respondentstreet || 
	 coalesce(', ' || respondentcity, '') || 
	 coalesce(' ' || respondentzip, '')
	) as owner_addy
from ecb_violations
where 
	respondenthousenumber is not null
	and respondentstreet is not null
	and bbl ~* '^[1-5](?!0{5})\d{5}(?!0{4})\d{4}$'
order by bbl, issuedate desc
limit 100;

-- do the same as above for oath_hearings