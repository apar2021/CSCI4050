# Packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

start = time.time()
# Time for explicit waits (seconds)
LOAD_TIME = 0.5


# Optionally render the chrome window
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Local URL to test on
URL = "http://127.0.0.1:5000"

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)
time.sleep(5)

menu = driver.find_element(By.CLASS_NAME, "horizontal-menu")
elements = menu.find_elements(By.TAG_NAME, "li")
for e in elements:
    print(e.text)

# Pause
driver.implicitly_wait(5)

# Returns a list of menu elements: Home, Cart, Register, and Login
# Each can be clicked
def get_menu():
    driver.get(URL)
    driver.implicitly_wait(5)
    menu = driver.find_element(By.CLASS_NAME, "horizontal-menu")
    elements = menu.find_elements(By.TAG_NAME, "li")
    return(elements)

# Navigate to the 
def get_login():
    elements = get_menu()
    login = elements[3]
    login.click()
    driver.implicitly_wait(5)
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    login = driver.find_element(By.XPATH, "/html/body/form/input[3]")
    return email_input, password_input, login

def get_register():
    elements = get_menu()
    register = elements[2]
    register.click()
    driver.implicitly_wait(5)
    name_input = driver.find_element(By.ID, "name")
    phone_input = driver.find_element(By.ID, "phone")
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    confirm_password_input = driver.find_element(By.ID, "confirm_password")
    submit = driver.find_element(By.XPATH, "/html/body/form/input[2]") # Adjust if HTML Changes
    return name_input, phone_input, email_input, password_input, confirm_password_input, submit






# Registration Test Cases
# Register Invalid Password
def register_short_password():
    name_input, phone_input, email_input, password_input, confirm_password_input, submit = get_register()
    name_input.send_keys("Jackson")
    phone_input.send_keys("7066128573")
    email_input.send_keys("fakemail123@gmail.com")
    password_input.send_keys("1")
    confirm_password_input.send_keys("1")
    submit.click()
    driver.implicitly_wait(5)
    #print(driver.current_url)
    if "signup" in driver.current_url:
        print("1")
        # Todo make sure error flashes
    else:
        print("Fail")
        return 0
    
def register_no_info():
    name_input, phone_input, email_input, password_input, confirm_password_input, submit = get_register()
    submit.click()
    driver.implicitly_wait(5)
    if "signup" in driver.current_url:
        # Todo: How should the site prompt the user for not having info
        # Once I know I can check for it
        raise NotImplemented
    else:
        print("Register No Info Fail: Wrong URL")
        return 0





# Requires Registering Without verified
# TODO
def login_no_validation():
    email_input, password_input = get_login()
    email_input.send_keys("fakemail123123123123@gmail.com")
    #password_input


#login_no_validation()
register_short_password()
end = time.time()
print(f"Tests Complete in {(end-start):.2f} Seconds")

#time.sleep(60)







