import os
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "Ethio_Medical_Database"  # Change as needed

def create_and_connect_db():
    """
    Creates and connects to the PostgreSQL database.
    
    Returns:
        tuple: (connection, cursor)
    """
    try:
        # Connect to default database
        temp_conn = psycopg2.connect(
            dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        temp_conn.autocommit = True
        temp_cursor = temp_conn.cursor()

        # Check if database exists
        temp_cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = temp_cursor.fetchone()

        if not exists:
            temp_cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✅ Database '{DB_NAME}' created successfully.")
        else:
            print(f"ℹ️ Database '{DB_NAME}' already exists. Connecting...")

        temp_cursor.close()
        temp_conn.close()

        # Connect to the actual database
        connection = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = connection.cursor()
        print(f"✅ Connected to database '{DB_NAME}'.")
        return connection, cursor

    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")
        return None, None

def create_table():
    """
    Creates a table for storing the medical data.
    """
    connection, cursor = create_and_connect_db()
    if not connection:
        return
    
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS medical_database (
            id SERIAL PRIMARY KEY,
            text TEXT,
            youtube_links TEXT,
            channel TEXT,
            image_path TEXT,
            contains_emoji TEXT,
            has_youtube_link TEXT,
            date TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Table 'medical_database' created successfully.")
    except psycopg2.Error as e:
        print(f"❌ Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

def load_to_postgresql(csv_file, table_name="medical_database"):
    """
    Loads cleaned data from a CSV file into PostgreSQL.
    
    Args:
        csv_file (str): Path to the cleaned CSV file.
        table_name (str): Name of the table to insert data into.
    """
    try:
        # Read CSV
        df = pd.read_csv(csv_file)

        # Ensure 'date' is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Create DB connection
        db_connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_connection_string)

        # Insert data
        df.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"✅ Data successfully loaded into '{table_name}' in '{DB_NAME}'.")

    except Exception as e:
        print(f"❌ Error loading data into PostgreSQL: {e}")
