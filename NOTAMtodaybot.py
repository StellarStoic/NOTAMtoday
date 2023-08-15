import os
import requests
import logging
from dotenv import load_dotenv
from today_notam_G import notams_by_day
import handling_files
import mapPlotting
import mapSnap
from mapPlotting import main as generate_map
from mapSnap import main as capture_image
import time
from datetime import datetime
from datetime import date

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

# Function to send a message to the Telegram group
def send_telegram_message(chat_id, api_key, message):
    base_url = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(base_url, data=payload)
    return response.json()

def send_telegram_image(chat_id, api_key, img_path, notam):
    """
    Sends an image to the specified Telegram chat with NOTAM details as the caption.
    """
    print(f"Trying to send image from path: {img_path}")  # Debug: print image path
    
    # Check if the image exists at the specified path
    if not os.path.exists(img_path):
        print(f"Image not found at path: {img_path}")
        return
    
    base_url = f"https://api.telegram.org/bot{api_key}/sendPhoto"
    
    # Format the NOTAM message to be used as a caption
    caption = f'''
NOTAM Number: {notam[0]}\n
{notam[1]}\n
{notam[2]}
{notam[5]}\n
{notam[6]}\n
{notam[7]}\n
{notam[8]}\n
Čas objave: {notam[9]}
KML File: {notam[10]}
'''
    
    with open(img_path, 'rb') as img_file:
        payload = {
            "chat_id": chat_id,
            "caption": caption
        }
        files = {
            "photo": img_file
        }
        response = requests.post(base_url, data=payload, files=files)
        print(f"Response from Telegram: {response.json()}")  # Debug: print API response
    return response.json()


# Functions to handle NOTAM IDs
def read_notam_ids(filename="/home/NOTAMtoday/NOTAMtoday/notamIDs.txt"):
    try:
        with open(filename, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

# def write_notam_ids(ids, filename="notamIDs.txt"):
#     with open(filename, "w") as file:
#         for notam_id in ids:
#             file.write(f"{notam_id}\n")

# Read existing NOTAM IDs from file
existing_ids = read_notam_ids()

# Extract all NOTAMs, then filter to get new NOTAMs based on their IDs (notam_number)
all_notams = [notam for date in notams_by_day for notam in notams_by_day[date]]
new_notams = [notam for notam in all_notams if notam[0] not in existing_ids]

# Processing new NOTAMs
for notam in new_notams:
    notam_id = notam[0]
    
    # Download KML files
    handling_files.handling_files()


    # Generate the maps (HTML files)
    generate_map()


    # Capture images from the generated maps
    capture_image()
    
    # # Capture the map image using Selenium
    # img_path = capture_image()

    # Format the NOTAM message
    message = f'''
NOTAM Number: {notam[0]}\n
{notam[1]}\n
{notam[2]}
{notam[5]}\n
{notam[6]}\n
{notam[7]}\n
{notam[8]}\n
Čas objave: {notam[9]}
KML File: {notam[10]}
'''

    # Send the associated image for the NOTAM
    img_name = notam_id.replace('/', '-') + '.png'
    img_path = os.path.join('/home/NOTAMtoday/NOTAMtoday/SNAPs', img_name)
    # Check if the image exists
    if os.path.exists(img_path):
        # Send the image with NOTAM details as the caption to the Telegram chat
        send_telegram_image(GROUP_CHAT_ID, API_KEY, img_path, notam)
    else:
        # If the image doesn't exist, just send the NOTAM message
        send_telegram_message(GROUP_CHAT_ID, API_KEY, message)
        
    existing_ids.add(notam[0])

# # Write the updated NOTAM IDs back to the file
# write_notam_ids(existing_ids)

def run_log():
    today = date.today()
    logging.info("Running bot...")
    try:
        notams = notams_by_day[today]
        logging.info(f"Retrieved {len(notams)} NOTAMs.")
    except Exception as e:
        logging.error(f"Error retrieving NOTAMs: {e}")
        raise

    for notam in notams:
        notam_id = notam['id']
        notam_message = notam['message']

        try:
            send_telegram_message(CHAT_ID, TELEGRAM_API_KEY, notam_message)
            logging.info(f"Sent message for NOTAM: {notam_id}")
        except Exception as e:
            logging.error(f"Error sending message for NOTAM {notam_id}: {e}")
            raise

        image_path = os.path.join("/home/NOTAMtoday/NOTAMtoday/SNAPs", f"{notam_id}.png")
        if os.path.exists(image_path):
            try:
                send_telegram_image(CHAT_ID, TELEGRAM_API_KEY, image_path, notam_message)
                logging.info(f"Sent image for NOTAM: {notam_id}")
            except Exception as e:
                logging.error(f"Error sending image for NOTAM {notam_id}: {e}")
                raise

# Configure logging
logging.basicConfig(filename="/home/NOTAMtoday/NOTAMtoday/bot_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

'''
    Use cron for timer
    crontab -e
    30 5 * * * /path/to/python3 /path/to/your/script.py
'''