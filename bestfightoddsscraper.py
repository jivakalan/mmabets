# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:16:05 2021

@author: kalan
"""

from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.bestfightodds.com")
                    
soup=BeautifulSoup(page.content, 'lxml')
print(soup.prettify())





aa=soup.find('table', attrs={'class':'odds-table'})