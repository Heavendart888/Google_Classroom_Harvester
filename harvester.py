"""
Project: Classroom Harvester (Red Team Edition)
Author: Biswajit Sahoo
Description: A Selenium-based automation tool to 'harvest' and download all materials 
             from a Google Classroom feed, bypassing 'View More' pagination and hidden elements.
"""

import os
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

# --- CONFIGURATION ---
DOWNLOAD_DIR = "Classroom_Downloads"
PROFILE_PATH = os.path.join(os.getcwd(), "edge_selenium_profile")
# Defaulting to look for driver in the current directory
DRIVER_PATH = os.path.join(os.getcwd(), "msedgedriver.exe")

def setup_driver():
    if not os.path.exists(DRIVER_PATH):
        print(f"\n[!] CRITICAL ERROR: 'msedgedriver.exe' not found at {DRIVER_PATH}")
        print("Please download the Edge Driver matching your browser version and place it in this folder.")
        raise FileNotFoundError("Missing msedgedriver.exe")

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument(f"user-data-dir={PROFILE_PATH}")
    options.add_argument("--start-maximized")
    
    # Red Team / Stealth args to mask automation behavior
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = EdgeService(executable_path=DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    return driver

def get_drive_direct_link(url):
    """ Extracts ID from Drive links (works for /d/, id=, open?id=) and converts to export link. """
    if "drive.google.com" not in url:
        return None
        
    patterns = [
        r'\/d\/([a-zA-Z0-9_-]+)', 
        r'id=([a-zA-Z0-9_-]+)', 
        r'open\?id=([a-zA-Z0-9_-]+)'
    ]
    
    for p in patterns:
        match = re.search(p, url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?id={file_id}&export=download"
    return None

def get_unique_filename(folder, filename):
    """ Prevents overwriting files by adding numerical suffixes (e.g., File (1).pdf). """
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base} ({counter}){ext}"
        counter += 1
    return new_filename

def download_file(driver, url, folder, default_name):
    # Hijack browser cookies for authenticated download
    selenium_cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    try:
        response = session.get(url, stream=True)
        if response.status_code != 200:
            print(f"  [X] Failed (Status {response.status_code}): {default_name}")
            return

        if "Content-Disposition" in response.headers:
            fname = response.headers["Content-Disposition"].split("filename=")[1].strip('"')
        else:
            fname = default_name + ".pdf" 

        # Sanitize filename
        fname = "".join([c for c in fname if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-', '(', ')')]).strip()
        
        final_filename = get_unique_filename(folder, fname)
        filepath = os.path.join(folder, final_filename)

        print(f"  [+] Downloading: {final_filename}...")
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
    except Exception as e:
        print(f"  [!] Error downloading {default_name}: {e}")

def force_reveal_content(driver):
    """ Finds hidden 'View more' buttons inside topics and forces them to expand. """
    # 1. Click 'View more'
    try:
        view_more_elements = driver.find_elements(By.XPATH, "//*[text()='View more'] | //*[contains(text(), 'View more')]")
        for btn in view_more_elements:
            try:
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("  [>] Expanded a topic...")
                    time.sleep(2)
            except:
                pass
    except:
        pass

    # 2. Expand individual assignments
    try:
        collapsed_items = driver.find_elements(By.CSS_SELECTOR, '[aria-expanded="false"]')
        if len(collapsed_items) > 0:
            for item in collapsed_items:
                try:
                    driver.execute_script("arguments[0].click();", item)
                    time.sleep(0.2)
                except:
                    pass
    except:
        pass

def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    try:
        driver = setup_driver()
    except FileNotFoundError as e:
        print(e)
        return

    driver.get("https://classroom.google.com/")
    
    print("\n" + "="*60)
    print("           CLASSROOM HARVESTER - MANUAL LOGIN")
    print("="*60)
    print("1. Browser is open. Please LOG IN to your account.")
    print("2. Navigate to the specific Class > 'Classwork' tab.")
    print("3. IMPORTANT: Scroll to the TOP of the list.")
    print("="*60 + "\n")
    
    input("Press ENTER when you are ready to start harvesting...")

    print("\n--- STARTING HARVEST ---")
    
    unique_links = set()
    scraped_count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    consecutive_no_change = 0

    while True:
        force_reveal_content(driver)
        
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                href = link.get_attribute("href")
                text = link.text.strip() or "Untitled"
                
                if href and "drive.google.com" in href:
                    direct_link = get_drive_direct_link(href)
                    if direct_link:
                        if direct_link not in unique_links:
                            unique_links.add(direct_link)
                            scraped_count += 1
                            print(f"  -> Found: {text}")
                            download_file(driver, direct_link, DOWNLOAD_DIR, text)
            except StaleElementReferenceException:
                pass 

        # Scroll logic
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2.0)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        current_scroll = driver.execute_script("return window.pageYOffset + window.innerHeight")
        
        if current_scroll >= new_height:
            if new_height == last_height:
                consecutive_no_change += 1
                if consecutive_no_change >= 3:
                    print("Reached absolute bottom. Stopping.")
                    break
            else:
                consecutive_no_change = 0
            last_height = new_height
        else:
            consecutive_no_change = 0

    print(f"\nCompleted. Total files: {scraped_count}")
    print(f"Location: {os.path.abspath(DOWNLOAD_DIR)}")
    input("Press Enter to close...")
    driver.quit()

if __name__ == "__main__":
    main()
