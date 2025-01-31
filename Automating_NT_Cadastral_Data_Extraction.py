from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set up Edge options with a custom download directory
download_dir = r"C:\Users\AlinaCui\Downloads\NRMapsDownloads"  # Specify your preferred download directory here

# Make sure the directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set up Edge options
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,  # Automatically download without prompt
    "download.directory_upgrade": True,     # Allow directory to be changed
    "safebrowsing.enabled": True            # Enable safe browsing for downloads
})

# Set up the Edge Service with the path to msedgedriver
driver_path = r"c:\Users\AlinaCui\Downloads\edgedriver_win32\msedgedriver.exe"  # Ensure this path is correct
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=options)

# Open the website
driver.get("https://nrmaps.nt.gov.au/rangelands.html")

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Number of pages to download (adjust as needed)
num_pages = 165

for page_num in range(1, num_pages + 1):
    print(f"Downloading data from page {page_num}...")
    
    # Wait for the export button to be clickable
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]")))
    export_button.click()
    
    # Select CSV from the dropdown menu
    csv_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'CSV')]")))
    csv_option.click()
    
    # Wait a bit to ensure the download starts (adjust time as necessary)
    time.sleep(2)
    
    # Navigate to the next page
    if page_num < num_pages:
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Next Page']")))
        next_button.click()
        time.sleep(2)  # Adjust if needed

print("All pages downloaded.")
driver.quit()