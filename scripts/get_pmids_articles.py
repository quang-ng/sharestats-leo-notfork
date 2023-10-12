from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
load_dotenv()  # Import NCBI_API_KEY before loading PubMedFetcher
from metapub.pubmedfetcher import PubMedFetcher

'''
PubMed has a list of types for each publication.
This code fetches the types of each publication in pmids.csv
and generates pmids_articles.csv, removing the types:
['Review', 'Comment', 'Editorial', 'Published Erratum']

one_hot_types.csv is also produced
each column is an existing type
each row is a publication
the cells are bools indicating which type is a pub
'''

DATA_PATH = Path('../data')
PMID_FILE_PATH = DATA_PATH / 'pmids.csv'
ONE_HOT_FILE_PATH = DATA_PATH / 'one_hot_types.csv'
FILTERED_PMID_FILE_PATH = DATA_PATH / 'pmids_articles.csv'
ERROR_FILE_PATH = DATA_PATH / 'get_pmids_articles_error.txt'

df = pd.read_csv(PMID_FILE_PATH)
pubtypes_lst_of_dict = []
pmids = []
for i, pmid in enumerate(df['PMID'].astype('Int64').unique()):
    print(f"{i+1} of {len(df['PMID'].unique())} PMIDS")
    try:
        pma = PubMedFetcher().article_by_pmid(pmid)
        row = pma.publication_types
        pubtypes_lst_of_dict.append(row)
        pmids.append(pmid)
        assert len(pubtypes_lst_of_dict) == len(pmids)
    except Exception as e:
        with open(ERROR_FILE_PATH, 'a') as f:
            f.write(f'{pmid}: {e}\n')
        continue

all_values = set()
for d in pubtypes_lst_of_dict:
    all_values.update(d.values())

data = []
for d in pubtypes_lst_of_dict:
    row_data = {value: value in d.values() for value in all_values}
    data.append(row_data)

one_hot_df = pd.DataFrame(data)
one_hot_df = one_hot_df.fillna(False)
one_hot_df['PMID'] = pmids
one_hot_df.to_csv(ONE_HOT_FILE_PATH, index=False)

remove_cols = ['Review', 'Comment', 'Editorial', 'Published Erratum']
article_pmid = one_hot_df[~one_hot_df[remove_cols].any(axis=1)]['PMID']
opendata_articles = df[df['PMID'].isin(article_pmid)]
opendata_articles.to_csv(FILTERED_PMID_FILE_PATH, index=False)
