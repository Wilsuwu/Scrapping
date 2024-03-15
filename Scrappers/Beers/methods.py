from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def click(driver, locator: tuple, wait_time: int = 2) -> None:
    element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
    element.click()

def enter_text(driver, locator: tuple, text: str, wait_time: int = 2) -> None:
    element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
    element.send_keys(text)

def get_text(driver, locator: tuple, wait_time: int = 2) -> str:
    element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
    return element.text

### methods 
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_titles(products_list):
    titles = []
    try:
        for e in products_list:
            a = e.find_element(By.TAG_NAME, 'a').text
            titles.append(a)

    except:
        print('Error occurred while getting the titles')

    return titles

def get_prices(products_list):
    prices, discount_prices = [], []
    try:
        for e in products_list:
            price = e.find_elements(By.TAG_NAME, 'p')[0].text
            d_price = e.find_elements(By.TAG_NAME, 'p')[1].text
            prices.append(price)
            discount_prices.append(d_price)

    except:
        print('Error occurred while getting the prices')

    return prices, discount_prices

