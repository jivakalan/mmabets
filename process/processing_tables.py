########################################################################
###             Create the DataScience dataset                      ###
#######################################################################
 # Data Model
 # fighter's mma record:                 fighter_record_fact
 # fighter detail:                       fighter_dim
 # output1 - main fight fact table:      main_fight_fact
 # output2 - weight class, outcome:      fight_outcome_fact
 # output3 - distance/clinch/ground:     fight_strike_location_fact
 # output4 - odds data                   fight_odds_fact
#####################################################################
##                          Imports                              ###
from process.tools.helper import *
###################################################################
## Read in Tables ##
####################
src_folder =r'C:\Users\kalan\PycharmProjects\MMABets\extract\data\database'

fighter_dim =pd.read_csv(src_folder +"\\" + "fighter_dim.csv")
main_fight_fact =pd.read_csv(src_folder +"\\" + "main_fight_fact.csv")
fighter_record_fact =pd.read_csv(src_folder +"\\" + "fighter_record_fact.csv")
fight_outcome_fact =pd.read_csv(src_folder +"\\" + "fight_outcome_fact.csv")
fight_strike_location_fact =pd.read_csv(src_folder +"\\" + "fight_strike_location_fact.csv")
fight_odds_fact = pd.read_csv(src_folder +"\\" + "fight_odds_fact.csv")


#####################
## Data process ##
####################
fighter_record_fact = fighter_record_fact.rename(columns={'Fighterr_ID':'Fighter_ID'})
fight_strike_location_fact = fight_strike_location_fact.rename(columns={'Fighterss_ID':'Fighter_ID','Fightss_ID':'Fight_ID'})


# get fight data for main fight fact
main_fight_fact_w_dates = pd.merge(main_fight_fact,fight_outcome_fact[['Fight_ID','Fighter_ID','Fight_Date']], on=['Fight_ID','Fighter_ID'])

# create the cumulative main fight fact table
main_fight_fact_cumulative =  create_main_fight_fact_cumulative(main_fight_fact_w_dates)



df = add_fighters_data(main_fight_fact_cumulative)
df = pd.merge(df,fighter_dim[['Fighter_ID','HT','WT','REACH','BELT']], on='Fighter_ID' )
df['Target'] = np.where(df.Result ='W',1,0)

df.to_csv('full_fights.csv')
#################################################################
###                             Fin                           ##
###############################################################
# ToDo fix fighterrs typo (to QA)
# Todo--regenerate fighter_record_fact - should be fixed
# todo drop unnamed , clean up ht --> feet inches to cms
# ToDo; create extract.py - combines crawl_ufc_fight_data.py & crawl_ufc_fight_data_detail.py
# ToDo  RuntimeWarning: Mean of empty slice return np.nanmean(a, axis, out=out, keepdims=keepdims)
# ToDo: Additional data process x2
######################################################










