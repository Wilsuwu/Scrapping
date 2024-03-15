import pandas as pd
from selenium.webdriver.common.by import By
from methods import click, get_driver, get_prices, get_titles 




driver = get_driver()
# Abrir la pagina de Cervezas
driver.get('https://www.booz.cl/catalogo/cervezas')



### Comienzo del Scraping: ###

div_main = "main"

main = driver.find_element(By.CLASS_NAME, div_main)
modal = main.find_element(By.XPATH, '//div[@data-testid="modalContainer"]')
boton = modal.find_element(By.XPATH, '//button[@class="Modal_Modal__CloseButton__fXh7X my-4"]')

### Quitamos la ventana Modal
click(driver, boton)

### Definimos nuestras listas de elementos:
# Productos:
product_list= main.find_elements(By.XPATH,'//div[@class="Card_card-details__name__hEqPR my-5 mx-auto Card_crop-text__52awQ"]')
# Scrapeamos Productos:
titles = get_titles(product_list)

# Precios:
price_list = main.find_elements(By.XPATH, '//div[@class="card-details__details"]')

# Scrapeamos Precios:
prices, discount_prices = get_prices(price_list)

df = pd.DataFrame(columns=['Product','Price'])
df['Product'] = titles
df['Price'] = prices


df.to_csv('cervezas.csv', index=False)