# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:11:22 2021

@author: kalan
"""
import pickle
import json
import sqlite3

def save_pickle(filename, yourdict):
    #filename must be a string
    #yourdict is a dictionary
    with open(filename,'w') as fp:
        json.dump(yourdict,fp)

def load_pickle(filename):
    with open(filename,'rb') as handle:
        yourdict= pickle.load(handle)
    return yourdict

def load_to_db(ufcdf,tablename):
    #load a pandas table to the mmabets db 
    #specify the pandas df and the tablename 

    sqliteConn = sqlite3.connect('mmabets.db')
    c= sqliteConn.cursor()
    
                    
    #import data to fighter_data table
    ufcdf.to_sql(tablename, sqliteConn, if_exists ='replace',index=False)
    sqliteConn.commit()

    #close the cursor/disconnect from db 
    c.close()
    sqliteConn.close()
    
    
#define function to split up table data to represent just one fighter
def pd_df_spltr(df):
        
    for column in df.columns:
        
        if column =='Fighter':
            continue #don't split fighter name 
        elif column =='Round':
            continue
        else:
            df[['%s_0' %column,'%s_1' %column]] = df[column].str.split("  ", expand=True)
            
    return df