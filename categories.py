
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
driver.get("https://www.supermarktcheck.de/lebensmittel/")
# assert "Python" in driver.title
search = driver.find_element(By.NAME, "query")
search.send_keys("APPEL Heringsfilets")
search.send_keys(Keys.RETURN)

time.sleep(1)

product = driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]')
product.send_keys('lola')
product.send_keys(Keys.RETURN)


# assert "No results found." not in driver.page_source
