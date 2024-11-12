# Share Stats

## get_ipids.py

### 'IC': Institute or Center abbreviation

- Values are defined in the list 'ICs', which includes abbreviations for various NIH institutes and centers.

### 'YEAR': Year of the data

- Each 'IC' and year combination is used to make a request to the NIH website to retrieve data.

### 'IPID': Intramural Program Integrated Data (unique identifier)

- Values are obtained by scraping the NIH website using a POST request with specific parameters ('ic' and 'searchyear').

  - Regular expression (re.findall) is used to extract IPID numbers from the response text.
  - For each unique IPID, a row with 'IC', 'YEAR', and 'IPID' is added to the CSV, avoiding duplicates.

## get_pmids.py

### 'PI': Principal Investigator(s)

- The 'headings' and 'showname' HTML elements are searched for relevant labels to extract the names of Principal Investigators.

### 'PMID': PubMed ID

- A regular expression is used to find patterns matching PubMed IDs in the HTML content.

### 'DOI': Digital Object Identifier

- A regular expression is used to find patterns matching DOI values in the HTML content.

### 'PROJECT': Project associated with the report

- Extracted from the 'contentlabel' HTML element within the reports.

## get_pmids_articles.py

### 'pmids_articles.csv': Filtered CSV containing articles that meet specific criteria

- Removes publications with types: ['Review', 'Comment', 'Editorial', 'Published Erratum'].
- Only includes publications identified as articles based on PubMed API data.

## data_conversion.py

### Fetches information for PubMed articles, specifically titles and journal names

- 'pmid': PubMed ID (unique identifier for a publication in PubMed).
- 'title': Title of the PubMed article.
- 'journal': Name of the journal in which the article was published.
- Errors during the fetch process are logged, and corresponding entries in the CSV have empty strings for title and journal.

### Data Retrieval Process

- The program reads an existing CSV file ('pmids_articles.csv') containing PubMed IDs ('PMID').
- For each unique PubMed ID, it uses the Metapub library to fetch additional details, including the article title and journal.
- If an error occurs during the fetch process, the program records the PubMed ID and assigns empty strings to title and journal.

## R Script Dependencies

Currently using `renv` for package management.

### Packages

#### Binary installations

- Pandoc. [Installation Instructions](https://pandoc.org/installing.html). Required for [rtransparent](https://github.com/serghiou/rtransparent) packages's vignettes.
- pdftotext. Install [Poppler](https://poppler.freedesktop.org/). For macOS use Homebrew: `brew install poppler`. See the OS Dependcies section on the [PYPI pdftotext module](https://pypi.org/project/pdftotext/) for other OS installations of Poppler.

#### R Packages

##### CRAN

- devtools
  - Needed for installing packaged hosted on GitHub.
_ renv
  - Needed for loading R project environment so users do not need to manually install packages. *TODO: Add in section on using renv to load dependencies.*

##### GitHub

- [Open Data Detection in Publications (ODDPub)](https://github.com/quest-bih/oddpub). Required for [rtransparent](https://github.com/serghiou/rtransparent). *Must us v6.0!* If installing manually run `devtools::install_github("quest-bih/oddpub@v6")`. Updated ODDPub uses different parameters in latest version than is
- [CrossRef Minter (crminer)](https://github.com/cran/crminer). Required for [metareadr](https://github.com/serghiou/metareadr)
_ [Meta Reader (metareadr)](https://github.com/serghiou/metareadr). Required for [rtransparent](https://github.com/serghiou/rtransparent).

## Python Dependencies

### Pip-tools

In order to separate the develepment dependencies and the required depedencies, this project uses pip-tools. For running the scripts run `pip install -r requirements`. To develop on the codebase with tools that help with formatting, typing, and linting run `pip install -r dev.txt`.

### psycopg2

The PYPI package `psycopg2-binary` is used in `requirements.in` for compatiblity with pip-tools. This version of psycopg2 is not for production uses of POSTGRESQL. See [psycopg2-binary docs](https://pypi.org/project/psycopg2-binary/) for an explanation.

### DSST-ETL

Some useful commands:

```
#install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# install all dependencies
uv sync --all-extras
# activate the virtual environment
source .venv/bin/activate

# copy the mock environment variables to the file used by docker compose and the package
cp .mockenv .env

# start the postgres server
docker compose -f .docker/postgres-compose.yaml up -d

# stop the postgres server and remove the volume with -v
docker compose -f .docker/postgres-compose.yaml down -v

# install the pre-commit hooks
pre-commit install

# run the pre-commit hooks on all files
pre-commit run -all

# run the tests
pytest
```
