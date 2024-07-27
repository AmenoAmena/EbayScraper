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

#filter_select = WebDriverWait(driver, 10).until(
#    expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[4]/div[1]/div[2]/div[2]/div[3]/div[1]/div/span/button"))
#)
#
#filter_select.click()

# Execute JavaScript to set aria-expanded to true
driver.execute_script("document.querySelector('button[aria-label=\"Sort selector. Best Match selected.\"]').setAttribute('aria-expanded', 'true')")


highest_to_lowest_filter = WebDriverWait(driver, 10).until(
    expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='s0-60-0-12-8-4-1-0-4[1]-70-39-1-content-menu']/li[5]/a"))
)

highest_to_lowest_filter.click()



