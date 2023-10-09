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
####################################################################
##                          Imports                             ###
from process.tools.helper import *
################################################################
## Read in Tables                                            ##
###############################################################
database = import_database()
fighter_dim = database[0]
main_fight_fact = database[1]
fighter_record_fact = database[2]
fight_outcome_fact = database[3]
fight_strike_location_fact = database[4]
fight_odds_fact = database[5]
##########################################################
## Data cleaning + processing                           #
#########################################################
# bit of cleaning
fighter_record_fact = fighter_record_fact.rename(columns={'Fighterr_ID':'Fighter_ID'})
fight_strike_location_fact = fight_strike_location_fact.rename(columns={'Fighterss_ID':'Fighter_ID','Fightss_ID':'Fight_ID'})

# fighter dim - ht + reach > cm
fighter_dim['HT_cm'] = fighter_dim.HT.apply(height_to_cm)
fighter_dim['Reach_cm'] = fighter_dim.REACH.apply(reach_to_cm)
# fighter dim - wt > numeric
fighter_dim['WT_numeric'] = fighter_dim.WT.apply(wt_to_numeric)
# fighter dim - 1-hot encoding stance
fighter_dim = pd.get_dummies(fighter_dim, columns =['STANCE'],dtype=float)

# get cumulative fight outcome data
fight_outcome_fact_cumulative = create_fighter_outcome_cumulative(fight_outcome_fact)

# get fight dates for main fight fact
main_fight_fact_w_dates = pd.merge(main_fight_fact, fight_outcome_fact[['Fight_ID','Fighter_ID','Fight_Date']], on=['Fight_ID','Fighter_ID'])

# create the cumulative main fight fact table
main_fight_fact_cumulative = create_main_fight_fact_cumulative(main_fight_fact_w_dates)

# create the data science dataset;  3 minutes
fight_base = fight_outcome_fact.Fight_ID.unique().tolist()
records = create_ds_test_set_parallel(fight_base, main_fight_fact_cumulative, fighter_dim, fight_outcome_fact_cumulative)
