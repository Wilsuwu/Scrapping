from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def click(driver, locator: tuple, wait_time: int = 2) -> None:
    element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
    element.click()

def enter_text(driver, locator: tuple, text: str, wait_time: int = 2) -> None:
    element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
    element.send_keys(text)

def get_text(driver, locator: tuple, wait_time: int = 2) -> str:
    element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located(locator))
    return element.text


### Methods
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_titles(products_list):
    titles = []
    try:
        for element in products_list:
            title = element.find_element(By.XPATH, './/span[@class="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body"]').text
            titles.append(title)

    except:
        print('An error occurred while getting the elements')

    return titles


def get_prices(products_list):
    prices, discount_prices = [], []
    
    try:
        
        for element in products_list:
            price = element.find_element(By.XPATH, './/span[@class="valtech-carrefourar-product-price-0-x-currencyContainer"]').text
            prices.append(price)
            try:
                discount_price = element.find_element(By.XPATH, './/span[@class="valtech-carrefourar-product-price-0-x-listPriceValue strike"]').text
                discount_prices.append(discount_price)
            except:
                print("Discount not found")
                discount_prices.append(price)
            
    
    except:
        print('An error occurred while getting the elements')

    return prices, discount_prices

def get_href(product_list):
    hrefs = []
    for e in product_list:
        href = e.find_element(By.TAG_NAME,  'a').get_attribute('href')
        hrefs.append(href)
    
    return hrefs