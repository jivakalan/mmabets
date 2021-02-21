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

#requirement- scrape once a week on Sundays after Saturday night events, and update database

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

 

##########################



def get_all_fights():
    
    ufcfightdata={}
    for fighter in uniq_afighters:
        ufcfightdata[i[36:52]]={}
        r = requests.get(i)
        soup = bs.BeautifulSoup(r.content,'lxml')
        
        cnt=0
        for a in soup.find_all('a', href=True):
            if "fight-details" in a['href']:
                if a['href'] not in ufcfightdata:
                    ufcfightdata[i[36:52]][cnt] = {}
                    ufcfightdata[i[36:52]][cnt][a['href']] = pd.read_html(a['href'])
                    cnt+=1                        
                                                   
    return ufcfightdata
          
start = t.time()
ufcfightdata = get_all_fights()                
stop = t.time()     
time= stop-start           
print('This took %s seconds' %time)
               
  
            
                
                
       
        
        
#######################################
###scrape all fight data#############
##################################
#tony ferguson
# only getting ufc stats---what is their record before their first fight in the UFC???slapm?etc
url="http://ufcstats.com/fighter-details/22a92d7f62195791"

r = requests.get(url)
soup = bs.BeautifulSoup(r.content,'lxml')

fight_details =[]
for a in soup.find_all('a', href=True):
    if "fight-details" in a['href']:
        print(a['href'])
        fight_details.append(a['href'])
        
       
        
testf=[]
testf.append("http://ufcstats.com/fighter-details/22a92d7f62195791")
        
dfs = pd.read_html("http://ufcstats.com/fight-details/b7b867eb3c3cf163")





for a in soup.find_all('p',href=True):
    if p['href'] = fighter_detail:
        #scrape the relevant metrics? or use pandas

