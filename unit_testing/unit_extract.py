#####################################################################
##                          Imports                              ###
####################################################################
from extract.crawl_best_fight_odds import *
from extract.crawl_fighters import *
from extract.crawl_ufc_fight_data import *
from extract.crawl_ufc_fight_data_detail import *
import pandas as pd

#################### Test Crawl Fighters ############################
def test_get_alpha_pages():
    result = get_alpha_pages()
    result = result[0]
    expected_result = 'http://ufcstats.com/statistics/fighters?char=a&page=all'
    assert result ==expected_result

def test_get_all_ufc_fighterIDs():
    urls =['http://ufcstats.com/statistics/fighters?char=y&page=all']
    result = get_all_ufc_fighterIDs(urls)
    result = result['http://ufcstats.com/fighter-details/d661ce4da776fc20']
    expected_result = {'d661ce4da776fc20': 'Petr Yan No Mercy'}
    assert result == expected_result

def test_get_active_fighters():
    test_fighter ={'http://ufcstats.com/fighter-details/f4c49976c75c5ab2': {"f4c49976c75c5ab2": "Conor McGregor"}}
    Active_fighters, result = get_active_fighters(test_fighter, days =365)
    expected_result = [] #Conor McGregor is not active, no fight in last 12 months
    assert result == expected_result

#################### Test Crawl Fight Data ##########################
def test_generate_alphabetic_fighter_list_urls():
    alphabetic_fighter_list_urls = generate_alphabetic_fighter_list_urls()
    result = alphabetic_fighter_list_urls[0]
    expected_result = 'http://ufcstats.com/statistics/fighters?char=a&page=all'

    assert result == expected_result, f"get_fighterDim failed: {result} is not equal to {expected_result}"

def test_crawl_fighterDim():
    with open('extract/data/outputs/alphabetic_fighter_list_urls.json', 'r') as json_file:
        alphabetic_fighter_list_urls = json.load(json_file)

    testId = [alphabetic_fighter_list_urls[12]]
    FighterLink, data1 = crawl_fighterDim(testId)

    df1 = pd.DataFrame(data=data1)
    result = df1[df1.Fighter_ID=='f4c49976c75c5ab2'].iloc[0].tolist()

    expected_result = [
        'f4c49976c75c5ab2',  # Fighter ID
        'Conor McGregor',  # Fighter name
        '5\' 9"',  # Height (with single quotes for the feet and double quotes for inches)
        '155 lbs.',  # Weight
        '74.0"',  # Reach
        'Southpaw',  # Fighting stance
        '22',  # Wins
        '6',   # losses
        '0',   # Draws
        ''
    ]

    assert result == expected_result, f"crawl_FighterDim failed: {result} is not equal to {expected_result}"

def test_crawl_FightOutcomeFact():

    FighterLink =['http://ufcstats.com/fighter-details/1338e2c7480bdf9e']
    data2 = crawl_FightOutcomeFact(FighterLink)
    df2 = pd.DataFrame(data=data2)
    result = df2[df2.Fighter_ID == '1338e2c7480bdf9e'].iloc[-1].tolist()

    expected_result = [
        '1338e2c7480bdf9e',  # FighterID
        '1cd5d5e271b646a3', # FightID debut
        'win', # Outcome
        'UFC 221: Romero vs. Rockhold', # FightName
        'Feb. 10, 2018', # FightDate
        'KO/TKO',        # Method
        '2',             # Round
        '3:37'         # Time
        ]

    assert result == expected_result, f"crawl_FightOutcomeFact failed: {result} is not equal to {expected_result}"

#################### Test Crawl Fight Data Detail ###################

def test_crawl_main_fight_fact():
    with open('extract/data/outputs/fightLinks.json', 'r') as json_file:
       FightLinks = json.load(json_file)

    FightLinks =FightLinks[0:10]

    data1 = crawl_main_fight_fact(FightLinks)
    df1=pd.DataFrame(data=data1)

    result = df1[df1.Fight_ID=='ae989e21c3839b49'].iloc[0].tolist()

    expected_result = ['2f5cbecbbe18bac4', #FighterID
         'ae989e21c3839b49',                #FightID
         'UFC Fight Night: Volkov vs. Aspinall', #FightName
         '1' , #Round
         '0',  #Knockdowns_0
         '1' , #knockdowns_1
         '17', #sigstr_0
         '21', #sigstr1
        # 'Sig_Strike_pct_0', 'Sig_Strike_pct_1','Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0',
         '50%', '44%', '34', '48', '4', '21', '4',
        # 'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0', 'Clinch_1', 'Ground_0', 'Ground_1'
         '0', '9', '0', '17', '6', '0', '4', '0', '11',
        # 'Takedowns_0', 'Takedowns_1', 'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0', 'Submission_Attempt_1'
         '0', '0', '0%', '---', '0', '0'
        # 'Rev_0', 'Rev_1', 'Control_Time_0','Control_Time_1'
          , '0', '0', '0:00', '0:12']

    assert result == expected_result, f"crawl_main_fight_fact failed: {result} is not equal to {expected_result}"
    #http://ufcstats.com/fight-details/ae989e21c3839b49

def test_crawl_fighter_record_fact():
    # load FightLinks
    with open('extract/data/outputs/fightLinks.json', 'r') as json_file:
        FightLinks = json.load(json_file)
    FightLinks =FightLinks[0:10]
    result = crawl_fighter_record_fact(FightLinks)
    result = pd.DataFrame(data=result)
    #fighter on ID for result
    result = result[result.Fight_ID =='f085f32bbb3220e1'].iloc[0].tolist()

    expected_result = [
            '2f5cbecbbe18bac4', #Fighter_ID
            'f085f32bbb3220e1', #Fight_ID
            'UFC 266: Volkanovski vs. Ortega', #Fight Name
            "Heavyweight Bout", #Weight Class
            "Chris Daukaus", #Opponent
            "KO/TKO", #Method
            '2', #Round
            "1:23",#Time_End
            '3 Rnd (5-5-5)', #Fight Format
            "Mark Smith",   #Referree
            'Punch to Head At Distance ' #Details
            ]

    assert result == expected_result, f"crawl_fighter_record_fact failed: {result} is not equal to {expected_result}"

def test_crawl_fight_strike_location_fact():
    with open('extract/data/outputs/fightLinks.json', 'r') as json_file:
        FightLinks = json.load(json_file)
    FightLinks =FightLinks[0:10]
    result = crawl_fight_strike_location_fact(FightLinks)
    result = pd.DataFrame(data=result)
    #fighter on ID for result
    result = result[result.Fight_ID =='f085f32bbb3220e1'].iloc[0].tolist()
    expected_result =[
          '2f5cbecbbe18bac4' #FighterID
        , 'f085f32bbb3220e1'            #FightID
        , 'Shamil Abdurakhimov'    #Fighter0
        , 'Chris Daukaus'          #Fighter1
         # Head_0_Pct,  'Head_1_Pct', 'Body_0_Pct', 'Body_1_Pct', 'Leg_0_Pct', 'Leg_1_Pct','Distance_0_Pct',
        , '56%', '89%', '26%','5%', '17%', '5%','95%',
        # 'Distance_1_Pct', 'Clinch_0_Pct', 'Clinch_1_Pct', 'Ground_0_Pct', 'Ground_1_Pct'
          '47%', '4%', '5%', '0%', '47%'
        ]

    assert result == expected_result, f"crawl_fight_strike_location_fact failed: {result} is not equal to {expected_result}"

#################### Test Best Fight Odds ###########################

def test_crawl_best_fight_odds():
    fighters_list =["/fighters/Israel-Adesanya-7845"]
    result = crawl_odds(fighters_list)
    result = result.iloc[-1].tolist()
    expected_result = [
    "Israel Adesanya vs Rob Wilkinson",      # Matchup
    "+250",                                  # Open
    "+285 ... +305",                         # Closing Range
    "+285",                                  # Close Start Range
    "+305",                                  # Close End Range
    "-2.2%",                                # Movement
    "UFC 221: Romero vs. Rockhold",          # Event
    "Feb 10th 2018"                          # Fight Date
    ]

    assert result == expected_result, f"crawl_odds failed: {result} is not equal to {expected_result}"

#####################################################################