import os
import logging
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Telegram API credentials
TG_API_ID = os.getenv('TG_API_ID')
TG_API_HASH = os.getenv('TG_API_HASH')
PHONE = os.getenv('phone')
SCRAPE_LIMIT = int(os.getenv('SCRAPE_LIMIT'))

# Folder to save images
SAVE_FOLDER = "data/images"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# Initialize Telegram Client
client = TelegramClient('session_name', TG_API_ID, TG_API_HASH)

async def download_images():
    try:
        # Connect to Telegram
        await client.start(phone=PHONE)
        
        # Get the channel (replace with the actual channel link)
        channel = await client.get_entity('https://t.me/lobelia4cosmetics')
        
        # Download images from the channel
        messages = await client.get_messages(channel, limit=SCRAPE_LIMIT, filter=InputMessagesFilterPhotos)
        
        logger.info(f"Found {len(messages)} photos. Downloading...")
        
        for i, message in enumerate(messages):
            # Check if the message contains a photo
            if message.photo:
                # Download the photo
                file_path = os.path.join(SAVE_FOLDER, f"image_{i+1}.jpg")
                await message.download_media(file_path)
                logger.info(f"Downloaded: {file_path}")
                
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        await client.disconnect()

# Run the download function asynchronously
if __name__ == '__main__':
    asyncio.run(download_images())
