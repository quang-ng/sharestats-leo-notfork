import psycopg2
import os
from dotenv import load_dotenv

# .env variables
load_dotenv()

# Database parameters from .env
db_params = {
    "dbname": os.getenv("POSTGRES_NAME"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}
# Path to SQL file
sql_file = r"sql-create/openalex_create_db.sql"

# Read the SQL commands from the file
with open(sql_file, "r") as file:
    sql_commands = file.read()

try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute(sql_commands)

    conn.commit()
    print("SQL commands executed successfully.")
except psycopg2.Error as e:
    conn.rollback()
    print("Error executing SQL commands:", e)
finally:
    cursor.close()
    conn.close()
