# Packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

# Optionally render the chrome window
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Local URL to test on
url = "http://127.0.0.1:5000"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

menu = driver.find_element(By.CLASS_NAME, "horizontal-menu")
elements = menu.find_elements(By.TAG_NAME, "li")
for e in elements:
    print(e.text)

# Pause
time.sleep(0.5) # Load Page

def test_register():
    register_button = elements[2]
    register_button.click()
    time.sleep(5)

test_register()
