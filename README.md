# get_ipids.py
## 'IC': Institute or Center abbreviation
   - Values are defined in the list 'ICs', which includes abbreviations for various NIH institutes and centers.

## 'YEAR': Year of the data
   - Each 'IC' and year combination is used to make a request to the NIH website to retrieve data.

## 'IPID': Intramural Program Integrated Data (unique identifier)
   - Values are obtained by scraping the NIH website using a POST request with specific parameters ('ic' and 'searchyear').
   - Regular expression (re.findall) is used to extract IPID numbers from the response text.
   - For each unique IPID, a row with 'IC', 'YEAR', and 'IPID' is added to the CSV, avoiding duplicates.


# ##########


# get_pmids.py
## 'PI': Principal Investigator(s)
   - The 'headings' and 'showname' HTML elements are searched for relevant labels to extract the names of Principal Investigators.

## 'PMID': PubMed ID
   - A regular expression is used to find patterns matching PubMed IDs in the HTML content.

## 'DOI': Digital Object Identifier
   - A regular expression is used to find patterns matching DOI values in the HTML content.

## 'PROJECT': Project associated with the report
   - Extracted from the 'contentlabel' HTML element within the reports.


# ##########


# get_pmids_articles.py

## 'pmids_articles.csv': Filtered CSV containing articles that meet specific criteria.
  - Removes publications with types: ['Review', 'Comment', 'Editorial', 'Published Erratum'].
  - Only includes publications identified as articles based on PubMed API data.


# ##########


# data_conversion.py

##   Fetches information for PubMed articles, specifically titles and journal names:

   - 'pmid': PubMed ID (unique identifier for a publication in PubMed).
   - 'title': Title of the PubMed article.
   - 'journal': Name of the journal in which the article was published.
   - Errors during the fetch process are logged, and corresponding entries in the CSV have empty strings for title and journal.

## Data Retrieval Process:
   - The program reads an existing CSV file ('pmids_articles.csv') containing PubMed IDs ('PMID').
   - For each unique PubMed ID, it uses the Metapub library to fetch additional details, including the article title and journal.
   - If an error occurs during the fetch process, the program records the PubMed ID and assigns empty strings to title and journal.

# ##########



