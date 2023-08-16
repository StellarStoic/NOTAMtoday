'''
This bot script sends notam images separately from the notam message.
I'm keeping it just in case, if the main NOTAMcheckbot script where
we add notam message in the image caption stops working
if KML files are not included in the notam message for some reason
'''


import os
import requests
from dotenv import load_dotenv
from today_notam_G import notams_by_day
import download_kml_files
import mapPlotting
import mapSnap
from mapPlotting import main as generate_map
from mapSnap import main as capture_image

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

def send_telegram_image(chat_id, api_key, img_path, caption=None):
    """
    Sends an image to the specified Telegram chat.
    
    Parameters:
    - chat_id (str): ID of the chat to send the message to.
    - api_key (str): API key for the Telegram bot.
    - img_path (str): Path to the image file to send.
    - caption (str, optional): Optional caption to include with the image.
    """
    print(f"Trying to send image from path: {img_path}")  # Debug: print image path
    
    # Check if the image exists at the specified path
    if not os.path.exists(img_path):
        print(f"Image not found at path: {img_path}")
        return
    
    base_url = f"https://api.telegram.org/bot{api_key}/sendPhoto"
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
def read_notam_ids(filename="notamIDs.txt"):
    try:
        with open(filename, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def write_notam_ids(ids, filename="notamIDs.txt"):
    with open(filename, "w") as file:
        for notam_id in ids:
            file.write(f"{notam_id}\n")

# Read existing NOTAM IDs from file
existing_ids = read_notam_ids()

# Extract all NOTAMs, then filter to get new NOTAMs based on their IDs (notam_number)
all_notams = [notam for date in notams_by_day for notam in notams_by_day[date]]
new_notams = [notam for notam in all_notams if notam[0] not in existing_ids]

# Processing new NOTAMs
for notam in new_notams:
    notam_id = notam[0]
    
    # Download KML files
    download_kml_files.download_kml_files()


    # Generate the maps (HTML files)
    generate_map()


    # Capture images from the generated maps
    capture_image()
    
    # Format the NOTAM message and send it
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
    img_path = os.path.join('SNAPs', img_name)
    if os.path.exists(img_path):
        send_telegram_image(GROUP_CHAT_ID, API_KEY, img_path, caption=f"Image for NOTAM {notam_id}")
        
    send_telegram_message(GROUP_CHAT_ID, API_KEY, message)
    existing_ids.add(notam[0])

# Write the updated NOTAM IDs back to the file
write_notam_ids(existing_ids)
