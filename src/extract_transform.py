import pandas as pd
import re

def extract_data(input_file):
    """
    Extracts raw data from a CSV file.
    
    Args:
        input_file (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Extracted raw data.
    """
    try:
        df = pd.read_csv(input_file)
        print(f"✅ Data extracted from '{input_file}' successfully.")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None
def transform_data(df):
    """
    Cleans and transforms the extracted data.

    Args:
        df (pd.DataFrame): Raw data.

    Returns:
        pd.DataFrame: Cleaned and transformed data.
    """
    if df is None:
        return None

    # Create a copy to avoid modifying the original data
    df = df.copy()

    # Standardize column names (removes spaces and converts to lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Remove duplicates if 'id' column exists
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'], keep='first')

    # Handle missing values properly
    df['text'] = df.get('text', pd.Series(dtype=str)).fillna('no text')
    df['youtube_links'] = df.get('youtube_links', pd.Series(dtype=str)).fillna('no link')
    df['channel'] = df.get('channel', pd.Series(dtype=str)).fillna('Unknown')
    df['image_path'] = df.get('image_path', pd.Series(dtype=str)).fillna('')
    
    # Ensure 'contains_emoji' column exists and replace missing values with "no emoji"
    df['contains_emoji'] = df.get('contains_emoji', pd.Series(dtype=str)).fillna('no emoji')

    # Improved YouTube link regex
    youtube_pattern = r"(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w\-]+"
    df['has_youtube_link'] = df['youtube_links'].apply(lambda x: bool(re.search(youtube_pattern, str(x))))

    # Convert 'date' column to datetime safely
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    print("✅ Data transformation complete.")
    return df
def save_cleaned_data(df, output_file):
    """
    Saves the cleaned data to a new CSV file.
    
    Args:
        df (pd.DataFrame): Cleaned data.
        output_file (str): Path to save the cleaned CSV file.
    """
    try:
        df.to_csv(output_file, index=False)
        print(f"✅ Cleaned data saved to '{output_file}'.")
    except Exception as e:
        print(f"❌ Error saving cleaned data: {e}")
