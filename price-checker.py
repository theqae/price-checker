from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

# List of URLs
urls = [
    "https://www.harristeeter.com/p/gevalia-frothy-cappuccino-2-step-k-cup-espresso-pods-with-cappuccino-froth-packets/0004300005772",
    "https://www.harristeeter.com/p/alexia-crispy-panko-breaded-onion-rings/0083418300705",
    "https://www.harristeeter.com/p/newman-s-own-four-cheese-thin-crust-frozen-pizza/0002066200600",
    "https://www.harristeeter.com/p/california-pizza-kitchen-marherita-crispy-thin-crust-frozen-pizza/0007192129053",
    "https://www.harristeeter.com/p/ben-jerry-s-chocolate-fudge-brownie-ice-cream-pint/0007684010047",
    "https://www.harristeeter.com/p/de-waflebakkers-chocolate-chip-pancakes/0067984410465"
]

# Set up the Selenium Chrome driver
service = Service(ChromeDriverManager().install())

for url in urls:
    # Initialize the driver for each URL
    driver = webdriver.Chrome(service=service)

    # Load the page using Selenium
    driver.get(url)

    # Wait for the page to fully load
    wait = WebDriverWait(driver, 10)
    webPriceElement = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-qa="cart-page-item-unit-price"]')))

    # Get the page source
    pageSource = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(pageSource, 'html.parser')

    # Extract unit price if present
    unitPriceElement = soup.find(attrs={'data-qa': 'cart-page-item-unit-price'})
    unitPriceValue = unitPriceElement.text.strip() if unitPriceElement else "Unit price not found"

   # Extract coupon information if present
    savingsCenterRow = soup.find('div', {'data-qa': 'savings-center-row-other-coupon'})
    if savingsCenterRow:
        couponTextSpan = savingsCenterRow.find('span', class_='kds-Text--s text-primary ml-8 -mt-1')
        couponInfo = couponTextSpan.text.strip() if couponTextSpan else "Coupon not found"
    else:
        couponInfo = "Coupon not found"

    # Print results
    print("URL:", url)
    print("Unit Price:", unitPriceValue)
    print("Coupon:", couponInfo)
    print()