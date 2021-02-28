# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:16:05 2021

@author: kalan
"""

import requests
import bs4 as bs
import pandas as pd
import re
from helper import load_to_db, save_pickle

import datetime

def get_BestfightoddsFighters():
    
    url ='https://www.bestfightodds.com'
    r = requests.get(url)
    soup = bs.BeautifulSoup(r.content,'lxml')
    
    fighter_odds ={}
    for a in soup.find_all(['span','a'], href=re.compile('fighters')):
        if "https://www.bestfightodds.com"+ a['href'] not in fighter_odds:        
            fighter_odds["https://www.bestfightodds.com"+ a['href']]= a.text

    #add_timestamp
    #add filter on ufc fighters only
    #save fighters 
    c  = str(datetime.date.today())
    save_pickle('fighter_odds_%s.json' %c,fighter_odds)

    return fighter_odds

##############################################################################

#def get_fightodds
def get_fight_odds():
    
    fighter_odds_test=[]
    fighter_odds_test.append('https://www.bestfightodds.com/fighters/Tony-Ferguson-2568')   
    fighter_odds_test.append("https://www.bestfightodds.com/fighters/Israel-Adesanya-7845")
    fighter_odds_test.append("https://www.bestfightodds.com/fighters/Jan-Blachowicz-2371")
    
    # for fighter_url in fighter_odds_test:
    
    finaldf = pd.DataFrame(columns=['Fighter_Name','Open','Close_range_Lower','Close_range_Upper','Event','Fighter_ID'])
    
    for fighter_url in fighter_odds_test:
        
        dfs= pd.read_html(fighter_url)
        df=dfs[0]
        df.columns =['Fighter_Name','Open','Close_range_Lower','Remove','Close_range_Upper','Remove1','Remove2','Event']
        df = df[df.index %3 !=0]
        df = df.drop(columns=["Remove","Remove1","Remove2"])
        df['Fighter_ID']= fighter_url[39:]
        finaldf= finaldf.append(df)
    
    finaldf=finaldf.reset_index(drop=True)
    
    finaldf1 = finaldf[finaldf.index%2==0]
    finaldf2 = finaldf[finaldf.index%2!=0]
    finaldf1=finaldf1.reset_index(drop=True)
    finaldf2=finaldf2.reset_index(drop=True)
    finaldf1.columns=['Fighter_Name0','Open0','Close_range_Lower0','Close_range_Upper0','Event_Name','Fighter_Id_0']
    finaldf2.columns=['Fighter_Name1','Open1','Close_range_Lower1','Close_range_Upper1','Event_Date','Fighter_Id_1']
    
    finaldf3= finaldf1.join(finaldf2)
    
    
    load_to_db(finaldf3,'fight_odd_fact')
    

##############################################################################

            