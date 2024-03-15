import re
import time
import traceback

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from methods import get_driver, scrape_all_pages, product_data, create_product_report
# ml_url = 'https://listado.mercadolibre.com.ar/computacion/componentes-pc/procesadores/nuevo/compra-gamer_NoIndex_True'



def main(text) -> None:
    # Driver instance creation
    driver = get_driver()

    # Search for products:
    product_list = scrape_all_pages(driver, text)

    # Get product data:
    product_data_list = product_data(driver=driver, product_list=product_list[:5])

    driver.close()

    create_product_report(product_data_list)

if __name__ == "__main__":
    
    text = input("Search: ") 
    main(text)
