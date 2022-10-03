# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 12:02:06 2021

@author: kalan
"""

# =============================================================================
# This file attempts to create a foreign_key for the fighter_dim table                
# such data from bestfightodds and ufcstats can be joined
# 
# for example: fighter_ID   from bestfightodds Israel-Adesanya-7845
#               fighter_name from bestfightodds Israel Adesanya
# 
#               fighter_ID   from ufcstats      1338e2c7480bdf9e
#               fighter_name from ufcstats      Israel Adesanya The Last Stylebender
# =============================================================================

#testing fuzzy wuzzy match on strings
#fuzz.partial_ratio("Israel Adesanya The Last Stylebender", "Tony Ferguson")

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import helper as h

###performance concern, re-tool if coming back to this 

def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    return df_1
;

#get the Fighter ODD Ids
fighter_odds = h.json_load("data\fighter_odds.json")

df1= pd.DataFrame.from_dict(fighter_odds.items())
df1.columns =['Fighter_ID','Fighter_Name']

#get Fighter DIM Ids
con = sqlite3.connect('mmabets.db')
df2 = pd.read_sql("select * from fighter_dim",con)
con.close()


df_1 = fuzzy_merge(df2, df1, 'Fighter_Name','Fighter_Name',threshold=90, limit=2)


##save to csv
df_1.to_csv('df_1.csv')
