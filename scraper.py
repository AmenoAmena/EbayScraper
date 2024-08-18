from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import re

class Product:
    def __init__(self, name, price, link):
        self.name = name
        self.price = price
        self.link = link

    def __str__(self):
        return f"title: {self.name} || price: {self.price}"

class Backend:
    def __init__(self):
        self.options = Options()
        self.service = Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get("https://www.ebay.com/")
        self.number_of_products = 0
        self.product_objects = []

    def pagination(self, url, pg_number):
        self.base_url = url.split("&_pgn=")[0]
        self.pagination_url = f"{self.base_url}&_pgn={pg_number}"
        return self.pagination_url

                
    def get_products_on_page(self):
        try:
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
            self.products = self.products[2:]   
        except Exception as e:
            print(f"Can't find products: {e}")
            return []

    def scrape(self, name):
        self.search_bar = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='gh-ac']"))
        )
        self.search_bar.send_keys(name)

        self.submit_btn = self.driver.find_element(By.ID, "gh-btn")
        self.submit_btn.click()

        self.driver.execute_script("document.querySelector('button[aria-label=\"Sort selector. Best Match selected.\"]').setAttribute('aria-expanded', 'true')")

        self.highest_to_lowest_filter = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='s0-60-0-12-8-4-1-0-4[1]-70-39-1-content-menu']/li[5]/a"))
        )
        self.highest_to_lowest_filter.click()

        self.base_url = self.driver.current_url

        
        for page in range(1, 5):  
            if page > 1:
                self.driver.get(self.pagination(self.base_url, page))
                sleep(2)  
            products = self.get_products_on_page()
            self.create_product(products)
            sleep(2)  

    def create_product(self, products):
        for product in self.products:
            try:
                product_title = product.find_element(By.CLASS_NAME, "s-item__title").text
                product_price = product.find_element(By.CLASS_NAME, "s-item__price").get_attribute("innerHTML")
                price_match = re.search(r'\$[0-9,]+\.\d{2}', product_price)
                if price_match:
                    product_price = price_match.group()
                product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
                product_obj = Product(name=product_title, price=product_price, link=product_link)
                self.product_objects.append(product_obj)
            except Exception as e:
                print(f"Error processing product: {e}")

    def print_objects(self):
        for product in self.product_objects:
            print(product)

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Link'])
            for product in self.product_objects:
                writer.writerow([product.name, product.price, product.link])

    def quit_driver(self):
        self.driver.quit()

    def main(self):
        self.scrape("laptop")
        self.save_to_csv('products.csv')
        self.quit_driver()

if __name__ == "__main__":
    scraper = EbayScraper()
    scraper.main()
