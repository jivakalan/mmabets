from extract.tools.helper import *
import json
import time as t 
import requests
import bs4 as bs 
import pandas as pd

def get_fight_end_times():

    ufcfightdata={}

    ##range of scores in ufc decision 30-23 for 3-rounder or 50-42 for 5rds
    scores =['23','24','25','26','27','28','29','30','42','43','44','45','46','47','48','49','50']
    
    ufcfightdataf= pickle.load(open("extract/data/ufcfightdata.pickle", "rb"))
    #ufcfightdataf =load_latest_pickle()
    fightersl = list(ufcfightdataf.keys())
    keys_to_extract = fightersl[1501:]
    
    # keys_to_extract = []
    # for fighter in fighters:
    #     keys_to_extract.append(fighter[36:52])
    
    ufcfightdata = {key: ufcfightdataf[key] for key in keys_to_extract}
     
    start = t.time()         
    
    fight_detail_im = pd.DataFrame()
    
    for fighter in ufcfightdata:
        for ft_index,fightdict in ufcfightdata[fighter].items():
            for fight_url in  ufcfightdata[fighter][ft_index]:
                #print(fight_url)
                fight_details_df = pd.DataFrame()
                
                r = requests.get(fight_url)
                soup = bs.BeautifulSoup(r.content,'lxml')
                
                
                
                for a in soup.find_all('i', class_=["b-fight-details__fight-title","b-fight-details__text-item"]):
                    
                    if any(score in a.text for score in scores):
                        continue
                        
                    else:
                        fight_details_df = fight_details_df.append([a.text.replace('\n','').strip()])
                    
                for a in soup.find_all('i', attrs={'style': 'font-style: normal'}):    
                    fight_details_df = fight_details_df.append([a.text.replace('\n','').strip()])       
            
                fight_details_df = fight_details_df.T
                fight_details_df['Fighter_ID'] = fighter
                fight_details_df['Fight_ID'] = fight_url[34:50]
                fight_detail_im= fight_detail_im.append(fight_details_df)

    stop = t.time()         
    time= stop-start 
    print('This took %s seconds' %time)  
               
    fight_detail_im.columns=['Weight_Class','Round_End','Time_End','Fight_format','Referee','Judge1','Judge2','Judge3','Outcome_Detail']

    load_to_db(fight_detail_im, 'fight_outcome_dim')
    
##############################################################################       

def db_insert_fighter_dim(all_fighters):
    #run once a month (scheduled task)
    
    def fighter_dic_to_df():
        fighter_id, fighter_name = [],[]
        for i in all_fighters:
            for j,k in all_fighters[i].items():
                fighter_id.append(j)
                fighter_name.append(k)
        fighter_df=pd.DataFrame([fighter_id, fighter_name]).T
        fighter_df.columns=['Fighter_ID','Fighter_Name']
        
    fighter_dic_to_df()

    load_to_db(fighter_df,"fighter_dim")


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
    start = t.time()
    for fighter in ufcfightdata:
        for ft_index,fightdict in ufcfightdata[fighter].items():
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                for df in listdf:
                    pd_df_spltr(df)
                    df['Fighter_ID'] =fighter
                    df['Fight_ID'] = fight[34:50]
                                   
    for fighter in ufcfightdata:
        
        for ft_index,fightdict in ufcfightdata[fighter].items():
            
            for fight, listdf in  ufcfightdata[fighter][ft_index].items():
                for df in range(0,len(listdf)):
                    if df==0:  
                    #import data to fighter_data table
                        load_to_db(listdf[df],"fighter_round_fact")

                    else:
                        load_to_db(listdf[df],"fight_area_round_fact")
    stop = t.time()         
    time= stop-start 
    print('This took %s seconds' %time)  
    
##############################################################################

def get_fite_dates_results():
    with open(r'../extract/data/ufcfighters.json', 'r') as fp:
        fighters = json.load(fp) 
        
    dates =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    # fighters =[]
    # fighters.append('http://ufcstats.com/fighter-details/22a92d7f62195791')
    # fighters.append('http://ufcstats.com/fighter-details/787bb1f087ccff8a')
    
    fighters = list(fighters.keys())
    fighters = fighters[:500]
    
    ufcfightdatedim={}
    ufcfightid_dim={}
    
    start = t.time()
    
    for fighter in fighters:
        ufcfightdatedim[fighter[36:52]]={}
        
        r = requests.get(fighter)
        soup = bs.BeautifulSoup(r.content,'lxml')
    
        cnt=0
        
        for p in soup.find_all('p',attrs={"class":"b-fight-details__table-text"} ):
            if any(x in p.text for x in dates):
                #print(p.text,cnt)
    
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
                    
    stop = t.time()         
    time= stop-start 
    print('This took %s seconds' %time)  
      
 
    datedim_df = pd.DataFrame()
    fightid_dimdf = pd.DataFrame()
    
    for fighter in ufcfightdatedim:

        df = pd.DataFrame.from_dict(ufcfightdatedim[fighter].items())
        df['Fighter_Id'] = fighter 
    
        datedim_df = datedim_df.append(df)        
        
        
        
        for fight_index, fightdata in ufcfightid_dim[fighter].items():
            
            fightid_dimdf = fightid_dimdf.append( [[fight_index, fighter, str(fightdata.keys())[46:62], str(fightdata.values())[14:]  ]] )
        
 
        
    datedim_df.columns=['Fight_Index','Fight_Date','Fighter_ID']
    fightid_dimdf.columns=['Fight_Index','Fighter_ID','Fight_ID','Result']
    

    
    #import data to fighter_data table                 
    load_to_db(datedim_df,"fight_date_dim")
    load_to_db(fightid_dimdf,"fight_id_dim")
    

            

##############################################################################


