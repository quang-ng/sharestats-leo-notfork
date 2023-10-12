import re
import os
import sys
import logging
import requests
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# .env variables
load_dotenv()
headers = {'user-agent': os.getenv('USER_AGENT')}
'''
Needs ipids.csv, run get_ipids.py to generate
Scrapes reports in search of PubMedIDs
Saves or appends to single csv: IPID, PI, PMID, DOI, PROJECT
'''
DATA_PATH = Path('../data')
IPID_FILE_PATH = DATA_PATH / 'ipids.csv'
PMID_FILE_PATH = DATA_PATH / 'pmids.csv'
ERROR_LOG_FILE_PATH = DATA_PATH / 'get_pmids_error.txt'

logging.basicConfig(
    filename=ERROR_LOG_FILE_PATH,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Check if we already have a pmid file
# Otherwise, create one with the headers
if PMID_FILE_PATH.exists():
    pmid_df = pd.read_csv(PMID_FILE_PATH)
else:
    pmid_df = pd.DataFrame(columns=['IPID', 'PI', 'PMID', 'DOI', 'PROJECT'])
    pmid_df.to_csv(PMID_FILE_PATH, index=False)
# Check if we have ipids.csv, necessary in this script
if not IPID_FILE_PATH.exists():
    print(f"{IPID_FILE_PATH} does not exist, run get_ipids.py to generate")
    sys.exit(1)
ipid_df = pd.read_csv(IPID_FILE_PATH)

URL_ROOT = "https://intramural.nih.gov/search/searchview.taf?ipid="
for (IC, year) in ipid_df[['IC', 'YEAR']].drop_duplicates().itertuples(index=False):
    print(f'Parsing {IC} {year}')
    ic_year_ipids = ipid_df[(ipid_df['IC'] == IC) & (ipid_df['YEAR'] == year)]
    ipids = list(ic_year_ipids['IPID'])
    # don't query ipids we already have:
    ipids = [ipid for ipid in ipids if ipid not in pmid_df['IPID'].tolist()]

    # loop over intramural project IDs
    for i, ipid in enumerate(ipids):
        print(f'IPID {i+1} of {len(ipids)}: {ipid}')
        # report url
        url = f'{URL_ROOT}{ipid}'

        try:
            # get the html for the report
            page = requests.get(url, headers=headers)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error - IPID {ipid}: {e}\n")
            continue

        # soup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # report code / PROJECT
        contentlabel_div = soup.find('div', class_='contentlabel')
        project = contentlabel_div.text.replace('  ', ' ')
        project = project.split()[1]

        # PIs
        headings = soup.findAll('span', class_='headings')
        PIs = []
        valid_listings_for_pis = ['Lead Investigator', 'Principal Investigator', 'Core Lead',
                                  'Lead Investigators', 'Principal Investigators', 'Core Leads']
        for head in headings:
            label = head.text.strip()
            label = re.sub(r'[^\w\s]', '', label)
            if label in valid_listings_for_pis:
                names = head.parent.parent.findNext('tr').findChildren('td', attrs={'class': 'showname'})
                [PIs.append(nn.text.replace('  ', ' ').split('\n')[0]) for nn in names]
        # If no PIs, log and check later for cause
        if not PIs:
            logging.error(f"No PIS found for - IPID {ipid}\n")
            continue

        # PubMedIDs and DOIs
        '''
        not all publications in the reports have a PubMedID
        and not all have a DOI (even if it exists)
        '''
        pmids = soup.findAll('div', attrs={'class': 'publisting'})
        pmid_pattern = r'pubmed/(\d+)'
        pmid_lst = [
            re.search(pmid_pattern, str(element)).group(1)
            if re.search(pmid_pattern, str(element))
            else ''
            for element in pmids
        ]
        dois = soup.findAll('div', attrs={'class': 'publisting'})
        doi_pattern = r'(10[.]\d{4,}[^\s"/<>]*/[^\s"<>]+)'  # from regex101, tested on 2019-2022 data
        doi_lst = [
            re.search(doi_pattern, element.text).group(1)
            if re.search(doi_pattern, element.text)
            else ''
            for element in dois
        ]

        current_ipid_rows = {
            'IPID': [],
            'PI': [],
            'PMID': [],
            'DOI': [],
            'PROJECT': []
        }

        for pi in PIs:
            for (pmid, doi) in zip(pmid_lst, doi_lst):
                if (pmid, doi) == ('', ''):
                    continue
                if pmid:
                    pmid = int(pmid)
                current_ipid_rows['IPID'].append(int(ipid))
                current_ipid_rows['PI'].append(pi)
                current_ipid_rows['PMID'].append(pmid)
                current_ipid_rows['DOI'].append(doi)
                current_ipid_rows['PROJECT'].append(project)

        current_ipid_df = pd.DataFrame(current_ipid_rows)
        pmid_df = pd.concat([pmid_df, current_ipid_df], ignore_index=True)
    # Save after all reports for given IC, YEAR
    pmid_df.drop_duplicates(inplace=True)
    pmid_df.to_csv(PMID_FILE_PATH, index=False)
