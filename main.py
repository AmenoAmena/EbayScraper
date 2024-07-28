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

class Product:
    def __init__(self,name,price,link):
        self.name = name
        self.price = price
        self.link = link

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

product = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME, "s-item__wrapper"))
)

product_id = product.get_attribute("id")

#product_info = product.find_element(By.CLASS_NAME,"s-item__info")
#product_link = product_info.find_element(By.TAG_NAME,"a")
#print(product_link.get_attribute("innerHTML"))


#print(product_info.get_attribute("innerHTML"))

#product_name = product.find_element(By.CLASS_NAME,"s-item__title")
#product_name_span = product_name.find_element(By.TAG_NAME,"span").get_attribute("innerHTML")
#print(product_name_span)

#print(product.get_attribute("innerHTML"))

product_price = product.find_element(By.XPATH, f"//*[@id='{product_id}']/div/div[2]/div[3]/div[1]/div[1]/span").get_attribute("innerHTML")

price_match = re.search(r'\$[0-9,]+\.\d{2}', product_price)
if price_match:
    product_price = price_match.group()
    print("Product Price:", product_price)
else:
    print("Price not found")




#sleep(5)
#driver.quit()