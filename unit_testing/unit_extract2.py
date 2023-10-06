#####################################################################
##                          Imports                              ###
####################################################################
from extract.run_crawlers import *
import os
####################################################################
def get_modif_date_testing_dataset():
    destination = 'extract/data/testing'

    dates = []
    for filename in os.listdir(destination):

        file_path = os.path.join(destination, filename)

        if os.path.isfile(file_path):
            # Get the modified timestamp
            timestamp = os.path.getmtime(file_path)
            # Convert the timestamp to a readable date format
            modified_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            dates.append(modified_date)
    modif_date = max(dates)
    return modif_date

def prepare_inits_data():
    # prepare the testing data

    # load alpha pages
    alphabetic_fighter_list_urls = load_json('extract/data/outputs/alphabetic_fighter_list_urls.json')
    alphabetic_fighter_list_urls = [alphabetic_fighter_list_urls[12]]
    #load fighterlinks
    FightLinks = load_json(r'extract\data\outputs\fightLinks.json')
    FightLinks = FightLinks[0:5]  #
    # load fighter odds pages
    fighters_odds_list = load_json('extract/data/outputs/bestoddfighters.json')
    fighters_odds_list = ["/fighters/Israel-Adesanya-7845"]

    testing_data = [alphabetic_fighter_list_urls, FightLinks, fighters_odds_list]

    return testing_data

# Test Upsert
def test_upsert_to_csv_singlekey():

    existing_csv_file = 'extract/data/testing/fighter_dim.csv'
    expected_result = [
        'f34s1029djkms',  # Fighter ID
        'Jiva Kalan',  # Fighter name
        '6\' 0"',  # Height (with single quotes for the feet and double quotes for inches)
        '155 lbs.',  # Weight
        '76.0"',  # Reach
        'Southpaw',  # Fighting stance
        '99',  # Wins
        '0',   # losses
        '1',   # Draws
        ''
    ]
    # Define column names
    columns = ['Fighter_ID', 'Fighter_name', 'HT', 'WT', 'REACH', 'STANCE', 'W', 'L', 'D','BELT']

    # Create a new DataFrame
    new_data_df = pd.DataFrame([expected_result], columns=columns)

    key_column =['Fighter_ID']

    merged_df = upsert_to_csv(existing_csv_file, new_data_df, key_column)
    result = merged_df[merged_df.Fighter_ID=='f34s1029djkms'].iloc[0].tolist()

    assert result == expected_result

def test_upsert_to_csv_singlekey_update():

    existing_csv_file = 'extract/data/testing/fighter_dim.csv'
    csv_file = pd.read_csv(existing_csv_file)
    print(csv_file[csv_file.Fighter_ID=='f4c49976c75c5ab2'].iloc[0].tolist())

    expected_result = [
        'f4c49976c75c5ab2',  # Fighter ID
        'Conor McGregor',  # Fighter name
        '5\' 9"',  # Height (with single quotes for the feet and double quotes for inches)
        '195 lbs.',  # Weight
        '74.0"',  # Reach
        'Southpaw',  # Fighting stance
        '22',  # Wins
        '6',   # losses
        '0',   # Draws
        ''
    ]
    # Define column names
    columns = ['Fighter_ID', 'Fighter_name', 'HT', 'WT', 'REACH', 'STANCE', 'W', 'L', 'D','BELT']

    # Create a new DataFrame
    new_data_df = pd.DataFrame([expected_result], columns=columns)

    key_column =['Fighter_ID']

    merged_df = upsert_to_csv(existing_csv_file, new_data_df, key_column)
    result = merged_df[merged_df.Fighter_ID=='f4c49976c75c5ab2'].iloc[0].tolist()

    assert result == expected_result

def test_upsert_to_csv_twokey_update():

    existing_csv_file = 'extract/data/testing/main_fight_fact.csv'

    #update adesanya fight to have various 99% metrics
    expected_result = ['1338e2c7480bdf9e', '7f16e7725245bb2d', 'UFC 293: Adesanya vs. Strickland'
                        , 1, 0, 1, 12, 27, '99%', '99%', 99, 99, 99, 22, 3, 1, 8, 4, 12, 11, 0, 11
                        , 0, 5, 0, 0, '---', '---', 0, 0, 0, 0, '0:00', '0:14']


    # Define column names
    columns = ['Fighter_ID', 'Fight_ID', 'Fight_Name', 'Round', 'Knockdowns_0',
               'Knockdowns_1', 'Significant_Strikes_0', 'Significant_Strikes_1',
               'Significant_Strike_pct_0', 'Significant_Strike_pct_1',
               'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0',
               'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0',
               'Clinch_1', 'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1',
               'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0',
               'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0',
               'Control_Time_1']

    #

    # Create a new DataFrame
    new_data_df = pd.DataFrame([expected_result], columns=columns)

    key_column =['Fighter_ID','Fight_ID' ,'Round']

    merged_df = upsert_to_csv(existing_csv_file, new_data_df, key_column)
    result = merged_df[(merged_df.Fighter_ID == '1338e2c7480bdf9e') & (merged_df.Fight_ID == '7f16e7725245bb2d') & (merged_df.Round == 1)]
    result = result.iloc[0].tolist()

    assert expected_result==result

def test_upsert_all_data():

    data = run_pipeline(prepare_inits_data()) #todo - use fake data for testing ...and then measure if the result changed

    upsert_all_data(data, environment='testing')

    result = get_modif_date_testing_dataset()

    expected_result = datetime.now().strftime('%Y-%m-%d')

    assert result == expected_result


# Other tests
def test_run_fight_data():
    data ={}
    alphabetic_fighter_list_urls = load_json('extract/data/outputs/alphabetic_fighter_list_urls.json')

    result = run_fight_data(data, alphabetic_fighter_list_urls, env='testing')

    result = {'fighter_dim': data['fighter_dim'].columns.tolist()
            , 'fight_outcome_fact': data['fight_outcome_fact'].columns.tolist()}
    expected_result = {
        'fighter_dim': ['Fighter_ID', 'Fighter_name', 'HT', 'WT', 'REACH', 'STANCE', 'W', 'L', 'D', 'BELT']
        ,'fight_outcome_fact': ['Fighter_ID', 'Fight_ID', 'Result', 'Fight_Name', 'Fight_Date', 'METHOD', 'ROUND', 'TIME']
        }
    assert result == expected_result

def test_run_fight_detail():
    data = {}


    FightLinks = load_json(r'extract\data\outputs\fightLinks.json')
    FightLinks = FightLinks[0:5]

    result = run_fight_detail(data, FightLinks)

    result = {'main_fight_fact': data['main_fight_fact'].columns.tolist()
            , 'fighter_record_fact': data['fighter_record_fact'].columns.tolist()
            , 'fight_strike_location_fact': data['fight_strike_location_fact'].columns.tolist()
              }

    expected_result = {
        'main_fight_fact': ['Fighter_ID', 'Fight_ID', 'Fight_Name', 'Round', 'Knockdowns_0', 'Knockdowns_1', 'Significant_Strikes_0', 'Significant_Strikes_1', 'Significant_Strike_pct_0', 'Significant_Strike_pct_1', 'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0', 'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0', 'Clinch_1', 'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1', 'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0', 'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0', 'Control_Time_1']
        ,'fighter_record_fact': ['Fighter_ID', 'Fight_ID', 'Fight_Name', 'Weight_Class', 'Opponent', 'Method', 'Round_End', 'Time_End', 'Fight_format', 'Referee', 'Details']
        ,'fight_strike_location_fact': ['Fighter_ID', 'Fight_ID', 'Fighter_0', 'Fighter_1', 'Head_0_Pct', 'Head_1_Pct', 'Body_0_Pct', 'Body_1_Pct', 'Leg_0_Pct', 'Leg_1_Pct', 'Distance_0_Pct', 'Distance_1_Pct', 'Clinch_0_Pct', 'Clinch_1_Pct', 'Ground_0_Pct', 'Ground_1_Pct']
        }
    assert result == expected_result

def test_run_pipeline():

    data = run_pipeline(prepare_inits_data())

    result = {'fighter_dim': data['fighter_dim'].columns.tolist()
            , 'fight_outcome_fact': data['fight_outcome_fact'].columns.tolist()
            , 'main_fight_fact': data['main_fight_fact'].columns.tolist()
            , 'fighter_record_fact': data['fighter_record_fact'].columns.tolist()
            , 'fight_strike_location_fact': data['fight_strike_location_fact'].columns.tolist()
            , 'fight_odds_fact': data['fight_odds_fact'].columns.tolist()
              }
    expected_result = {
          'fighter_dim': ['Fighter_ID', 'Fighter_name', 'HT', 'WT', 'REACH', 'STANCE', 'W', 'L', 'D', 'BELT']
        , 'fight_outcome_fact': ['Fighter_ID', 'Fight_ID', 'Result', 'Fight_Name', 'Fight_Date', 'METHOD', 'ROUND', 'TIME']
        , 'main_fight_fact': ['Fighter_ID', 'Fight_ID', 'Fight_Name', 'Round', 'Knockdowns_0', 'Knockdowns_1',
                            'Significant_Strikes_0', 'Significant_Strikes_1', 'Significant_Strike_pct_0',
                            'Significant_Strike_pct_1', 'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1',
                            'Body_0', 'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0', 'Clinch_1',
                            'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1', 'Takedown_pct_0', 'Takedown_pct_1',
                            'Submission_Attempt_0', 'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0',
                            'Control_Time_1']
        , 'fighter_record_fact': ['Fighter_ID', 'Fight_ID', 'Fight_Name', 'Weight_Class', 'Opponent', 'Method',
                                  'Round_End', 'Time_End', 'Fight_format', 'Referee', 'Details']
        , 'fight_strike_location_fact': ['Fighter_ID', 'Fight_ID', 'Fighter_0', 'Fighter_1', 'Head_0_Pct', 'Head_1_Pct',
                                         'Body_0_Pct', 'Body_1_Pct', 'Leg_0_Pct', 'Leg_1_Pct', 'Distance_0_Pct',
                                         'Distance_1_Pct', 'Clinch_0_Pct', 'Clinch_1_Pct', 'Ground_0_Pct',
                                         'Ground_1_Pct']
        , 'fight_odds_fact': ['Matchup', 'Open', 'Closing Range', 'Close Start Range', 'Close End Range', 'Movement', 'Event', 'Fight Date']

    }
    assert result == expected_result



def test_crawler_0_0():
    crawler(active=0,update=0, environment='testing')
    return

def test_crawler_1_0():
    crawler(active=1,update=0, environment='testing')
    return