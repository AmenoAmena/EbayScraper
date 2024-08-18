from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
import re
from bs4 import BeautifulSoup as bs

class Product:
    def __init__(self, name, price, link):
        self.name = name
        self.price = price
        self.link = link

    def __str__(self):
        return f"title: {self.name} || price: {self.price}"

def pagination(url, pg_number):
    base_url = url.split("&_pgn=")[0]
    return f"{base_url}&_pgn={pg_number}"

def scrape_products():
    products = []
    while True:
        products = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 's-item')]"))
        )
        number_of_products = len(products)
        products = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 's-item')]"))
        )
        if len(products) == number_of_products:
            current_url = driver.current_url
            pagination(current_url)
            break

    return products

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service('chromedriver.exe'), options=options)
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

number_of_products = 0

highest_to_lowest_filter = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='s0-60-0-12-8-4-1-0-4[1]-70-39-1-content-menu']/li[5]/a"))
)
highest_to_lowest_filter.click()

try: 
    products = scrape_products()
except Exception as e:
    print(f"Can't find products: {e}")

product_list = products[2:]

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

with open('products.csv', "w", newline='', encoding='utf-8') as product_file:
    writer = csv.writer(product_file, delimiter=',')
    writer.writerow(["Name", "Price", "Link"])
    for product_object in product_objects:
        writer.writerow([product_object.name, product_object.price, product_object.link])


class EbayScraper:
    def __init__(self,DRIVER_PATH):
        self.options = Options()
        self.options.add_argument('--headless=new')
        self.service = Service(DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get("https://www.ebay.com/")
        self.number_of_products = 0
        self.product_objects = []
    
    def scrape(self, name: str, min_price: float = None, max_price: float = None):
        self.search_bar = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='gh-ac']"))
        )
        self.search_bar.send_keys(name)

        self.submit_btn = self.driver.find_element(By.ID, "gh-btn")
        self.submit_btn.click()

        if min_price and max_price:
            self.min_inp = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "s0-60-0-12-8-0-1-2-2-8[2]-textrange-beginParamValue-textbox"))
            )

            self.max_inp = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.ID, "s0-60-0-12-8-0-1-2-2-8[2]-textrange-endParamValue-textbox"))
            )

            self.min_inp.send_keys(min_price)
            self.max_inp.send_keys(max_price)

            self.price_submit = self.driver.find_element(By.CLASS_NAME, "btn--states")
            self.price_submit.click()

        try:
            self.products = []
            while True:
                self.products = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 's-item')]"))
                )
                self.number_of_products = len(self.products)
                self.products = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 's-item')]"))
                )
                if len(self.products) == self.number_of_products:
                    break
        except Exception as e:
            print(f"Can't find products: {e} ")

        self.product_list = self.products[2:]

    def create_product(self):
        for product in self.product_list:
            self.product_title = product.find_element(By.CLASS_NAME, "s-item__title").text
            self.product_price = product.find_element(By.CLASS_NAME, "s-item__price").get_attribute("innerHTML")
            self.price_match = re.search(r'\$[0-9,]+\.\d{2}', self.product_price)
            if self.price_match:
                self.product_price = self.price_match.group()
            self.product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.product_img = product.find_element(By.TAG_NAME, "img").get_attribute("src")
            self.product_obj = EbayProduct(name=self.product_title, price=self.product_price, link=self.product_link,img_src=self.product_img)
            self.product_objects.append(self.product_obj)

    def print_objects(self):
        for product in self.product_objects:
            print(product)

    def get_products(self):
        return self.product_objects

    def quit_driver(self):
        self.driver.quit()