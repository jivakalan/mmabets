import requests
import bs4 as bs
import string
import pandas as pd
import time as t  
import json
#import sqlite3
#import pickle
import helper
# import os 
import datetime

# os.chdir(r'C:\\Users\\kalan\\PycharmProjects\\mmabets')
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
    
    c  = str(datetime.date.today())

    ##all fighters in UFC and IDs
    with open(r'data\ufcfighters.json_%s' %c,'w') as fp:
    json.dump(all_fighters,fp)
    
    return all_fighters

##############################################################################
def get_all_fights():
    c  = str(datetime.date.today())
    with open(r'Data/ufcfighters.json', 'r') as fp:
        fighters = json.load(fp)

    
    #fighters =list(fighters.keys())[0:10]
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
                     
        if fighter_count%100 ==0:
            print(fighter_count,'fighters have been processed', t.time()-start,'seconds have elapsed')
        
    
    stop = t.time()   
    time= stop-start 
    print('This took %s seconds' %time)  
    print('pickling...')
    
    helper.save_pickle(r'data\ufcfightdata_%s.pickle' %c,ufcfightdata)
    
    # with open('ufcfightdata.pickle','wb') as handle:
        # pickle.dump(ufcfightdata,handle,protocol=pickle.HIGHEST_PROTOCOL)  
    print('pickled like a briny cucumber')          
                 
    return ufcfightdata     

##############################################################################


    

