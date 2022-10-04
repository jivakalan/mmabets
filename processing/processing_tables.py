import pandas as pd

#read in tables
fighter_dim =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fighter_dim.csv", index_col= 0)
main_fight_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\main_fight_fact.csv", index_col= 0)
fighter_record_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fighter_record_fact.csv", index_col= 0)
fight_outcome_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fight_outcome_fact.csv", index_col= 0)
fight_strike_location_fact =pd.read_csv(r"C:\Users\kalan\PycharmProjects\MMABets\extract\data\database\fight_strike_location_fact.csv", index_col= 0)

##fighter -page :  every fighters' record to date:  fighter_record_fact
##fighter dimension table - descriptive variables of fighter:  fighter_dim
#output1 - main fight fact table  :   main_fight_fact
#output2 - descriptive vars of fight - weight class, outcome, ref, format etc only place to get outcome:  fight_outcome_fact
#outpu3 -- distance/clinch/ground = head/body/leg % by fighter for every fight :                          fight_strike_location_fact

#ToDo fix fighterrs typo

single_fighter = fighter_dim[fighter_dim.Fighter_ID =='22a92d7f62195791']
#ToDo remove this when typo is fixed
fighter_record_fact['Fighter_ID'] = fighter_record_fact['Fighterr_ID']

#merge on fighter's record
single_fighter = pd.merge(single_fighter, fighter_record_fact, how = 'inner', on ='Fighter_ID')
main_fight_fact= main_fight_fact.drop_duplicates()

single_fighter = pd.merge(single_fighter, main_fight_fact, how = 'inner', on =['Fighter_ID','Fight_ID'])


single_fight = main_fight_fact[main_fight_fact.Fighter_ID =='22a92d7f62195791']


single_fight = single_fight[single_fight.Fight_ID =='ae0b5ab5bc4bb6a7']
single_fighter = pd.merge(single_fighter, single_fight, how = 'inner', on =['Fighter_ID','Fight_ID'])

##convert row by row data to 1-line per fight
def processing_fight_fact_vars():
    ##input: 1 line per round of fight
#output shuld be 1 line per fighter
#for each column sum/avg/median/25/75/  _0 is main and _1 is opoonent  _0 -- becomes for ---_1 becomes _against?
    fighterIDs = main_fight_fact.Fighter_ID.unique()

    fight_cols = ['Fight_Name', 'Round', 'Knockdowns_0',
                 'Knockdowns_1', 'Significant_Strikes_0', 'Significant_Strikes_1',
                 'Significant_Strike_pct_0', 'Significant_Strike_pct_1',
                 'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0',
                 'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0',
                 'Clinch_1', 'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1',
                 'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0',
                 'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0',
                 'Control_Time_1']
    for fID in fighterIDs:
        df = main_fight_fact[main_fight_fact.Fighter_ID == fID]
        for col in fight_cols:

            print(df[col].sum(),df[col].min(),df[col].max(), df[col].mean(), df[col].median() )




main_fight_fact = processing_fight_fact_vars()

#merge to fight outcome to get outcome

#merge on opponent to get opponents stats per fight

#merge on strike location