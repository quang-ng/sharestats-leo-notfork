# DSST ETL Package

This package provides ETL (Extract, Load, Transform) functionality for data processing with PostgreSQL database integration.

## Features

- SQLAlchemy ORM integration
- Pydantic data validation
- PostgreSQL database support
- Environment-based configuration
- Raw and processed data handling
- JSON data type support
- Automated timestamp tracking
- Relationship management between raw and processed data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dsst_etl.git
   cd dsst_etl
   ```

2. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your database credentials and other settings
   ```

## Project Structure
```
dsst_etl/
├── dsst_etl/
│   ├── __init__.py
│   ├── config.py      # Configuration management
│   ├── db.py          # Database connection and models
│   ├── extract.py     # Data extraction logic
│   └── load.py        # Data loading operations
├── dockers/
│   └── docker-compose.yml
├── tests/             # Directory for test cases
├── .env.example       # Example environment configuration
├── .python-version    # Python version specification
├── pyproject.toml     # Project metadata and dependencies
└── README.md          # Project documentation
```

## Usage

### First, start the database in Docker

```bash
cd dockers
docker compose up
```

### Then, run the ETL script
To run the ETL script, use the following command:
```bash
python dsst_etl/elt_script.py --file_path path/to/your/file.csv
```

