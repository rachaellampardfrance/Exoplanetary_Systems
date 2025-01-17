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

def main():
    """run all tests"""
    test_search_bar(DRIVER)

    # driver.quit()
    DRIVER.close() # closes one tab at a time but if one all is closed by default


def test_search_bar(driver):
    """Test search bar yields results or redirects"""

    test_search_none_redirect(driver)
    view_sleep() # sleep for my viewing

    test_search_suggs_ete(driver)
    view_sleep()

    test_search_bar_success(driver)
    view_sleep()
    

def test_search_none_redirect(driver):
    """Search bar redirects to empty suggestions page with no input"""
    search_elem = if_search_get(driver)
    search_elem.send_keys("", Keys.ENTER)

    assert "Suggestions" in driver.page_source
    assert "No suggestions available" in driver.page_source


def test_search_suggs_ete(driver):
    """End to End
    search bar gives suggestions if no system found
    and suggestion links lead to system
    """
    tables = ["sug-planets", "sug-stars", "sug-systems"]

    search_elem = if_search_get(driver)
    search_elem.send_keys("TOI" + Keys.ENTER)

    view_sleep()

    for table in tables:
        try:
            elem = driver.find_element(By.ID, table)
        except:
            continue
        else:
            # if search element if not found test will exit after 5
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "TOI"))
            )
        
            link = elem.find_element(By.PARTIAL_LINK_TEXT, "TOI")
            link.click()
            assert "System" in driver.page_source
            back_page_wait(driver)


def test_search_bar_success(driver):
    stellar_bodies = ["WASP-12 b", "WASP-12 C", "WASP-12"] # planet, star, system/main star

    for body in stellar_bodies:
        search_elem = if_search_get(driver)
        search_elem.send_keys(body + Keys.ENTER)

        th_system = driver.find_element(By.TAG_NAME, 'h2') 

        assert "WASP-12" in th_system.text
        back_page_wait(driver)


def if_search_get(driver):
    """Wait for search bar and return if found"""
    wait_for_search_bar(driver)
    return get_search_bar(driver)

def wait_for_search_bar(driver):
    """if search element if not found test will exit after 5""" 
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "search"))
    )

def get_search_bar(driver):
    """get search bar element"""
    elem = driver.find_element(By.NAME, "search")
    elem.clear()
    return elem

def back_page_wait(driver):
    """return to previous page"""
    view_sleep()
    driver.back()
    view_sleep()

if __name__ == '__main__':
    main()