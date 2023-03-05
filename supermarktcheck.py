import requests
import re
import firebase_admin
from firebase_admin import credentials, firestore
import json
import numpy as np
from bs4 import BeautifulSoup

class Supermarktcheck:

    def firestore_instance(self):
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

        try:
            # Find class supermarkets
            supermarket_class = soup.find_all(class_='sources')[0]
            strong_elements = supermarket_class.find_all('a')
            product_info_dict["supermarkets"] = []
            accepted_markets = ["Rewe", "Netto Marken-Discount", "Lidl", "Kaufland", "Penny-Markt", "Norma", "EDEKA", "Aldi Nord", "Aldu Süd"]
            for element in strong_elements:
                market = element.text
                if market in accepted_markets:
                    product_info_dict["supermarkets"].append(market)
        except: 
            pass
        
        return product_info_dict
    
    
    def create_db_ref(self, branches):
        global db
        db_ref = db.collection(u'supermarktcheck')
        # replace /
        branches = [s.replace("/", "&") for s in branches]
        print(branches)
        # append branches
        for branch in branches:
            # alternating cols and docs
            if isinstance(db_ref, firestore.CollectionReference):
                db_ref = db_ref.document(branch)
            else:
                db_ref = db_ref.collection(branch)
        # last one must be collection to set values
        # if not set last col to name of previous document
        if isinstance(db_ref, firestore.DocumentReference):
            db_ref = db_ref.collection(branches[-1])
        
        return db_ref
    
    
    def recursive_tree_building(self, tree, node_link, node_name):
        sub_categories = self.crawl_categories(node_link)

        # are there any more sub-categories?
        if sub_categories is not None:
        
            for category in sub_categories:
                name = category[0] 
                link = category[1]
                print(name)
                # creating branch
                tree_branch.append(name)
                self.recursive_tree_building(tree, link, name)
                # when all added remove branch
                tree_branch.pop()
        
        else:
            # leaf reached -> add items
            product_properties = {}
            item_list = self.crawl_item_list(node_link)
            db_doc = self.create_db_ref(tree_branch)
            
            for item in item_list:
                name = item[0] # product name
                link = item[1] # link
                print(name)
                product_properties[name] = self.crawl_item( link )
                # make sure docs have no /
                doc_name = name.replace("/", "-")
                # upload leaf
                db_doc.document(doc_name).set(product_properties[name])

sm = Supermarktcheck()
db = sm.firestore_instance()
tree_branch = []

def main():
    root_link = "https://www.supermarktcheck.de"
    done = ["/nahrungsmittel/produkte/","/fleisch-wurst-und-ersatz/produkte/", "/molkereiprodukte-und-ersatz/produkte/"]
    start_link = [  "/muesli-konfituere-kaffee/produkte/", "/frische-lebensmittel-aus-der-kuehlung/produkte/", "/tiefkuehlkost/produkte/", "/konserven/produkte/"]
    neglectable = ["/suesswaren-knabberartikel/produkte/" , "/backwaren/produkte/", "/getraenke/produkte/", "/saucen-suppen-gewuerze/produkte/"]
    
    for link in start_link:
        category = link.split("/")[1]
        print(category)
        tree_branch.append(category)
        sm = Supermarktcheck()
        sm.recursive_tree_building({},root_link + link, category)
        # remove start link
        tree_branch.pop()

if __name__ == "__main__":
    main()