import os
import logging
import csv
from telethon import TelegramClient
from dotenv import load_dotenv
import re
import asyncio

# Load environment variables from a .env file
load_dotenv()
TG_API_ID = os.getenv("TG_API_ID")
TG_API_HASH = os.getenv("TG_API_HASH")
PHONE = os.getenv("PHONE")
SCRAPE_LIMIT = int(os.getenv("SCRAPE_LIMIT", 100))  # Default limit set to 100 messages

# Set up logging to monitor the scraping process
log_dir = os.path.join(os.getcwd(), "log")  # Log folder in the current working directory
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "scraper.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set up data storage folder in the current working directory
data_dir = os.path.join(os.getcwd(), "data")
os.makedirs(data_dir, exist_ok=True)

# Initialize the Telegram Client
client = TelegramClient("session", TG_API_ID, TG_API_HASH)

# Function to extract YouTube links from message text
def extract_youtube_links(text):
    youtube_pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/[\w\-?=]+"  # Regex pattern for YouTube links
    return re.findall(youtube_pattern, text)

# Function to scrape messages, download images, and extract YouTube links
async def scrape_channel(channel, writer):
    logging.info(f"Scraping started for: {channel}")
    
    try:
        # Start the client with the phone number
        await client.start(PHONE)
        
        # Iterate over messages in the channel
        async for message in client.iter_messages(channel, limit=SCRAPE_LIMIT):
            youtube_links = extract_youtube_links(message.text) if message.text else []
            image_path = f"{message.id}.jpg" if message.photo else "No image"
            message_date = message.date.strftime("%Y-%m-%d %H:%M:%S")  # Format the date to a readable string
            
            # Write message data to CSV file
            writer.writerow([
                message.id, 
                message.text, 
                youtube_links, 
                channel, 
                message_date,  # Add the formatted date
                image_path
            ])
            
            # If message has an image, download it
            if message.photo:
                image_path = os.path.join(data_dir, f"{message.id}.jpg")
                if not os.path.exists(image_path):
                    await message.download_media(image_path)
                    logging.info(f"Downloaded image: {image_path}")
        
        logging.info(f"Scraping completed for: {channel}")
    except Exception as e:
        logging.error(f"Error scraping {channel}: {e}")

# List of channels to scrape
channels = [
    "DoctorsET",
    "lobelia4cosmetics",
    "yetenaweg",
    "EAHCI"
]

# Main function to scrape data from all channels and save to CSV
async def main():
    # Open CSV file for writing all scraped data
    file_path = os.path.join(data_dir, "all_channels_data.csv")
    
    with open(file_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "text", "youtube_links", "channel", "date", "image_path"])  # Write header row
        
        # Start scraping each channel concurrently
        await client.start(PHONE)
        tasks = [scrape_channel(channel, writer) for channel in channels]
        await asyncio.gather(*tasks)

# Run the main function to start scraping
with client:
    client.loop.run_until_complete(main())
