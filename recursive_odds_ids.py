# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 20:49:44 2021

@author: kalan
"""

#####################################################################################################
# This file searches for all the opponents of all the opponents of fighters on bestfightodds;
# The front page only crawl only yeilded 214 IDs however by implementing tactic of navigating 
# to each fighter on the main page, and further recursively searching through their oponnents
# while updating the dictionary:
    
#takes a dictionary fighter odds web pages - started with fighter_odds.json which was
#an initial crawl of just the front page of bestfight odds and the opponents of all fighters
#on the front page

#working on feature branch
#merge with master when complete 
#"https://www.bestfightodds.com"
###################################################################################################
import requests
import bs4 as bs 
import json
import helper as h


class bestfightOddsScraper:
    def __init__(self,):
        self.bestfightOddsUrl = "https://www.bestfightodds.com"
        self.fighter_lst_address = "data\fighter_odds_2021-03-02.json"
        self.opponent ='/fighters/Israel-Adesanya-7845'
        self.cnt = 0
        self.fighter_lst=['/fighters/Israel-Adesanya-7845']
        self.prev_fiter_lst_address = ''
        
        
    def get_all_bestfightOdds_IDs(self.opponent, self.cnt, self.fighter_lst):
        
        for fighter_url in fighter_lst:
            if fighter_url == opponent:
                
                ##extract the web page for the fighter
                r = requests.get(self.bestfightOddsUrl+fighter_url)
                soup = bs.BeautifulSoup(r.content,'lxml')
                  
                #for each fighter, go through their opponents
                #each link to their opopnent contains the string "fighters" within it
                for a in soup.find_all('a', href=re.compile('fighters')):
                    
                    #filter out the fighter urls that are the fighter themselves
                    if fighter_url not in a['href']:
                        
                        #if the fighter's opponent is not already in the dictoinary
                        if a['href'] not in fighter_lst:
                                           
                            #add the ID to the new dictionary
                            fighter_lst.append(a['href'])
                              
                            #send the opponent to scrape all the IDs of their opponents
                            opponent=  a['href']
                            
                            #then recursively get the IDs of their opponents
                            get_all_bestfightOdds_IDs(opponent, cnt, fighter_lst)   
         
                            
    def update_fighters():
        #use to update the main fighterID db - run once a week or to get any new FIDs from the 
        #front page of bestfightodds
        with open(self.fighter_lst_address ,'r') as fp:
            fighter_odds_lst = json.load(fp)
        
        #pull the front page
        r = requests.get(self.bestfightOddsUrl)
        soup = bs.BeautifulSoup(r.content,'lxml')
        
        for a in soup.find_all(['span','a'], href=re.compile('fighters')):
            #if the fighter links are not in the fighter odds list
            if a['href'] not in fighter_odds_lst:        
                fighter_odds_lst.append(a['href'])
                         
        c  = str(datetime.date.today())
        
        h.save_json(self.fighter_lst_addres, fighter_lst)    
        
        # self.prev_fiter_lst_address = self.fighter_lst_address
        
        self.fighter_lst_address = "data\fighter_odds_%s.json" %c
        
    
    def get_fight_odds():
        
        fighter_odds = h.load_json(self.fighter_lst_address)
        # with open(self.fighter_lst_addres,'r') as fp:
        #     fighter_odds = json.load(fp) 
        
        #get only the difference between the latest fighter odd IDs and what's in the database
        #send that through for data scraping and creating the dfs
        
        # fighter_odds = list(fighter_odds.keys())[100:]
        # fighter_odds_test=[]
        # fighter_odds_test.append('https://www.bestfightodds.com/fighters/Tony-Ferguson-2568')   
        # fighter_odds_test.append("https://www.bestfightodds.com/fighters/Israel-Adesanya-7845")
        # fighter_odds_test.append("https://www.bestfightodds.com/fighters/Jan-Blachowicz-2371")
        
        
        finaldf = pd.DataFrame(columns=['Fighter_Name','Open','Close_range_Lower','Close_range_Upper','Event','Fighter_ID'])
        
        start = t.time()  
        for fighter_url in fighter_odds:

            dfs= pd.read_html(self.bestfightOddsUrl+fighter_url)
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
        
        stop = t.time()   
        time= stop-start 
        print('This took %s seconds' %time)  
        
        h.load_to_db(finaldf3,'fight_odd_fact')
        
        




# def get_all_bestfightOdds_IDs(opponent, cnt, fighter_lst):
    
#     for fighter_url in fighter_lst:
#         if fighter_url == opponent:
            
#             ##extract the web page for the fighter
#             r = requests.get("https://www.bestfightodds.com"+fighter_url)
#             soup = bs.BeautifulSoup(r.content,'lxml')
              
#             #for each fighter, go through their opponents
#             #each link to their opopnent contains the string "fighters" within it
#             for a in soup.find_all('a', href=re.compile('fighters')):
                
#                 #filter out the fighter urls that are the fighter themselves
#                 if fighter_url not in a['href']:
                    
#                     #if the fighter's opponent is not already in the dictoinary
#                     if a['href'] not in fighter_lst:
                        
                        
#                         #add the ID to the new dictionary
# #                        fighter_lst[a['href']] = a.text
#                         fighter_lst.append(a['href'])
                        
#                         #some checking
#                         cnt+=1
#                         print(a.text,' added #',cnt)
                        
#                         #send the opponent to scrape all the IDs of their opponents
#                         opponent=  a['href']
                        
#                         #then recursively get the IDs of their opponents
#                         get_all_bestfightOdds_IDs(opponent, cnt, fighter_lst)                   
            
#     return fighter_lst


# fighter_list= ['/fighters/Israel-Adesanya-7845']
# fighter_lst.append('/fighters/Israel-Adesanya-7845')
# cnt=0
# opponent = '/fighters/Israel-Adesanya-7845'

# get_all_bestfightOdds_IDs(opponent, cnt, fighter_lst)
# #how to terminate? count was going down for some reason 

# ##save output
# c  = str(datetime.date.today())
# with open(r'data\fighter_odds_%s.json' %c,'w') as fp:
#     json.dump(fighter_lst,fp)

# fidf = pd.DataFrame(fighter_lst, columns=['Fighter_ID'])
# h.load_to_db(fidf,'fighter_id_recursive')