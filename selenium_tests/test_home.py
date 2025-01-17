from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_helpers.helpers import view_sleep 

service = Service(executable_path="selenium_tests/chromedriver.exe")
DRIVER = webdriver.Chrome(service=service)

DRIVER.get("http://127.0.0.1:5000")

VIEW_TIME = 1

def main():
    test_home_page(DRIVER)
    view_sleep()
    DRIVER.close()

def test_home_page(driver):
    assert "Home" in driver.title

if __name__ == '__main__':
    main()

