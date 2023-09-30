# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:27:41 2021

@author: kalan
"""
from extract.ufcstatsScraper import get_all_fighter_pages,get_all_fights
import bestfightoddsScraper as b
from scratches import janitor_ufcfightdata as u

###########################
### Scrape fighter data ###
###########################
#get all the fighter pages and save json file
all_fighters = get_all_fighter_pages()  #19 seconds for 3597 fighters


#get_all_fights data and save as pickle file
ufcfightdata = get_all_fights(all_fighters)                
         
#get fighter odd dim as save json file
b.get_BestfightoddsFighters()



##############################
## Update database tables ####
##############################
#udpate fighter_dim
u.db_insert_fighter_dim(all_fighters)

#clean data
u.data_cleansing(ufcfightdata)

#more data cleaning and update fighter_round_fact and fight_area_round_fact
u.data_cleansing_2()

#update fight_date_dim and fight_id_dim
u.get_fite_dates_results()

#update fight_outcome_dim
u.get_fight_end_times()

#update fight_odd_fact
b.get_fight_odds()





