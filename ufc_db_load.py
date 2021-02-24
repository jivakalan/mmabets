# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:20:26 2021

@author: kalan
"""


##############################################################################       

#def fight_update():
    #for each fighter, if there are new fight IDs, then include into the dictionary, otherwise - no
    #need to update the not in ufcfightdata conditio so that it actually does a real check
    #check back for Cyril Gane on Sunday
    #before Sunday - fix not in ufcfightdata condition
    
##############################################################################       

# def db_insert():
    
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



# #run once a month (scheduled task)
# all_fighters = get_all_fighter_pages()  #19 seconds for 3597 fighters
# #save as json
# with open('ufcfighters.json','w') as fp:
#     json.dump(all_fighters,fp)
# #get_all_fights can take 12 hours-only run on test data 
# #run test this week 
# #run update sat/sun and see - can I afford to run this once a week 
# ufcfightdata = get_all_fights(fighters)                
# #fighter table insert           
# db_insert()


##############################################################################


# def fight_df_readr():
   # with open('ufcfightdata.pickle','rb') as handle:
   #   test= pickle.load(handle)
    

# tonyferg= ufcfightdata['22a92d7f62195791'][1]['http://ufcstats.com/fight-details/d395828f5cb045a5']
# tf1=tonyferg[1]
# tf3=tonyferg[3]


# if tonyferg[1]: 
#     tf1['Round']=list(tf1.columns[9])[1:6]
#     tf1.columns=['Fighter','Knockdowns','Significant_Strikes','Significant_Strike_pct','Total_Strikes','Takedowns','Takedown_pct','Submission_Attempt','Rev','Control_Time','Round']
    
# else:
#     tf3['Round']=list(tf3.columns[0])[1:6]
#     del tf3['Unnamed: 9_level_0']
#     tf3.columns=['Fighter','Significant_Strikes','Significant_Strike_pct','Head','Body','Leg','Distance','Clinch','Ground','Round']



# def pd_df_spltr(tf1):
        
#     for column in tf1.columns:
        
#         if column =='Fighter':
#             tf1[['Fighter_1_First_Name','Fighter_1_Last_Name','Fighter_2_First_Name','Fighter_2_Last_Name']] = tf1[column].str.split(" ", expand=True)
#         elif column =='Round':
#             continue
#         else:
#             tf1[['%s_0' %column,'%s_1' %column]] = tf1[column].str.split("  ", expand=True)
            

#     return tf1

# pd_df_spltr(tf3)





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
  
#4 full run (today!):)
    #run on Azure
    #1hr
    

