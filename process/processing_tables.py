
########################################################################
###             Create the DataScience dataset                      ###
#######################################################################
 # Data Model
 # fighter's mma record:                 fighter_record_fact
 # fighter detail:                       fighter_dim
 # output1 - main fight fact table:      main_fight_fact
 # output2 - weight class, outcome:      fight_outcome_fact
 # output3 - distance/clinch/ground:     fight_strike_location_fact
#####################################################################
##                          Imports                              ###
import pandas as pd
from unit_testing.unit_processing import *
from process.tools.helper import *
###################################################################
## Read in Tables ##
####################
fighter_dim =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fighter_dim.csv", index_col= 0)
main_fight_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\main_fight_fact.csv", index_col= 0)
fighter_record_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fighter_record_fact.csv", index_col= 0)
fight_outcome_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fight_outcome_fact.csv", index_col= 0)
fight_strike_location_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fight_strike_location_fact.csv", index_col= 0)
#####################
## Data process ##
####################
fighter_record_fact = fighter_record_fact.rename(columns={'Fighterr_ID':'Fighter_ID'})
fight_strike_location_fact = fighter_record_fact.rename(columns={'Fighterss_ID':'Fighter_ID','Fightss_ID':'Fight_ID'})

fight_outcome_fact= fight_outcome_fact.drop_duplicates()
fighters = list(fighter_dim.Fighter_ID.unique())
main_fight_fact_cumulative =  create_main_fight_fact_cumulative(main_fight_fact,fighters)



df = add_fighters_data(main_fight_fact_cumulative)
df = pd.merge(df,fighter_dim[['Fighter_ID','HT','WT','REACH','BELT']], on='Fighter_ID' )
df['Target'] = np.where(df.Result ='W',1,0)

df.to_csv('full_fights.csv')
#################################################################
###                             Fin                           ##
###############################################################
## UNIT TESTING ###
##################
tests = unit_testing_processing(df,fight_outcome_fact)
############################################################
# ToDo fix fighterrs typo (to QA)
# Todo--regenerate fighter_record_fact - should be fixed
# todo drop unnamed , clean up ht --> feet inches to cms
# ToDo; create extract.py - combines crawl_ufc_fight_data.py & crawl_ufc_fight_data_detail.py
# ToDo  RuntimeWarning: Mean of empty slice return np.nanmean(a, axis, out=out, keepdims=keepdims)
# ToDo: Additional data process x2
######################################################










