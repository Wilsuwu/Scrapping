import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from methods import get_href,get_prices,get_titles,get_driver


driver = get_driver()
driver.implicitly_wait(2)


done, counter = False, 1
path = f'https://www.carrefour.com.ar/norton?_q=Norton&map=ft'

#Lists
titles = []
prices = []
original_prices = []
eans = []
types = []
links = []

print("--- Scraping ---")
while not done:
    try:
        new_path = path+f"&page={counter}" if counter!=1 else path
        driver.get(new_path)
        # r = requests.get(new_path)
        # soup = BeautifulSoup(r.text, 'html.parser')

    #if soup.find_all(string="No se ha encontrado ningún producto"):
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        elements = driver.find_element(By.XPATH, '//div[@class="valtech-carrefourar-search-result-0-x-gallery flex flex-row flex-wrap items-stretch bn ph1 na4 pl9-l"]')
        
        product_list = elements.find_elements(By.XPATH,'//div[@class="valtech-carrefourar-search-result-0-x-galleryItem valtech-carrefourar-search-result-0-x-galleryItem--normal pa4"]')
        titles_f = get_titles(product_list)
        titles.append(titles_f)
        
        prices_f, original_prices_f = get_prices(product_list)
        prices.append(prices_f)
        original_prices.append(original_prices_f)
        
        links_f = get_href(product_list)
        links.append(links_f)
        print(titles, prices)
    except:
        for href in links:
            for e in href:
                driver.get(e)
                
                specs = driver.find_elements(By.TAG_NAME, 'td')
                
                ean = specs[1].get_attribute("data-specification")
                wine_type = specs[3].get_attribute("data-specification")
                
                eans.append(ean)
                types.append(wine_type)
        df = pd.DataFrame(columns=['Title','Price','Original_Price','Type','EAN'])
        
        # Lists to organize Columns content
        titles_df = []
        prices_df = []
        original_prices_df = []
        
        
        for i in titles:
            for title in i:
                titles_df.append(title)
        
        for i in prices:
            for price in i:
                prices_df.append(price)
        
        for i in original_prices:
            for price in i:
                original_prices_df.append(price)
        
        df['Title'] = titles_df
        df['Price'] = prices_df
        df['Original_Price'] = original_prices_df
        df['Type'] = types
        df['EAN'] = eans
        
        df.to_csv('Carrefour_vinos.csv')
        done = True
    counter +=1 