# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 14:20:23 2021

@author: kalan
"""
import requests
import bs4 as bs
import string
import json
import string

alphabet = string.ascii_lowercase

urls = []
for letter in alphabet:
    url ="http://ufcstats.com/statistics/fighters?char=%s&page=all" %letter
    urls.append(url)  
all_fighters={}

for url in urls:
    r = requests.get(url)
    soup = bs.BeautifulSoup(r.content,'lxml')
        
    for a in soup.find_all('a', href=True):
        if "fighter-details" in a['href']:
            #afighters.append(a['href'])
            
            if a['href'] not in all_fighters:
                all_fighters[a['href']] = {}
                
                all_fighters[a['href']][a['href'][36:52]] = [a.text]
            else:
                all_fighters[a['href']][a['href'][36:52]].append(a.text)


for i in all_fighters:
    for j,k in all_fighters[i].items():
        all_fighters[i][j] = ' '.join(k)


with open('ufcfighters.json','w') as file:
    file.write(str(all_fighters))