import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import requests

class NutritionCrawler:

    def firebase_instance(self):
        path = 'supermercado-371012-firebase-adminsdk-lu3fc-48a8c3583d.json'
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)

        firebase_admin.get_app()

        db = firestore.client()
        return db

    def crawl_groceries(self, page):
        # Send the request and get the response
        response = requests.get(page)

        # Parse the response content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with the class 'c-teaser__link'
        recipe_elements = soup.find_all(class_='list-group')[0]
        # print(recipe_elements)

        grocery_list = arr = np.empty((1, 2))
        print(grocery_list)
        # Print the text and href attributes of each element
        
        for html in recipe_elements:
            html = str(html)
            soup = BeautifulSoup(html, 'html.parser')
            
            # find the img tag
            a_tag = soup.find('a')
            if a_tag:
                link = a_tag.get('href')
                text = a_tag.text
                # print(link)
                # print(text)
                text_list = text.split()
                if "roh" in text_list or len(text_list) == 1:
                    # text without roh
                    result = ""
                    for word in text_list:
                        if word == "roh":
                            break
                        result += word + ' '
                    if result not in grocery_list[:,0]:
                    # kicks off double appearences
                        grocery_list = np.concatenate((grocery_list, np.array([[result, link]])), axis=0)
                    
        return grocery_list[1:]

    def get_nutrition(self, food, page):
        # Send the request and get the response
        response = requests.get(page)

        # Parse the response content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements with the class 'c-teaser__link'
        table_element = soup.find_all(class_='table table-condensed table-striped table-bordered')[0]

        rows = table_element.find_all('tr')

        d = {} 
        calories = {}
        protein = {}
        fats = {}
        carbs = {}
        # Iterate over all rows
        for row in rows:
            # Find the cells in each row
            cells = row.find_all('td')
            if len(cells) > 0:
                # Get the text of the first cell
                inhalt = cells[0].text
                if inhalt == 'Eiweiß':
                    protein["amount"] = cells[1].text
                    protein["unit"] = cells[2].text
                    d["protein"] = protein
                
                if inhalt == 'Kilokalorien':
                    calories["amount"] = cells[1].text
                    calories["unit"] = cells[2].text
                    d["calories"] = calories
        
                if inhalt == 'Fett':
                    fats["amount"] = cells[1].text
                    fats["unit"] = cells[2].text
                    d["fats"] = fats
        
                if inhalt == 'Kohlenhydrate':
                    carbs["amount"] = cells[1].text
                    carbs["unit"] = cells[2].text
                    d["carbs"] = carbs
        
        
        return d

    def write_recipe(self, db, food, nutrition_dict):
        db.collection(u'groceries').document(u'fruits').collection(u'loose').document(food).set(nutrition_dict)

def main():
    nc = NutritionCrawler()
    grocery_list = nc.crawl_groceries("https://www.ernaehrung.de/lebensmittel/de/inhaltsstoffe-6-Fruechte,-Obst-und--Erzeugnisse.php")
    db = nc.firebase_instance()
    for row in grocery_list:

        food = row[0]
        print(food)
        nutrition_dict = nc.get_nutrition(food, row[1])
        # nc.write_recipe(db, food, nutrition_dict)


if __name__ == "__main__":
    main()