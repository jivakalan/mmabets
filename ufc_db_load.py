# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:20:26 2021

@author: kalan
"""

import sqlite3

##############################################################################       

#def fight_update():
    #for each fighter, if there are new fight IDs, then include into the dictionary, otherwise - no
    #need to update the not in ufcfightdata conditio so that it actually does a real check
    #check back for Cyril Gane on Sunday
    #before Sunday - fix not in ufcfightdata condition
    
##############################################################################       

# def db_insert():
    # #run once a month (scheduled task)
    
#     def fighter_dic_to_df()
#         fighter_id, fighter_name = [],[]
#         for i in all_fighters:
#             for j,k in all_fighters[i].items():
#                 fighter_id.append(j)
#                 fighter_name.append(k)
#         fighter_df=pd.DataFrame([fighter_id, fighter_name]).T
#         fighter_df.columns=['Fighter_ID','Fighter_Name']
        
#     fighter_dic_to_df()


#     sqliteConn = sqlite3.connect('mmabets.db')
#     c= sqliteConn.cursor()
    
#     #import data to relevant table
#     fighter_df.to_sql("fighter_dim", sqliteConn, if_exists ='append',index=False)
#     sqliteConn.commit()
        

#     #close the cursor/disconnect from db 
#     c.close()
#     sqliteConn.close()
##############################################################################




# all_fighters = get_all_fighter_pages()  #19 seconds for 3597 fighters
# #save as json
# with open('ufcfighters.json','w') as fp:
#     json.dump(all_fighters,fp)
# #get_all_fights can take 2.5 hours-only run on test data 

# ufcfightdata = get_all_fights(fighters)                
 #fighter table insert           
# db_insert()
# #PICKLE testing data with timestamp
# with open('TESTufcfightdata.pickle','wb') as handle:
#     pickle.dump(ufcfightdata,handle,protocol=pickle.HIGHEST_PROTOCOL)


##############################################################################





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


def data_cleansing(ufcfightdata):

    #delete the tables that are unneccessary
    for fighter in ufcfightdata:
        for ft_index,fightdict in ufcfightdata[fighter].items():
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                del listdf[0],listdf[1]
                
    # and clean the other two tables            
    for fighter in ufcfightdata:
        for ft_index,fightdict in ufcfightdata[fighter].items():
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                
                for cntr in range(0,len(listdf)):         
                    
                    if cntr ==0:
                        ##create a column for Rounds
                        listdf[cntr]['Round'] = list(range(1,len(listdf[cntr].columns[0])))
                        listdf[cntr].columns = ['Fighter','Knockdowns','Significant_Strikes','Significant_Strike_pct','Total_Strikes','Takedowns','Takedown_pct','Submission_Attempt','Rev','Control_Time','Round']
                    elif cntr ==1:
                        listdf[cntr]['Round'] = list(range(1,len(listdf[cntr].columns[0])))
                        del listdf[cntr]['Unnamed: 9_level_0']
                        listdf[cntr].columns  = ['Fighter','Significant_Strikes','Significant_Strike_pct','Head','Body','Leg','Distance','Clinch','Ground','Round']
     
                    else:
                        del listdf[cntr]
                        
    return ufcfightdata
            
##############################################################################

import pickle
#read in data
with open('TESTufcfightdata.pickle','rb') as handle:
    ufcfightdata= pickle.load(handle)
#cleanse the data
data_cleansing(ufcfightdata)

for fighter in ufcfightdata:
    for ft_index,fightdict in ufcfightdata[fighter].items():
        for fight, listdf in  ufcfightdata[fighter][ft_index].items():
            for df in listdf:
                pd_df_spltr(df)
                df['Fighter_ID'] =fighter
                
                
for fighter in ufcfightdata:
    sqliteConn = sqlite3.connect('mmabets.db')
    c= sqliteConn.cursor()
    
    for ft_index,fightdict in ufcfightdata[fighter].items():
        
        for fight, listdf in  ufcfightdata[fighter][ft_index].items():
            for df in listdf:
                #import data to fighter_data table
                df.to_sql("fighter_data", sqliteConn, if_exists ='append',index=False)
                sqliteConn.commit()
                     
        #close the cursor/disconnect from db 
        c.close()
        sqliteConn.close()



#IMPORT FIGHT_DIM TABLE 

get all tony fergus fight+fightids+date



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
  #  (tomorrow)
  

dates =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Aug','Nov','Dec']

fighters =[]
fighters.append('http://ufcstats.com/fighter-details/22a92d7f62195791')

ufcfightdim={}

for fighter in fighters:
    ufcfightdim[fighter[36:52]]={}
    
    r = requests.get(fighter)
    soup = bs.BeautifulSoup(r.content,'lxml')


    for p in soup.find_all('p',attrs={"class":"b-fight-details__table-text"} ):
        if any(x in p.text for x in dates):

            ufcfightdim[fighter[36:52]][p.text.strip()]={}
            
    for a in soup.find_all('a', href=True):
        if "fight-details" in a['href']:
           # print(a.text,a['href'])
            if a['href'] not in ufcfightdim and a.text !='next' and 'Matchup' not in a.text:            
                for k in ufcfightdim[fighter[36:52]]:
                    try:
                        ufcfightdim[fighter[36:52]][k] = {a['href']:a.text}
                    except ValueError:
                        pass


