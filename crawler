import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


class Penny():
    
    def dataframe(self):
        # Create test DataFrame
        data = {'ProduktID': [0],
                'Tag': ['montag'],
                'Sektion': ['ab-montag-obst-und-gemuese'],
                'Preis_Old': [15.99],
                'Preis_New': [9.99],
                'Name': ['Test'],
                'Period': '10.01.-17.01.'}
        df = pd.DataFrame(data)
        
        return df


    """def selenium():
        '''
        Python Selenium Safari Example
        '''

        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        import os

        # path to selenium server standalone jar, downloaded here:
        # http://docs.seleniumhq.org/download/
        # or a direct url:
        # http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar
        os.environ["SELENIUM_SERVER_JAR"] = "selenium-server-standalone-2.41.0.jar"
        # note: I've put this jar file in the same folder as this python file

        browser = webdriver.Safari()

        # makes the browser wait if it can't find an element
        browser.implicitly_wait(10)

        browser.get("http://google.com/")

        search_input = browser.find_element_by_css_selector("#gbqfq")
        search_input.send_keys("python SELENIUM_SERVER_JAR turn logging off")
        search_input.send_keys(Keys.RETURN)

        raw_input("Press Enter to close...")

        browser.quit()


    def penny_filialen():

        nutz selenium um alle filialen links zu kriegen und in eine liste zu speichern
        
    """

        
    def crawl_produkte(self,soup, df):
        """
        Methode die alle Produkte einer Penny Filiale crawlt
        """

        i = 0
        for date in soup.find_all('div', {"class": "category-menu__header-week active"}):
            period = date.text

        #Ab wann das Angebot gilt
        for tag in soup.find_all('div', {"class": "js-category-section"}):
            day = tag.get('id')

            #Für jede Sektion 
            for section in tag.find_all('section', {"class": "page-sector page-sector--above-prev page-sector--spacing-below-xxl t-bg--wild-sand js-category-section"}):
                sec = section.get('id')

                #für jedes Produkt
                for li in section.find_all('li', {"class": "tile-list__item"}):
                    i += 1

                    #für beide Preise in der bubble
                    for div in li.findAll('div', {"class": "bubble__wrap"}):
                        a = True

                        for div2 in div.findAll('div', {"class": "bubble__small-value"}):
                            a = False
                            for span2 in div2.findAll('span', {'class': 'value ellipsis'}):
                                preis = span2.text

                        #google class equals exactly class name wegen ellipsis und 
                        for span in div.findAll('span', {'class': 'ellipsis'}):
                            #nur if a =False reicht?
                            if(a):
                                preis = span.text
                            else:
                                preis2 = span.text

                    #Namen der Produkte
                    for a in li.findAll('a', {'class': 'tile__link--cover'}):
                        name = a.text
                    df.loc[i] = [i,day,sec,preis,preis2,name,period]

        #df['Preis_New'] = df['Preis_Old'].map({'': df['Preis_Old']})
        #df.Preis_Old = df.Preis_Old.astype('int64')
        #df.Preis_New = df.Preis_New.astype('int64')
        #df['Rabatt'] = df.Preis_Old / df.Preis_New
        df['Run_date'] = datetime.today().strftime('%Y-%m-%d')
        df['Weeknumber'] = datetime.today().isocalendar().week

        return df

    def transformation(self, df):
        days = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
        i = 1
        for day in days:
            df.Tag = df.Tag.apply(lambda x: str(i) if str(day) in x else x)
            i += 1

        d = str(datetime.now().year) + '-W' + str(datetime.today().isocalendar().week)
        r = datetime.strptime(d + '-1', "%Y-W%W-%w")
        df['A'] = r

        df['Tag'] = df['Tag'].astype(int) - 1
        df['Tag'] = pd.to_timedelta(df['Tag'], 'd')
        df['from'] = df.A + df.Tag 
        df['until'] = datetime.fromisocalendar(datetime.now().year, datetime.today().isocalendar().week, 6)
        df = df.drop(['Tag', 'Period', 'Weeknumber', 'A'], axis=1)

        return df

    def run(self):
        link = "https://www.penny.de/angebote/15A-10"
        page = requests.get(link)
        soup = BeautifulSoup(page.content)
        
        df = self.dataframe()
        df = self.crawl_produkte(soup,df)
        df = self.transformation(df)
        return df
