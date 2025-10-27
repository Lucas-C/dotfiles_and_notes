#!/usr/bin/env python3
"Downloads all new PDFs in https://www.famileo.com/web-family/#/gazette"
# USAGE: ./famileo_archiver.py download_dir phpsessid
# INSTALL: pip install selenium
# In case of `locale.Error: unsupported locale setting` do: locale-gen fr_FR.UTF-8
import argparse, locale, logging, os
from datetime import datetime
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

URL = "https://www.famileo.com/web-family/"
FAMILEO_LINK_TEXT_FORMAT = "Gazette du %d %b %Y > " # %b is in French
FAMILEO_DOWNLOADED_FILE_FORMAT = "Gazette-%Y-%b-%d.pdf" # %b is in English
ARCHIVER_FILE_FORMAT = "Gazette-%Y-%m-%d-%B.pdf" # %b is in French
SCREENSHOT_FILENAME = "famileo-browser-screenshot-on-failure.png"
TIMEOUT = 5  # max seconds to wait for an element to be clickable

def main():
    args = parse_args()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    existing_dates = list_existing_pdf_files(args.download_dir)
    driver = init_browser(args)
    driver.get(URL)
    driver.add_cookie({"name": "PHPSESSID", "value": args.phpsessid})
    driver.get(URL)
    try:
        print("Waiting for wall to be loaded...")
        wait_for(driver, "#ngb-nav-0-panel")
        try:  # Modale d'acceptation des cookies
            driver.find_element(By.CSS_SELECTOR, "#tarteaucitronAllDenied2").click()
            print("Modal #tarteaucitronAllDenied2 discarded")
        except NoSuchElementException:
            pass
        try:  # Modale "Les événements du jour"
            driver.find_element(By.CSS_SELECTOR, "#birthday-modal-ok-button").click()
            print("Modal #birthday-modal-ok-button discarded")
        except NoSuchElementException:
            pass
        wait_for(driver, 'a[href="#/gazette"]').click()
        wait_for(driver, ".gazettes")
        for a in driver.find_elements(By.CSS_SELECTOR, ".gazettes a"):
            link_text = a.get_attribute("textContent")
            publication_day = get_publication_day(link_text)
            if publication_day in existing_dates:
                print("Skipping month already downloaded:", link_text)
            else:
                print("Downloading PDF for:", link_text)
                driver.get(a.get_attribute("href"))
        rename_downloaded_files(args.download_dir)
    except Exception:
        driver.get_screenshot_as_file(SCREENSHOT_FILENAME)
        print("Failure - Screenshot generated:", SCREENSHOT_FILENAME)
        raise

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("download_dir")
    parser.add_argument("phpsessid")
    parser.add_argument("--headless", default=False, action="store_true", help="Headless browser mode")
    parser.add_argument("--detach", default=False, action="store_true", help="Allows to keep the browser open after script has executed")
    parser.add_argument("--debug", default=False, action="store_true", help="Enable Selenium debug logs")
    args = parser.parse_args()
    if ';' in args.phpsessid or '=' in args.phpsessid:
        parser.error("Invalid ; or = character in $PHPSESSID provided")
    return args

def init_browser(args):
    options = ChromeOptions()
    if args.headless:
        options.headless = True
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
    options.add_argument("window-size=1920,1080")
    options.add_experimental_option("prefs", {
        "download.default_directory": args.download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True  # disable Chrome PDF Viewer
    })
    if args.detach:
        options.add_experimental_option("detach", True)
    return Chrome(options=options)

def wait_for(driver, css_selector):
    wdw = WebDriverWait(driver, timeout=TIMEOUT)
    return wdw.until(element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

def get_publication_day(link_text):
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")  # set locale for strptime
    # Strangely, this was not needed with Python 3.11 under Windows:
    link_text = link_text.replace("avr.", "avril")
    return datetime.strptime(link_text, FAMILEO_LINK_TEXT_FORMAT)

def list_existing_pdf_files(download_dir):
    existing_dates = set()
    locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")  # set locale for strptime
    for pdf_file in Path(download_dir).glob("*.pdf"):
        existing_dates.add(datetime.strptime(pdf_file.name, ARCHIVER_FILE_FORMAT))
    return existing_dates

def rename_downloaded_files(download_dir):
    for pdf_file in Path(download_dir).glob("*.pdf"):
        try:
            datetime.strptime(pdf_file.name, ARCHIVER_FILE_FORMAT)
            continue  # File already has correct format
        except ValueError:
            pass
        # Testing original file name format: the name of the PDF file produced by famileo
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")  # set locale for strptime
        publication_day = datetime.strptime(pdf_file.name, FAMILEO_DOWNLOADED_FILE_FORMAT)
        # Renaming to new file format, so that alphabetical sorting is correct in nginx index
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")  # set locale for strptime
        new_filename = publication_day.strftime(ARCHIVER_FILE_FORMAT)
        print(f"Renaming {pdf_file.name} into {new_filename}...")
        pdf_file.rename(new_filename)


if __name__ == "__main__":
    main()
