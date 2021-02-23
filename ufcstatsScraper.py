import requests
import bs4 as bs
import string
import pandas as pd
import time as t  
import json
#import sqlite3

##############################################################################
def get_all_fighter_pages():
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
    # for i in all_fighters:
    #     all_fighters[i] = ' '.join(all_fighters[i])
        
    return all_fighters
##############################################################################
def get_all_fights():
    
    with open('ufcfighters.json','r') as fp:
        all_fighters = json.load(fp)
    
    fighters =list(all_fighters.keys())[0:100]
    fighter_count=0
    ufcfightdata={}
    
    start = t.time()
    
    for fighter in fighters:
        ufcfightdata[fighter[36:52]]={}
        r = requests.get(fighter)
        soup = bs.BeautifulSoup(r.content,'lxml')
        fighter_count +=1
        cnt=0
        for a in soup.find_all('a', href=True):
            if "fight-details" in a['href']:
                if a['href'] not in ufcfightdata and a.text !='next' and 'Matchup' not in a.text:
                    ufcfightdata[fighter[36:52]][cnt] = {}
                    try:
                        ufcfightdata[fighter[36:52]][cnt][a['href']] = pd.read_html(a['href'])
                    except ValueError:
                        pass
                    cnt+=1   
                     
        if fighter_count%5 ==0:
            print(fighter_count,'fighters have been processed')
        
    
    stop = t.time()   
    time= stop-start 
    print('This took %s seconds' %time)  
                                     
    return ufcfightdata     


