import pandas as pd
import re
import time
import traceback

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



def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


#url_main = "https://www.mercadolibre.com.ar/"
#driver.get("https://www.mercadolibre.com.ar/")

# Search for a product
def search_product(driver, text):
    
    try:
        accept_cookies = (By.XPATH, '//button[@class="cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept"]')
        click(driver, accept_cookies)
    except Exception as e:
        pass

    search_input =  (By.XPATH, '//*[@id="cb1-edit"]')
    enter_text(driver, search_input, text)

    search_button = (By.XPATH, '//button[@class="nav-search-btn"]')
    click(driver, search_button)



# Obtener total de resultados
# Get total results
def get_total_results(driver, class_="span.ui-search-search-result__quantity-results"):
    try:
        element = driver.find_element(By.CSS_SELECTOR, class_)
        return int(element.text.split()[0].replace(",", ""))
    except:
        print("Failed to retrieve the total number of results.")
        return 0


def get_elements(driver, locator: tuple, wait_time: int = 3) -> list:
    return WebDriverWait(driver, wait_time).until(EC.visibility_of_all_elements_located(locator))


def scrape_categories_and_follow_link(driver):

    try:
        # Locate the <li> elements within the <ul> (as in your original code)
        ul_element = driver.find_element(By.XPATH, "//h3[text()='Categories']/following-sibling::ul")
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')

        # Print the categories and their indices
        for index, li in enumerate(li_elements):
            text = li.text
            print(f"Index {index}: {text}")

        # Ask the user to choose an index
        choice = int(input("Choose the index of the category you want to go to: "))

        # Check if the choice is valid
        if 0 <= choice < len(li_elements):
            # Get the link (href) of the selected category
            selected_link = li_elements[choice].find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Open the link in the same current window
            driver.get(selected_link)

            # Now you can continue scraping on the new page
            # For example, you can find elements on the new page with find_element or find_elements

            # Example: Get the title of the new page
            new_page_title = driver.title
            print(f"Title of the new page: {new_page_title}")

            # You can perform further scraping actions on the new page here

        else:
            print("Invalid choice. Please choose a valid index.")

    except NoSuchElementException as e:
        print("It seems 'Categories' does not exist:", e)
        pass


def get_products(driver, text):
    ml_url = "https://www.mercadolibre.com.ar/"
    driver.get(ml_url)

    search_product(driver, text)
    url = driver.current_url
    print("Searching in:", url)
    print('Page title:', driver.title)

    scrape_categories_and_follow_link(driver)

    
    print('Getting products')
    product_div_class =  "ui-search-layout__item"
    locator = (By.CLASS_NAME, product_div_class)
    products = get_elements(driver, locator)
    print(f'Found {len(products)} products')

    return products




def get_href_attributes(products):
    # List to store the results
    href_attributes = []
    try:
        for element in products:
            # Get the 'href' attribute of 'a' elements
            href = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            # Add the 'href' attribute to the list
            href_attributes.append(href)

    except:
        print('An error occurred while getting the "href" elements')

    return href_attributes

# products is a list of web elements from which you want to extract the 'href' attributes
# href_list = get_href_attributes(products)
# print(href_list)




def scrape_all_pages(driver, text) -> list:
    # Scroll through the page and extract the links of the products appearing on it

    get_products(driver, text)
    # Get the total number of results
    total_results = get_total_results(driver)  # this function gets the total number of results
    print(f"Total results: {total_results}")

    try:
        click(driver, (By.XPATH, '//button[contains(text(), "Accept cookies")]'))
    except NoSuchElementException:
        # The cookies message is not present, do nothing
        pass
    except TimeoutException:
        pass
    
    next_button_exists = True
    # Initialize a list to store all href attributes
    all_href_attributes = []
    while next_button_exists:
        
        time.sleep(5)
        products_locator = (By.XPATH, '//li[@class="ui-search-layout__item"]')
        products = get_elements(driver, products_locator)
        
        # Get href attributes of the products
        href_attributes = get_href_attributes(products)
        all_href_attributes.extend(href_attributes)
        
        

        try:
            next_button = (By.XPATH, '//li[@class="andes-pagination__button andes-pagination__button--next shops__pagination-button"]')
            click(driver, next_button, 3)
            print('Clicking on next')
        except Exception as e:
            print('Next button does not exist')
            next_button_exists = False
            #traceback.print_exc()
            pass


    return all_href_attributes


def get_features(driver):
    try:
        # Click on the "See all features" link
        driver.find_element(By.XPATH, "//span[contains(text(),'See all features')]").click()
    except Exception as e:
        print("Could not click 'See all features'. Error:", str(e))
        return None

    # Find all tables with class 'andes-table'
    tables = driver.find_elements(By.XPATH, "//table[@class='andes-table']")

    # Initialize a dictionary to store the data
    features_data = {}

    # Iterate through the tables
    for table_element in tables:
        # Find all rows of the table with class 'andes-table__row ui-vpp-striped-specs__row'
        rows = table_element.find_elements(By.XPATH, "//tr[@class='andes-table__row ui-vpp-striped-specs__row']")

        # Iterate through the rows
        for row in rows:
            # Find the cells of the row (th for key and td for value)
            cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                # Extract the text of the first cell (th) as key and the text of the second cell (td) as value
                key = cells[0].text
                value = cells[1].text
                features_data[key] = value

        # If we have found and processed the first table, exit the loop
        if features_data:
            break

    # Return the general features data or None if no features were found
    return features_data if features_data else None


def get_stock_number(driver):
    try:
        # Wait for a maximum of 3 seconds for the element to appear
        stock_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='ui-pdp-buybox__quantity__available']"))
        )
        stock_available = stock_element.text
        match = re.search(r'\d+', stock_available)
        if match:
            return int(match.group())
    except (NoSuchElementException, TimeoutException):
        try:
            # Wait for a maximum of 3 seconds for the element to appear
            stock_status_text = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'Last available!')]"))
            )
            if stock_status_text.text == 'Last available!':
                return 1
        except (NoSuchElementException, TimeoutException):
            pass
    return 0





def product_data(driver, product_list: list):
    # Get the total length of the list to calculate percentage
    total_length = len(product_list)
    product_data_list = []

    # Initialize a counter to keep track of iteration
    counter = 0

    for product in product_list:
        # Update counter
        counter += 1

        # Calculate and print the percentage of completion
        completion_percentage = (counter / total_length) * 100
        print(f"Progress: {completion_percentage:.2f}%")

        driver.get(product)
        time.sleep(3)
        product_url = product
        product_name = "No Name"
        product_price = "No Price"
        review_count = "No Reviews"
        product_rating = "No Rating"
        product_stock = 0
        product_features = ""

        try:
            product_name = get_text(driver, (By.XPATH, '//h1[@class="ui-pdp-title"]'), 3)
            product_price = get_text(driver, (By.XPATH, '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]'), 3)
            review_count = get_text(driver, (By.XPATH, '//span[@class="ui-pdp-review__amount"]'), 3)
            product_rating = get_text(driver, (By.XPATH, '//p[@class="ui-review-capability__rating__average ui-review-capability__rating__average--desktop"]'), 3)
            product_features = get_features(driver)
            product_stock = get_stock_number(driver)
        except Exception as error:
            print(error)
            pass

        product_data = [product_url, product_name, product_price, review_count, product_rating, product_stock, product_features]
        product_data_list.append(product_data)

    return product_data_list


def create_product_report(product_data_list: list) -> None:
    columns = ['URL', 'Name', 'Price', 'Reviews', 'Rating', 'Stock', 'Features']
    df = pd.DataFrame(product_data_list, columns=columns)
    print('Creating Excel report')
    df.to_excel(f"product_report.xlsx", index=False)
    print('Report exported to Excel')
