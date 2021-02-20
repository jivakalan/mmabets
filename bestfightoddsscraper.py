# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:16:05 2021

@author: kalan
"""

import requests
import bs4 as bs
import string
import pandas as pd

alphabet = string.ascii_lowercase



for letter in alphabet:
    url ="http://ufcstats.com/statistics/fighters?char=%s&page=all" %letter
    print(url)

r = requests.get(url)
soup = bs.BeautifulSoup(r.content,'lxml')

afighters=[]
for a in soup.find_all('a', href=True):
    if "fighter-details" in a['href']:
        print(a['href'])
        afighters.append(a['href'])
uniq_afighters = set(afighters)
    


dfs = pd.read_html("https://www.bestfightodds.com")

