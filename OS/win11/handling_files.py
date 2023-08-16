import os
import zipfile
import requests
import io
import shutil
from today_notam_G import notams_by_day
from datetime import datetime

KML_FOLDER = "KMLs"
IMAGES_FOLDER = "SNAPs"
LEAFLET_HTML_IMAGES = "HTMLs"
NOTAM_IDS_FILE = "notamIDs.txt"


def get_existing_notam_ids():
    if os.path.exists(NOTAM_IDS_FILE):
        with open(NOTAM_IDS_FILE, 'r') as f:
            return set(f.read().splitlines())
    return set()

# def save_new_notam_id(notam_id):
#     with open(NOTAM_IDS_FILE, 'a') as f:
#         f.write(f"{notam_id}\n")

def handling_files():
    if not os.path.exists(KML_FOLDER):
        os.makedirs(KML_FOLDER)
    
    today = datetime.now().date()
    notams_today = notams_by_day[today]
    
    existing_ids = get_existing_notam_ids()
    current_ids = set()

    for notam in notams_today:
        notam_id = notam[0]  # Assuming the NOTAM ID is the first element in the tuple
        kml_url = notam[-1]  # Assuming kml link is the last element
        
        current_ids.add(notam_id)

        if notam_id in existing_ids:
            continue

        kml_filename = os.path.join(KML_FOLDER, kml_url.split('/')[-1])
        
        response = requests.get(kml_url)
        
        if response.content.startswith(b"PK"):  # ZIP file check
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                with z.open(z.namelist()[0]) as kml_file:  # Get the first file inside ZIP
                    kml_content = kml_file.read()
                    with open(kml_filename.replace(".kmz", ".kml"), "wb") as out_file:
                        out_file.write(kml_content)
        else:
            with open(kml_filename, 'wb') as f:
                f.write(response.content)

        # save_new_notam_id(notam_id)

    # Cleanup old NOTAMs
    for existing_id in existing_ids:
        if existing_id not in current_ids:
            kml_filename = os.path.join(KML_FOLDER, f"{existing_id.replace('/', '-')}.kml")
            snap_filename = os.path.join(IMAGES_FOLDER, f"{existing_id.replace('/', '-')}.png")
            html_filename = os.path.join(LEAFLET_HTML_IMAGES, f"{existing_id.replace('/', '-')}.html")
            
            for file in [kml_filename, snap_filename, html_filename]:
                if os.path.exists(file):
                    os.remove(file)

            # Remove the NOTAM ID from the file
            with open(NOTAM_IDS_FILE, 'r') as f:
                lines = f.readlines()
            with open(NOTAM_IDS_FILE, 'w') as f:
                for line in lines:
                    if line.strip("\n") != existing_id:
                        f.write(line)
                        
if __name__ == "__main__":
    handling_files()
