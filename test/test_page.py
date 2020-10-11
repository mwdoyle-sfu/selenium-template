from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

from pathlib import Path
import os


def construct_headless_chrome_driver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def get_landing_page_url():
    test_dir = os.getcwd()
    index_path = os.path.join(test_dir, "..", "page", "index.html")
    index_uri = Path(index_path).as_uri()
    return index_uri


# As demonstrated in the linked web page from the course assignment
@contextmanager
def wait_for_page_load(driver, timeout=30):
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until( staleness_of(old_page) )


def test_nonsecret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    # You can place additional test code here to drive this one test
    # Scenario 1
    # 1. land on main page
    driver.implicitly_wait(10)
    driver.get(landing_page)
    wait_for_page_load(driver)
    driver.maximize_window()
    title = "Simple Web Page"
    assert title == driver.title

    # 2. fill in for name and favorite food
    # name
    sample_name = "Miki Sudo"
    name_text_field = driver.find_element_by_id("preferredname")
    name_text_field.send_keys(sample_name)
    # food
    sample_food = "Hot Dogs"
    food_text_field = driver.find_element_by_id("food")
    food_text_field.send_keys(sample_food)

    # 3. fills in a value for the password other than "magic" or "abracadabra"
    sample_code = "secret"
    code_text_field = driver.find_element_by_id("secret")
    code_text_field.send_keys(sample_code)

    # 4. click submit
    driver.find_element_by_id("submit").click()
    wait_for_page_load(driver)

    # 1. redirect to response.html
    # 2. where the response page should include a thank for the user by name
    thank_name_text = driver.find_element_by_id("thankname").text
    assert thank_name_text == sample_name

    # 3. and it should note that the company also likes the same food as the user
    food_ploy_text = driver.find_element_by_id("foodploy").text
    assert food_ploy_text == sample_food

    # 4. and it should not include a button to the secret page
    assert (len(driver.find_elements_by_id("secretButton"))) == 0
    
    driver.quit()


# You may want to add additional tests....

def test_secret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    # Scenario 2
    # 1. lands on main page
    driver.implicitly_wait(10)
    driver.get(landing_page)
    wait_for_page_load(driver)
    driver.maximize_window()
    title = "Simple Web Page"
    assert title == driver.title

    # 2. fills in non-empty values for name and food
    # name
    sample_name = "Miki Sudo"
    name_text_field = driver.find_element_by_id("preferredname")
    name_text_field.send_keys(sample_name)
    # food
    sample_food = "Hot Dogs"
    food_text_field = driver.find_element_by_id("food")
    food_text_field.send_keys(sample_food)

    # 3. fills in either "magic" or "abracadabra"
    sample_code = "magic"
    code_text_field = driver.find_element_by_id("secret")
    code_text_field.send_keys(sample_code)

    # 4. clicks submit
    driver.find_element_by_id("submit").click()
    wait_for_page_load(driver)

    # 1. redirect to response page
    # 2. where the response page should include a thank for the user by name
    thank_name_text = driver.find_element_by_id("thankname").text
    assert thank_name_text == sample_name

    # 3. and it should note that the company also likes the same food as the user
    food_ploy_text = driver.find_element_by_id("foodploy").text
    assert food_ploy_text == sample_food

    # 4. and it should include a button to the secret page
    assert (len(driver.find_elements_by_id("secretButton"))) == 1

    # 5. and clicking the button should redirect to the page at secret.html
    driver.find_element_by_id("secretButton").click()
    wait_for_page_load(driver)

    # 6. and the secret page should thank them by name
    thank_name_text = driver.find_element_by_id("thankname").text
    assert thank_name_text == sample_name

    # 7. and the secret page should repeat the specific secret code entered by the user.
    secret_text = driver.find_element_by_id("secret").text
    assert secret_text == sample_code

    driver.quit()
