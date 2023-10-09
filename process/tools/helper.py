#####################################################################
##                          Imports                              ###
import pandas as pd
import datetime
from tqdm import tqdm
import numpy as np
import re
from extract.tools.helper import load_json
from multiprocessing import Pool
#####################################################################

src_folder =r'C:\Users\kalan\PycharmProjects\MMABets\extract\data\database'

def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = (minutes * 60) + seconds
    except:
        total_seconds = 0
    return total_seconds

def height_to_cm(height):
    try:
        feet, inches = map(int, re.findall(r'\d+', height))
        total_inches = (feet * 12) + inches
        cm = round(total_inches * 2.54,0)
    except:
        cm = np.NaN
    return cm

def reach_to_cm(reach):
    try:
        inches = int(reach.split(".")[0])
        cm = round(inches * 2.54,0)
    except:
        cm = np.NaN
    return cm

def wt_to_numeric(weight):
    try:
        weight_num = int(weight.split("lbs")[0])
    except:
        weight_num = np.NaN
    return weight_num

def import_database():
    fighter_dim = pd.read_csv(src_folder + "\\" + "fighter_dim.csv")
    main_fight_fact = pd.read_csv(src_folder + "\\" + "main_fight_fact.csv")
    fighter_record_fact = pd.read_csv(src_folder + "\\" + "fighter_record_fact.csv")
    fight_outcome_fact = pd.read_csv(src_folder + "\\" + "fight_outcome_fact.csv")
    fight_strike_location_fact = pd.read_csv(src_folder + "\\" + "fight_strike_location_fact.csv")
    fight_odds_fact = pd.read_csv(src_folder + "\\" + "fight_odds_fact.csv")

    database = [fighter_dim, main_fight_fact, fighter_record_fact, fight_outcome_fact
              , fight_strike_location_fact, fight_odds_fact]
    return database


def create_ds_test_set(fight_base,main_fight_fact_cumulative,fighter_dim,fight_outcome_fact_cumulative):

    cols = load_json('process/tools/ds_dataset_cols.json')
    cumulative_cols_0 = cols['cumulative_cols_0']
    cumulative_cols_1 = cols['cumulative_cols_1']
    cumulative_demo_cols = cols['cumulative_demo_cols']
    demo_cols = cols['demo_cols']
    odds_cols = cols['odds_cols'] #todo: from fight odds fact

    records = []

    for fight in tqdm(fight_base):

        fight_block = fight_outcome_fact_cumulative[fight_outcome_fact_cumulative.Fight_ID==fight]

        if len(fight_block) == 2:
            fighter_0 = fight_block.Fighter_ID.iloc[0]
            fighter_1 = fight_block.Fighter_ID.iloc[1]
            fight_date = pd.to_datetime(fight_block.Fight_Date.iloc[0])

            # look up the cum totals data upto the date
            try:
                cumdata_fighter_0 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_0)
                                                               & (main_fight_fact_cumulative.Fight_Date < fight_date)][cumulative_cols_0].iloc[-1].to_frame().T.reset_index(drop=True)
                cumdata_fighter_1 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_1)
                                                               & (main_fight_fact_cumulative.Fight_Date < fight_date)][cumulative_cols_1].iloc[-1].to_frame().T.reset_index(drop=True)
            except:
                cumdata_fighter_0 = pd.DataFrame(0, index=range(1), columns = cumulative_cols_0)
                cumdata_fighter_1 = pd.DataFrame(0, index=range(1), columns = cumulative_cols_1)


            # lookup the demographic data
            demos_fighter_0 = fighter_dim[fighter_dim.Fighter_ID == fighter_0][demo_cols].reset_index(drop=True)
            # Rename the columns by adding a suffix "_0"
            demos_fighter_0.columns = [col + '_0' for col in demo_cols]

            demos_fighter_1 = fighter_dim[fighter_dim.Fighter_ID == fighter_1][demo_cols].reset_index(drop=True)
            # Rename the columns by adding a suffix "_0"
            demos_fighter_1.columns = [col + '_1' for col in demo_cols]


            # lookup the cumulative demo data
            demos_cum_fighter_0 = fight_block[fight_block.Fighter_ID == fighter_0][cumulative_demo_cols].reset_index(drop=True)
            demos_cum_fighter_0.columns = [col + '_0' for col in cumulative_demo_cols]

            demos_cum_fighter_1 = fight_block[fight_block.Fighter_ID == fighter_1][cumulative_demo_cols].reset_index(drop=True)
            demos_cum_fighter_1.columns = [col + '_1' for col in cumulative_demo_cols]

            # calculate the cumulative PCT metrics
            # todo

            # lookup the Outcome - 0/1/2
            fighter_0_outcome = fight_block[fight_block.Fighter_ID == fighter_0]['Outcome'].to_frame().reset_index(drop=True).rename(columns={'Outcome': 'Fighter_0_Outcome'})

            # Stitch all the parts back back together
            fight_df = pd.DataFrame({'Fight_ID':[fight]})
            fighter_0_df = pd.DataFrame({'Fighter_ID_0':[fighter_0]})
            fighter_1_df = pd.DataFrame({'Fighter_ID_1':[fighter_1]})

            record = [fight_df, fighter_0_df, cumdata_fighter_0, fighter_1_df,
                      cumdata_fighter_1, demos_fighter_0, demos_fighter_1,
                      demos_cum_fighter_0, demos_cum_fighter_1, fighter_0_outcome]

            records.append(record)

        else:
            continue




    return records


def map_result(value):
    # Define a custom function to map the values from Result to Outcome

    if value == 'win':
        return 1
    elif value == 'loss':
        return 0
    elif value == 'draw':
        return 2
    elif value == 'nc':
        return 3
    else:
        return None


def create_main_fight_fact_cumulative(main_fight_fact_w_dates):

    main_fight_fact_w_dates['Fight_Date'] = pd.to_datetime(main_fight_fact_w_dates['Fight_Date'])
    main_fight_fact_w_dates = main_fight_fact_w_dates.sort_values(by=['Fighter_ID', 'Fight_Date'])
    main_fight_fact_w_dates['Control_Time_0_Seconds'] = main_fight_fact_w_dates['Control_Time_0'].apply(time_to_seconds)
    main_fight_fact_w_dates['Control_Time_1_Seconds'] = main_fight_fact_w_dates['Control_Time_1'].apply(time_to_seconds)
    cols =['Knockdowns_0',
       'Knockdowns_1', 'Significant_Strikes_0', 'Significant_Strikes_1',
       'Significant_Strike_pct_0', 'Significant_Strike_pct_1',
       'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0',
       'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0',
       'Clinch_1', 'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1',
       'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0',
       'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0_Seconds',
       'Control_Time_1_Seconds']

    for col in cols:
        try:
            main_fight_fact_w_dates[col+'_cumulative']= main_fight_fact_w_dates.groupby(['Fighter_ID'])[col].cumsum()
        except:
            pass


    return main_fight_fact_w_dates


def create_fighter_outcome_cumulative(fight_outcome_fact):
    # Apply the custom function to create the new column 'Outcome' from Result
    fight_outcome_fact['Outcome'] = fight_outcome_fact['Result'].apply(map_result)

    # one-hot encode Result column -> win | loss | nc | draw
    fight_outcome_fact = pd.get_dummies(fight_outcome_fact, columns=['Result','METHOD'],dtype=float)

    cols = ['Result_win','Result_loss','Result_nc','Result_draw','METHOD_CNC', 'METHOD_DQ',
            'METHOD_Decision', 'METHOD_KO/TKO', 'METHOD_M-DEC', 'METHOD_Other', 'METHOD_Overturned',
            'METHOD_S-DEC','METHOD_SUB', 'METHOD_U-DEC']

    fight_outcome_fact['Fight_Date'] = pd.to_datetime(fight_outcome_fact['Fight_Date'])
    fight_outcome_fact = fight_outcome_fact.sort_values(by=['Fighter_ID', 'Fight_Date'])

    for col in cols:
        fight_outcome_fact[col+'_cumulative'] =  fight_outcome_fact.groupby(['Fighter_ID'])[col].cumsum()


    return fight_outcome_fact


#
#
# def create_ds_test_set_chunk(chunk):
#     cols = load_json('process/tools/ds_dataset_cols.json')
#     cumulative_cols_0 = cols['cumulative_cols_0']
#     cumulative_cols_1 = cols['cumulative_cols_1']
#     cumulative_demo_cols = cols['cumulative_demo_cols']
#     demo_cols = cols['demo_cols']
#     odds_cols = cols['odds_cols']  # todo: from fight odds fact
#
#     records = []
#
#     for fight in chunk:
#         fight_block = fight_outcome_fact_cumulative[fight_outcome_fact_cumulative.Fight_ID == fight]
#
#         if len(fight_block) == 2:
#             fighter_0 = fight_block.Fighter_ID.iloc[0]
#             fighter_1 = fight_block.Fighter_ID.iloc[1]
#             fight_date = pd.to_datetime(fight_block.Fight_Date.iloc[0])
#
#             # look up the cum totals data upto the date
#             try:
#                 cumdata_fighter_0 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_0)
#                                                                & (main_fight_fact_cumulative.Fight_Date < fight_date)][cumulative_cols_0].iloc[-1].to_frame().T.reset_index(drop=True)
#                 cumdata_fighter_1 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_1)
#                                                                & (main_fight_fact_cumulative.Fight_Date < fight_date)][cumulative_cols_1].iloc[-1].to_frame().T.reset_index(drop=True)
#             except:
#                 cumdata_fighter_0 = pd.DataFrame(0, index=range(1), columns = cumulative_cols_0)
#                 cumdata_fighter_1 = pd.DataFrame(0, index=range(1), columns = cumulative_cols_1)
#
#
#             # lookup the demographic data
#             demos_fighter_0 = fighter_dim[fighter_dim.Fighter_ID == fighter_0][demo_cols].reset_index(drop=True)
#             # Rename the columns by adding a suffix "_0"
#             demos_fighter_0.columns = [col + '_0' for col in demo_cols]
#
#             demos_fighter_1 = fighter_dim[fighter_dim.Fighter_ID == fighter_1][demo_cols].reset_index(drop=True)
#             # Rename the columns by adding a suffix "_0"
#             demos_fighter_1.columns = [col + '_1' for col in demo_cols]
#
#
#             # lookup the cumulative demo data
#             demos_cum_fighter_0 = fight_block[fight_block.Fighter_ID == fighter_0][cumulative_demo_cols]
#             demos_cum_fighter_0.columns = [col + '_0' for col in cumulative_demo_cols]
#
#             demos_cum_fighter_1 = fight_block[fight_block.Fighter_ID == fighter_1][cumulative_demo_cols]
#             demos_cum_fighter_1.columns = [col + '_1' for col in cumulative_demo_cols]
#
#             # calculate the cumulative PCT metrics
#             # todo
#
#             # lookup the Outcome - 0/1/2
#             fighter_0_outcome = fight_block[fight_block.Fighter_ID == fighter_0]['Outcome'].to_frame().reset_index(drop=True).rename(columns={'Outcome': 'Fighter_0_Outcome'})
#
#             # Stitch all the parts back back together
#             fight_df = pd.DataFrame({'Fight_ID':[fight]})
#             fighter_0_df = pd.DataFrame({'Fighter_ID_0':[fighter_0]})
#             fighter_1_df = pd.DataFrame({'Fighter_ID_1':[fighter_1]})
#
#
#         record = [fight_df, fighter_0_df, cumdata_fighter_0, fighter_1_df,
#                  cumdata_fighter_1, demos_fighter_0, demos_fighter_1,
#                  demos_cum_fighter_0, demos_cum_fighter_1, fighter_0_outcome]
#
#         records.append(record)
#
#
#     return records
#
#
#
# def create_ds_test_set_parallel(fight_base, main_fight_fact_cumulative, fighter_dim, fight_outcome_fact_cumulative, num_processes=4):
#     # Split fight_base into chunks for parallel processing
#     chunk_size = len(fight_base) // num_processes
#     chunks = [fight_base[i:i + chunk_size] for i in range(0, len(fight_base), chunk_size)]
#
#     # Create a pool of processes
#     with Pool(processes=num_processes) as pool:
#         results = pool.map(create_ds_test_set_chunk, chunks)
#
#     # Flatten the results list of lists
#     records = [record for sublist in results for record in sublist]
#
#     return records