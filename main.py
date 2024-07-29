from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
import re
from bs4 import BeautifulSoup as bs


class Product:
    def __init__(self,name,price,link):
        self.name = name
        self.price = price
        self.link = link

    def __str__(self):
        return f"title: {self.name} || price: {self.price}"


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.ebay.com/")

driver.maximize_window()

product_to_buy = ' '.join(sys.argv[1:])

search_bar = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='gh-ac']"))
)
search_bar.send_keys(product_to_buy)

submit_btn = driver.find_element(By.ID, "gh-btn")
submit_btn.click()

driver.execute_script("document.querySelector('button[aria-label=\"Sort selector. Best Match selected.\"]').setAttribute('aria-expanded', 'true')")


highest_to_lowest_filter = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='s0-60-0-12-8-4-1-0-4[1]-70-39-1-content-menu']/li[5]/a"))
)
highest_to_lowest_filter.click()

products = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 's-item')]"))
)

#First 2 skipped because ebay made filler 2 products.if you want to increase of product number make the 12 higher
product_list = products[2:12]

product_objects = []

for product in product_list:
    product_title = product.find_element(By.CLASS_NAME, "s-item__title").text
    product_price = product.find_element(By.CLASS_NAME, "s-item__price").get_attribute("innerHTML")
    price_match = re.search(r'\$[0-9,]+\.\d{2}', product_price)
    if price_match:
        product_price = price_match.group()
    product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
    product_obj = Product(name=product_title, price=product_price, link=product_link)
    product_objects.append(product_obj)

with open('products.csv', "w",newline='') as product_file:
    writer = csv.writer(product_file,delimiter=',')
    writer.writerow(["Name", "Price", "Link"])
    for product_object in product_objects:
        writer.writerow([product_object.name, product_object.price, product_object.link])


sleep(5)
driver.quit()
