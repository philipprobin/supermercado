
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from dataclasses import dataclass

@dataclass
class Product:
    name: str=None
    nutrients:list[str]=None
    price:float=None
    category:str=None


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
        time.sleep(2)

    def _format_price(self, price:str) -> float:
        return float(price.split(' ')[0].replace(',', '.'))

    def _accept_cookies(self):
        btn_cookies = self.driver.find_element(By.XPATH, "//button[@class='uc-btn uc-btn-primary']")
        btn_cookies.click()
        time.sleep(4)

    def crawl_products_and_categories(self):
        self._main_page()
        self._accept_cookies()

        # Enlarge list of products:
        catalogs = self.driver.find_elements(By.XPATH, './/div[@class="sos-category__content"]')
        for catalog in catalogs:
            btn_more_products = catalog.find_element(By.XPATH, './/div[contains(@class, "sos-category__content-button-wrapper")]//button')
            if btn_more_products.is_displayed():
                btn_more_products.click()
                time.sleep(1)

        # Category titles and Articles:
        category_titles = self.driver.find_elements(By.XPATH, './/div[@class="sos-category"]//div[@class="sos-category__content"]//h2')
        article_products_html = self.driver.find_elements(By.XPATH, './/div[@class="sos-category"]//div[@class="sos-category__content"]')
        all_prods = []

        for i, cat in enumerate(article_products_html):
            article_names = cat.find_elements(By.XPATH, './/div[contains(@class, "sos-category__content-items")]//article//a')
            for article in article_names:
                all_prods.append(Product(
                    name=article.text,
                    category=category_titles[i].get_attribute('innerHTML'),
                ))

        return all_prods




    def crawl_only_products(self):
        self._accept_cookies()

        # Enlarge list of products:
        catalogs = self.driver.find_elements(By.XPATH, './/div[@class="sos-category__content"]')
        for catalog in catalogs:
            btn_more_products = catalog.find_element(By.XPATH, './/div[contains(@class, "sos-category__content-button-wrapper")]//button')
            if btn_more_products.is_displayed():
                btn_more_products.click()
                time.sleep(1)

        article_products_html = self.driver.find_elements(By.XPATH, "//article[@class='cor-offer-renderer-tile cor-link']")

        for article_html in article_products_html:
            self.inventory.append(Product(
                name=article_html.find_element(By.XPATH, ".//a[contains(@class,'cor-offer-information__title-link')]").text,
                nutrients=[nutri.text for nutri in article_html.find_elements(By.XPATH, ".//span[contains(@class,'cor-offer-information__additional')]")],
                price=self._format_price(article_html.find_element(By.XPATH, ".//div[contains(@class,'cor-offer-price__tag-price')]").text)
            ))

        return self.inventory


if __name__ == '__main__':
    print(REWECRAWLER('https://www.rewe.de/').crawl_products_and_categories())





