# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:20:26 2021

@author: kalan
"""

import sqlite3
from helper import load_to_db, load_pickle, pd_df_spltr

##############################################################################       

#def fight_update():
    # TBD Sunday, Feb 28   
        # test JairzinhoRozenstruik-2cd428e9606856fd  CirylGane-787bb1f087ccff8a
        # fix not in ufcfightdata condition
        # next match id 4a704dae3091adaf; does the fight id change? 
        # match preview id 4a704dae3091adaf#
        #estimate -2hrs

    
##############################################################################       

def get_fight_end_times:
    ##still needs work ; 2 fighters-  fix loop input
    
    fight_detail_im=pd.DataFrame()
    for fighter in fighters:
        
        
        for fight_url in fights:
            fight_details_df = pd.DataFrame()
            
            r = requests.get(fight_url)
            soup = bs.BeautifulSoup(r.content,'lxml')
            

            for a in soup.find_all('i', class_=["b-fight-details__fight-title","b-fight-details__text-item"]):
                fight_details_df = fight_details_df.append([a.text.replace('\n','').strip()])

            for a in soup.find_all('i', attrs={'style': 'font-style: normal'}):    
                fight_details_df = fight_details_df.append([a.text.replace('\n','').strip()])       
        
            fight_details_df = fight_details_df.T
            fight_detail_im= fight_detail_im.append(fight_details_df)
             
    fight_detail_im.columns=['Weight_Class','Round_End','Time_End','Fight_format','Referee','Judge1','Judge2','Judge3','Outcome_Detail']
             
##############################################################################       

def db_insert_fighter_dim():
    #run once a month (scheduled task)
    
    def fighter_dic_to_df()
        fighter_id, fighter_name = [],[]
        for i in all_fighters:
            for j,k in all_fighters[i].items():
                fighter_id.append(j)
                fighter_name.append(k)
        fighter_df=pd.DataFrame([fighter_id, fighter_name]).T
        fighter_df.columns=['Fighter_ID','Fighter_Name']
        
    fighter_dic_to_df()

    load_to_db(fighter_df,"fighter_dim")
    
    #sqliteConn = sqlite3.connect('mmabets.db')
    #c= sqliteConn.cursor()
    
    #import data to relevant table
    #fighter_df.to_sql("fighter_dim", sqliteConn, if_exists ='append',index=False)
    #sqliteConn.commit()
        

    #close the cursor/disconnect from db 
    #c.close()
    #sqliteConn.close()

##############################################################################



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
                    #print(listdf[cntr])                    
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
def data_cleansing_2():
    
    for fighter in ufcfightdata:
        for ft_index,fightdict in ufcfightdata[fighter].items():
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                for df in listdf:
                    pd_df_spltr(df)
                    df['Fighter_ID'] =fighter
                    df['Fight_ID'] = fight[34:50]
                                   
    for fighter in ufcfightdata:
        #sqliteConn = sqlite3.connect('mmabets.db')
        #c= sqliteConn.cursor()
        
        for ft_index,fightdict in ufcfightdata[fighter].items():
            
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                for df in range(0,len(listdf)):
                    if df==0:  
                    #import data to fighter_data table
                        load_to_db(listdf[df],"fighter_round_fact")
                        # listdf[df].to_sql("fighter_round_fact", sqliteConn, if_exists ='append',index=False)
                        # sqliteConn.commit()
                    else:
                        load_to_db(listdf[df],"fight_area_round_fact")
                        #listdf[df].to_sql("fight_area_round_fact", sqliteConn, if_exists ='append',index=False)
                        # sqliteConn.commit()                    
            #close the cursor/disconnect from db 
        #c.close()
        #sqliteConn.close()
##############################################################################

def get_fite_dates_results():
        
    dates =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    fighters =[]
    fighters.append('http://ufcstats.com/fighter-details/22a92d7f62195791')
    
    ufcfightdatedim={}
    ufcfightid_dim={}
    
    for fighter in fighters:
        ufcfightdatedim[fighter[36:52]]={}
        
        r = requests.get(fighter)
        soup = bs.BeautifulSoup(r.content,'lxml')
    
        cnt=0
        
        for p in soup.find_all('p',attrs={"class":"b-fight-details__table-text"} ):
            if any(x in p.text for x in dates):
                print(p.text,cnt)
    
                ufcfightdatedim[fighter[36:52]][cnt] = p.text.strip()
                cnt+=1
        
        ufcfightid_dim[fighter[36:52]]={}
        
        cnt=0
        for a in soup.find_all('a', href=True):
            if "fight-details" in a['href']:
               # print(a.text,a['href'])
                if a['href'] not in ufcfightid_dim and a.text !='next' and 'Matchup' not in a.text:
                                    
                    ufcfightid_dim[fighter[36:52]][cnt] = {a['href']: a.text}
                    cnt+=1
    
    for fighter in ufcfightdatedim:
    
        datedim_df = pd.DataFrame.from_dict(ufcfightdatedim.values()).T
        datedim_df['Fighter_ID']= fighter
        
        
        fightid_dimdf = pd.DataFrame() ##columns=['Fighter_ID','Fight_ID','Result'])
        for fight_index, fightdata in ufcfightid_dim[fighter].items():
            
            fightid_dimdf = fightid_dimdf.append( [[fight_index, fighter, str(fightdata.keys())[46:62], str(fightdata.values())[14:]  ]] )
        
        
    datedim_df.columns=['Fight_Date','Fighter_ID']
    fightid_dimdf.columns=['Fight_Index','Fighter_ID','Fight_ID','Result']
    
    #import data to fighter_data table                 
    load_to_db(datedim_df,"fight_date_dim")
    load_to_db(fightid_dimdf,"fight_id_dim")
    
    #sqliteConn = sqlite3.connect('mmabets.db')
    #c= sqliteConn.cursor()
    
                    
    #import data to fighter_data table
    #datedim_df.to_sql("fight_date_dim", sqliteConn, if_exists ='append',index=True)
    #sqliteConn.commit()
    
    #fightid_dimdf.to_sql("fight_id_dim", sqliteConn, if_exists ='append',index=False)
    #sqliteConn.commit()
    
    #close the cursor/disconnect from db 
    #c.close()
    #sqliteConn.close()
            

##############################################################################


  

