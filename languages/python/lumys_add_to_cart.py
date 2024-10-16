#!/usr/bin/env python3
# Put photos to print in the cart in a Lumys galery : https://lumys.photo/
# INSTALL: pip install selenium
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

URL = "..."
ACCESS_CODE = "..."
ACCESS_EMAIL = "..."

TIMEOUT = 5  # max seconds to wait for an element to be clickable
TYPES = (
    ("Standard", ("10x15", "13x19", "15x23", "18x27", "20x30")),
    ("Agrandissements", ("24x36", "40x45", "40x60", "50x75")),
)

options = ChromeOptions()
# Allows to keep the browser open after script has executed:
options.add_experimental_option("detach", True)
driver = Chrome(options=options)
driver.get(URL)

def wait_for(css_selector):
    wdw = WebDriverWait(driver, timeout=TIMEOUT)
    return wdw.until(element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

def elem(css_selector, parent=None):
    "Shorthand function"
    return (parent or driver).find_element(By.CSS_SELECTOR, css_selector)

def elems(css_selector, parent=None):
    "Shorthand function"
    return (parent or driver).find_elements(By.CSS_SELECTOR, css_selector)

def scroll_to(elem):
    driver.execute_script("arguments[0].scrollIntoView()", elem)

def hide(elem):
    driver.execute_script("arguments[0].style.display = 'none'", elem)

def click_with_retry(elem):
    try:
        elem.click()
    except ElementClickInterceptedException:
        print("Retrying click...")
        elem.click()

def auth(access_code, access_email):
    print("Filling password...")
    wait_for('input[data-test="galleryAccessCode"]').send_keys(access_code)
    print("Submitting login form 1st page...")
    click_with_retry(wait_for('button[type="submit"]'))
    print("Filling email...")
    wait_for('input[data-test="galleryAccessEmail"]').send_keys(access_email)
    print("Submitting login form 2nd page...")
    click_with_retry(wait_for('button[type="submit"]'))

def add_selection_to_cart(selection_id, type, format):
    type_index, formats = next((i, formats)
        for i, (type_name, formats) in enumerate(TYPES)
        if type_name == type)
    format_index = formats.index(format)
    line_index, cell_index = 0, 0
    while True:
        # print(f"  {line_index=} {cell_index=}")
        driver.get(f"{URL}/selections/{selection_id}")
        wait_for(".lumico-cart-add")
        scroll_to(wait_for(".lumico-cart-add"))
        hide(elem("header"))
        hide(elem("footer"))
        lines = elems(".line")
        # print("  #lines:", len(lines))
        line_items = elems(".line-item", parent=lines[line_index])
        # print("  #line_items:", len(line_items))
        line_item = line_items[cell_index]
        scroll_to(line_item)
        click_with_retry(elem(".lumico-cart-add", parent=line_item))
        # Wait for new page to load, and select the first option ("Tirages papiers photo"):
        click_with_retry(wait_for('[data-test="section"]'))
        radio_btns = elems(".q-radio")
        # Select radio option:
        click_with_retry(radio_btns[type_index])
        click_with_retry(wait_for('button[data-test="buyButton"]'))
        # Wait for new page to load, and consider formats:
        wait_for('button[data-test="format"]')
        formats = elems('[data-test="format"]')
        click_with_retry(formats[format_index])
        select_finition_mat = wait_for('button[data-test="selectMat"]')
        scroll_to(select_finition_mat)
        click_with_retry(select_finition_mat)
        click_with_retry(wait_for('button[data-test="addToCart"]'))
        btn_notif = wait_for('.nav-button-notification')
        print("  elements in cart:", btn_notif.text)
        cell_index += 1
        if cell_index == len(line_items):
            line_index += 1
            if line_index == len(lines):
                print("No more photos in selection - Stopping\n")
                break
            cell_index = 0

if __name__ == "__main__":
    auth(ACCESS_CODE, ACCESS_EMAIL)
    print("Selection TresGrandsTirages...")
    add_selection_to_cart("66ce3ab4c9c6803d881040ca", "Agrandissements", "24x36") # 1
    print("Selection GrandsTirages...")
    add_selection_to_cart("66ce347b61b0f98c5ce4a6fd",  "Standard", "20x30")       # 6
    print("Selection TiragesAnnaLucas...")
    add_selection_to_cart("66ce333261b0f98c5ce4a17e", "Standard", "10x15")        # 26
    print("Selection Tirages1-JM_Claire...")
    add_selection_to_cart("66dd84befc61d0e7cf3af3d6", "Standard", "10x15")        # 5
    print("Selection Tirages2-BernardCatherine...")
    add_selection_to_cart("66dd854f1190a10b1b01b2a8", "Standard", "10x15")        # 7   
