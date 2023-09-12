import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    def capture_screenshot(html_path, output_image_path):
        # Set up the Selenium driver in headless mode (no GUI)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('window-size=1280x720') # Do not increase the resolution. Mobile viewer will hate you!
        driver = webdriver.Chrome(options=options)

        
        # Open the HTML file with the driver
        driver.get(f"file://{html_path}")
        
        # Explicitly wait for the map element to be present
        try:
            # element_present = EC.presence_of_element_located((By.ID, 'map_96633ea7002869c56cf6afa8144cb43a'))
            
            # Explicit wait. tell the computer to wait until it sees a specific thing on the webpage
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'ElementID')))
        except Exception as e:
            print(f"Error: {e}")
        
        
        # Capture the screenshot and save it
        driver.save_screenshot(output_image_path)
        
        # Close the driver
        driver.quit()

    def process_html_files_in_directory(directory_path):
        # Ensure the 'SNAPS' directory exists or create it
        screenshot_dir = os.path.join(os.path.dirname(directory_path), 'SNAPs')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        # Iterate through each file in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.html'):
                html_path = os.path.abspath(os.path.join(directory_path, filename))
                screenshot_name = os.path.splitext(filename)[0] + '.png'
                output_image_path = os.path.join(screenshot_dir, screenshot_name)
                capture_screenshot(html_path, output_image_path)

    # Example usage
    directory_path = "HTMLs"
    process_html_files_in_directory(directory_path)
    
if __name__ == "__main__":
    main()
