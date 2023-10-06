#####################################################################
##                          Imports                              ###
#####################################################################
from extract.crawl_fighters import *                               #
import os                                                          #
import logging                                                     #
from extract.crawl_best_fight_odds import *                        #
from extract.crawl_ufc_fight_data import *                         #
from extract.crawl_ufc_fight_data_detail import *                  #
from extract.tools.helper import save_json, load_json              #
####################################################################

def upsert_to_csv(existing_csv_file, new_data_df, key_column):
    # Load existing CSV data into a DataFrame
    try:
        existing_df = pd.read_csv(existing_csv_file)
        print(existing_df.shape)
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=new_data_df.columns)

    # Merge the existing data with the new data and remove duplicates based on the key column
    merged_df = pd.concat([existing_df, new_data_df], ignore_index=True)

    if len(key_column)>1:
        # Combine the key columns in the new_data_df to create a single key column
        merged_df['Combined_Key'] = ''
        for key in key_column:
            print(key)
            merged_df['Combined_Key'] += merged_df[key].astype(str)

        key_column ='Combined_Key'

        merged_df.drop_duplicates(subset=key_column, keep='last', inplace=True)
        merged_df = merged_df.drop(columns='Combined_Key')
    else:
        merged_df.drop_duplicates(subset=key_column, keep='last', inplace=True)

    # Save the merged DataFrame back to the CSV file
    merged_df.to_csv(existing_csv_file, index=False)
    print(merged_df.shape)

    return merged_df

def upsert_all_data(data, environment= 'production'):
    config = load_json("extract/tools/config.json")
    filepaths = config[environment]['filepaths']
    primary_keys = config['primary_keys']
    pipeline_files = config['index']

    for i in range(0, len(pipeline_files)):
        filename = filepaths[i].split("/")[-1].split(".")[0]

        existing_csv_file = filepaths[i]
        new_data_df = data[filename]
        key_column = primary_keys[i]

        try:
            upsert_to_csv(existing_csv_file, new_data_df, key_column)
        except:
            pass
    return

def run_fight_data(data, alphabetic_fighter_list_urls, env ='production'):

    # get fighter dim
    fighter_links, fighter_dim = crawl_fighterDim(alphabetic_fighter_list_urls)
    fighter_dim = pd.DataFrame(data=fighter_dim)
    data['fighter_dim'] = fighter_dim

    # save required output
    save_json('extract/data/outputs/fighterDimLinks.json', fighter_links)

    # use unit test if needed
    if env =='testing':
        fighter_links = ['http://ufcstats.com/fighter-details/1338e2c7480bdf9e']

    # get fight outcome fact
    fight_outcome_fact = crawl_FightOutcomeFact(fighter_links)
    fight_outcome_fact = pd.DataFrame(data=fight_outcome_fact)
    data['fight_outcome_fact'] = fight_outcome_fact

    return data

def run_fight_detail(data, fight_links):

    # crawl ufc fight data detail
    main_fight_fact = crawl_main_fight_fact(fight_links)
    main_fight_fact = pd.DataFrame(data=main_fight_fact)

    fighter_record_fact = crawl_fighter_record_fact(fight_links)
    fighter_record_fact = pd.DataFrame(data=fighter_record_fact)

    fight_strike_location_fact = crawl_fight_strike_location_fact(fight_links)
    fight_strike_location_fact = pd.DataFrame(data=fight_strike_location_fact)

    data['main_fight_fact'] = main_fight_fact
    data['fighter_record_fact'] = fighter_record_fact
    data['fight_strike_location_fact'] = fight_strike_location_fact

    return data

def run_pipeline(inits):

    alphabetic_fighter_list_urls=inits[0]
    fight_links = inits[1]
    odds_fighters_list = inits[2]

    data = {}

    # get fight data
    run_fight_data(data, alphabetic_fighter_list_urls)

    # get fight detail
    run_fight_detail(data, fight_links)

    # get best fight odds data
    fight_odds_fact = crawl_odds(odds_fighters_list)
    data['fight_odds_fact'] = fight_odds_fact

    return data

def crawler(active=0, update=0, environment ='production'):
    # load alpha pages
    alphabetic_fighter_list_urls = load_json('extract/data/outputs/alphabetic_fighter_list_urls.json')

    if environment == 'testing':
        alphabetic_fighter_list_urls = [alphabetic_fighter_list_urls[12]]

    if update == 0 and active == 0:
        # Simple ReRun of Pipeline for all fighters
        # pick up fight_links from outputs
        fight_links = load_json(r'extract\data\outputs\fightLinks.json')
        if environment == 'testing':
            fight_links = fight_links[0:5]

        # load fighter odds pages
        fighters_odds_list = load_json('extract/data/outputs/bestoddfighters.json')
        if environment == 'testing':
            fighters_odds_list = ["/fighters/Israel-Adesanya-7845"]

        inits = [alphabetic_fighter_list_urls, fight_links, fighters_odds_list]

        # run the pipeline
        all_df = run_pipeline(inits)

    # update all fights for active fighters (last fight > 365 days)
    if update == 0 and active == 1:
        # pick up active fight_links from outputs
        active_fight_links = load_json(r'extract\data\outputs\fightLinks.json')
        # todo: active_fight_links
        if environment == 'testing':
            active_fight_links = active_fight_links[0:5]

        # load fighter odds pages
        active_odds_fighters = load_json('extract/data/outputs/bestoddfighters.json') #
        # todo: active_odds_fighters
        if environment == 'testing':
            active_odds_fighters = ["/fighters/Israel-Adesanya-7845"]

        inits = [alphabetic_fighter_list_urls, active_fight_links, active_odds_fighters]

        # run the pipeline
        all_df = run_pipeline(inits)

    # if update == 1 and active == 1:
        # todo: if last modified date is more than 1 month old...update active fighter list
        # alldf = run_pipeline(data)

    # if update == 1 and active == 0:
        # todo: Initiate fresh scrape of UFC website for all fighter IDs; this will take the longest time

    # upsert all data
    upsert_all_data(all_df)

    return


