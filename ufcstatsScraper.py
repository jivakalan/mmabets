import requests
import bs4 as bs
import string
import pandas as pd
import time as t  
import json


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

start = t.time()
all_fighters = get_all_fighter_pages()
#need to run get_all_fighters infrequently, only when new fighters are signed and have a fight in UFC
#how often does that happen...can probably schedule it once a month 
stop = t.time()
time= stop-start 
print('This took %s seconds' %time)   #19 seconds for 3597 fighters

with open('ufcfighters.json','w') as fp:
    json.dump(all_fighters,fp)
    

##########################

with open('ufcfighters.json','r') as fp:
    all_fighters = json.load(fp)

def get_all_fights(fighters):
    
    ufcfightdata={}
    for fighter in fighters:
        ufcfightdata[fighter[36:52]]={}
        r = requests.get(fighter)
        soup = bs.BeautifulSoup(r.content,'lxml')
        
        cnt=0
        for a in soup.find_all('a', href=True):
            if "fight-details" in a['href']:
                if a['href'] not in ufcfightdata and a.text !='next' and 'Matchup' not in a.text:
                    ufcfightdata[fighter[36:52]][cnt] = {}
                    ufcfightdata[fighter[36:52]][cnt][a['href']] = pd.read_html(a['href'])
                    cnt+=1                        
                                                   
    return ufcfightdata
          

uniq_afighters=list(all_fighters.keys())
fighters =list(uniq_afighters)[0:2]

start = t.time()
ufcfightdata = get_all_fights(fighters)                
stop = t.time()     
time= stop-start           
print('This took %s seconds' %time)


##########################        

ufcfightdata={}
for fighter in fighters:
    ufcfightdata[fighter[36:52]]={}
    r = requests.get(fighter)
    soup = bs.BeautifulSoup(r.content,'lxml')
    
    cnt=0
    for a in soup.find_all('a', href=True):
        if "fight-details" in a['href']:
            if a['href'] not in ufcfightdata:
                print(a['href'])
                ufcfightdata[fighter[36:52]][cnt] = {}
                try:
                    ufcfightdata[fighter[36:52]][cnt][a['href']] = pd.read_html(a['href'])
                except ValueError:
                    pass
                cnt+=1      
                
#TO DO

#2 def update() --delta update - get ready to test for JairzinhoRozenstruik CirylGane
    #Ciryl Gane -787bb1f087ccff8a
    #Rozenstriuk-2cd428e9606856fd
    ## next match id 4a704dae3091adaf
    ## match preview id 4a704dae3091adaf
    ##what does the fight ID become for this fight? 
  #2h
  
#3 read through 4 pandas DFs per fighter in the right manner and insert to table in sqlDB 
    #test for Ferguson - read to db table - stats by event insert 
    #"http://ufcstats.com/fighter-details/22a92d7f62195791"
  #2h
  
#4 full run
    #run on GCP rather than local machine for 12 hours? 
    #1hr
        
