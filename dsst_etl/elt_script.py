import argparse
import sys
from dsst_etl.extract import extract_from_csv
from dsst_etl.transform import clean_data
from dsst_etl.load import load_data
from dsst_etl.db import get_db_session

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='ETL script for processing CSV data')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')
    
    # Parse arguments
    args = parser.parse_args()

    try:
        # Initialize database session
        db_session = get_db_session()

        # Step 1: Extract data
        data = extract_from_csv(args.file_path)

        # Step 2: Transform data
        cleaned_data = clean_data(data)

        # Step 3: Load data
        load_data(cleaned_data, db_session)

        db_session.commit()
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        if 'db_session' in locals():
            db_session.rollback()
        sys.exit(1)
    finally:
        if 'db_session' in locals():
            db_session.close()

if __name__ == "__main__":
    main() 