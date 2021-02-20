# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:30:58 2021

@author: kalan
"""

import requests
import bs4 as bs
import string
import pandas as pd
import time as t  


def get_all_fighter_pages():
    alphabet = string.ascii_lowercase
 
    urls = []
    for letter in alphabet:
        url ="http://ufcstats.com/statistics/fighters?char=%s&page=all" %letter
        urls.append(url)
    
 
    
    afighters=[]
    for url in urls:
        r = requests.get(url)
        soup = bs.BeautifulSoup(r.content,'lxml')
            
        for a in soup.find_all('a', href=True):
            if "fighter-details" in a['href']:
                afighters.append(a['href'])
    
    return set(afighters)

start = t.time()
uniq_afighters = get_all_fighter_pages()
stop = t.time()
time= stop-start 
print('This took %s seconds' %time)
###############################



r = requests.get(url)
soup = bs.BeautifulSoup(r.content,'lxml')

dfs = pd.read_html("https://www.bestfightodds.com")

dfs = pd.read_html("http://ufcstats.com/fighter-details/22a92d7f62195791")
dfs[3]
    