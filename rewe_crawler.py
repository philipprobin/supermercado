
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    nutrients:list[str]
    price:float


class REWECRAWLER():
    def __init__(
            self,
            url:str
        ):

        self.query = url
        #options.add_argument('proxy-server=106.122.8.54:3128')
        self.driver = uc.Chrome(options=webdriver.ChromeOptions())
        self.driver.get(self.query)
        self.inventory = []


    def _main_page(self):
        self.driver.find_element(By.XPATH, "//span[@class='ths-funnel-tab__title']").click()
        time.sleep(3)

    def _format_price(self, price:str) -> float:
        return float(price.split(' ')[0].replace(',', '.'))

    def more_offers_button(self):
        self._main_page()
        for btn in self.driver.find_elements(By.XPATH, ".//button[contains(@class, 'sos-category__content-button')]"):
            btn.click()

    def crawl_products(self):
        self._main_page()
        article_products_html = self.driver.find_elements(By.XPATH, "//article[@class='cor-offer-renderer-tile cor-link']")
        for article_html in article_products_html:
            self.inventory.append(Product(
                name=article_html.find_element(By.XPATH, ".//a[contains(@class,'cor-offer-information__title-link')]").text,
                nutrients=[nutri.text for nutri in article_html.find_elements(By.XPATH, ".//span[contains(@class,'cor-offer-information__additional')]")],
                price=self._format_price(article_html.find_element(By.XPATH, ".//div[contains(@class,'cor-offer-price__tag-price')]").text)
            ))

        return self.inventory


if __name__ == '__main__':
    REWECRAWLER('https://www.rewe.de/').more_offers_button()


# search = driver.find_element(By.NAME, "query")
# search.send_keys("APPEL Heringsfilets")
# search.send_keys(Keys.RETURN)
#
# time.sleep(1)
#
# product = driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]')
# product.send_keys('lola')
# product.send_keys(Keys.RETURN)




