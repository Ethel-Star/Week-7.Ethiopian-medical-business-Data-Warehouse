import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error: Unable to connect to the database: {e}")
        return None

# Create detection results table if not exists
def create_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS detections (
            id SERIAL PRIMARY KEY,
            image_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            confidence DECIMAL,
            bbox_x DECIMAL,
            bbox_y DECIMAL,
            bbox_w DECIMAL,
            bbox_h DECIMAL
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
def store_detection_results(image_file, detections):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        for detection in detections:
            class_name = detection['class_name']
            confidence = detection['confidence']
            bbox = detection['bbox']
            query = '''
            INSERT INTO detections (image_name, class_name, confidence, bbox_x, bbox_y, bbox_w, bbox_h)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''
            cursor.execute(query, (
                image_file,
                class_name,
                confidence,
                bbox[0],
                bbox[1],
                bbox[2],
                bbox[3]
            ))
        conn.commit()
        cursor.close()
        conn.close()
