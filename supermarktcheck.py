import requests
import re
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from bs4 import BeautifulSoup

class Supermarktcheck:

    def firestore_instance():
        # create firestore instance with credits
        path = 'supermercado-371012-firebase-adminsdk-lu3fc-48a8c3583d.json'
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)

        firebase_admin.get_app()

        db = firestore.client()
        return db

    def crawl_categories(self, page):
        # Send the request and get the response
        root_link = "https://www.supermarktcheck.de"
        response = requests.get(page)

        # Parse the response content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Find all elements with the class
            sub_categories = soup.find_all(class_='tabs-scroll categories-list-container')[0]

            catergory_list = np.empty((1, 2))
            
            # find sub categories with respective links
            links_and_titles = [(li.a["href"], re.sub(r"\s+\(\d+\)", "", li.a.text.strip())) for li in sub_categories.select("li")]

            # add to list
            for link, title in links_and_titles:
                catergory_list = np.concatenate((catergory_list, np.array([[title, root_link + link]])), axis=0)

            # random first value
            return catergory_list[1:] 
        except IndexError:
            return None

    def crawl_item_list(self, page):
        root_link = "https://www.supermarktcheck.de"
        # Send the request and get the response
        response = requests.get(page)

        # Parse the response content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # find list of products
        all_items = soup.find_all(class_='row supermarketListElement productListElement')

        item_list = arr = np.empty((1, 2))

        # select every product
        for item in all_items:

            # get link and title and other information
            links_and_titles = [(a["href"], a.text.strip()) for a in item.select("a")]
            
            # append to list
            for link, title in links_and_titles:
                item_list = np.concatenate((item_list, np.array([[title, root_link +  link]])), axis=0)

        # first element is random
        item_list = item_list[1:]
        # every 6th element contains the relevent data, starting from the second
        return item_list[1::6]


    def crawl_item(self, page):
        response = requests.get(page)

        # Parse the response content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        print(page)

        # Find class with prices
        try:
            prices_class = soup.find_all(class_='details-fact')[0]
            price_elements = prices_class.find_all("span", class_="label")
        except:
            pass
        product_info_dict = {}

        try:
            price = price_elements[0].find_next('strong').text
            price_per_kg = price_elements[1].next_sibling[1:-1]
            product_info_dict["price"] = price
            product_info_dict["price_per_kg"] = price_per_kg
        except:
            pass

        try:
            # Find class with calories
            calories_class = soup.find_all(class_='details-fact')[1]
            calories_elements = calories_class.find_all("span", class_="label")
            calories = calories_elements[0].find_next('strong').text.split("/")[0].rstrip()
            product_info_dict["calories"] = calories
        except: 
            pass
        
        return product_info_dict
    
    def recursive_tree_building(self, tree, node_link, node_name):
        
        print(node_link)
        sub_categories = self.crawl_categories(node_link)
        # are there any more sub-categories?
        if sub_categories is not None:
            for category in sub_categories:
                name = category[0] 
                print(name)
                link = category[1]
                tree[node_name] = self.recursive_tree_building( tree, link, name)
        
        else:
            # leaf reached -> add items
            node_dict = {}
            item_list = self.crawl_item_list( node_link)
            for item in item_list:
                name = item[0]
                link = item[1]
                node_dict[name] = self.crawl_item( link)
            return node_dict
        return tree

def main():
    root_link = "https://www.supermarktcheck.de"
    start_link = "/backwaren/produkte/"
    ### todo: find all starting links
    sm = Supermarktcheck()
    tree = sm.recursive_tree_building({},root_link + start_link, "Backwaren")
    print(tree)


if __name__ == "__main__":
    main()