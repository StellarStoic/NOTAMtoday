## NOTAM Today Bot
_CHECKING ONLY NOTAMS FROM BETWEEN **GND** AND UP **TO 3000m** AND PROCESSING **QR**, **QW** and **QOR** Q-CODE MESSAGES ONLY_

**NOTAM Today Bot** _is a Telegram bot designed to fetch, analyze, draw and relay NOTAM (Notice to Airmen) data to users. It processes and visualizes NOTAM data, ensuring that sky junkies, paragliding pilots and hang gliding pilots or maybe even aviation professionals receive a relevant airspace information for them and not all NOTAM messages which is mostly why people don't read NOTAMs. It's a mess putting all NOTAMS in one list_


### Features:
1. **Automated NOTAM Retrieval**: Downloads today's NOTAMs, ensuring free flyers like PG and HG pilots get relevant up-to-date Slovenian airspace information sutable for them, every morning at 5:30 in the Telegram club group chat.
2. **Data Cleanup**: Automatically manages and cleans old NOTAM data to ensure the system remains efficient and clean.
3. **Map Visualization**: Processes the NOTAM data, plots them on a map, and sends the visual representation to the [Club Telegram group](https://t.me/klvcvek).

![Telegram message sample.](https://cdn.nostr.build/i/e819c150aa8dad9b7c1d840c649bbe1489a056194e8d91d26a88524d5f553303.png)


### Components:
- **NOTAMtodaybot.py**: The main script responsible for interacting with the Telegram API, sending NOTAM data and associated images to the group.
- **handling.py**: Fetches the latest NOTAM data in KML format and manages (deletes) old NOTAM files.
- **mapPlotting.py**: Processes the NOTAM data and plots them on a map for visualization.
- **mapSnap.py**: Uses Selenium to capture and save the visual representation of the NOTAM data.


### How it Works:
1. the `today_notam_G.py` script is fatching the notam data that is relevant to PG and HG pilots inside of Slovenia borders. _(notams relevant for up to 3000m and only procesing q-Code data containing QR, QW and QOR messages)_
1. The `handling_files.py` retrieves the latest NOTAM KML files for today unzip them and storing kml files to KMLs folder. It also clean up all the old NOTAM data from the notamIDs.txt, and other folders containing files with a none valid NOTAM ID number name. In the `notamIDs.txt` we can manually set the notam IDs like so `C1120/23` in each line to avoid publishing them in the mornings if they are really, really unimportant.
2. The NOTAMs are then processed and visualized on a map using `mapPlotting.py` using [Folium](https://python-visualization.github.io/folium/), and created html visual representation files are stored in HTMLs folder.
3. `mapSnap.py` captures these visual html representations as a screenshot taken with solenium, and then saving these screenshots as images in SNAPs folder.
4. `NOTAMtodaybot.py` sends NOTAM messages valid for today, every morning to telegram group chat at 05:30. 


### Setup & Usage:
1. Ensure all required Python libraries are installed. to do this use `pip install -r requirements.txt`

2. Store secrets and configurations in the `ENV` file like this...
`GROUP_CHAT_ID=-1105658887564`
`API_KEY=6025761979:TrewER4ewSSwdE-R-2NtrEd4Z6Dd`

3. Run `NOTAMtodaybot.py` to start the bot.
