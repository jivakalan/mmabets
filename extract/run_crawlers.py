from extract.crawl_best_fight_odds import *
from extract.crawl_ufc_fight_data import *
from extract.crawl_ufc_fight_data_detail import *
import logging
import os

logging.basicConfig(filename='UFC pipeline.log'
                    , level=logging.INFO
                    , format='%(asctime)s - %(levelname)s: %(message)s')


def update_csv(data, file_path):
    file_directory = r'extract\\data\\database\\'
    df = pd.DataFrame(data=data)
    df.to_csv(file_directory+file_path, mode='a'
              , header=False, index=False)
    return

def run_component(component_name, component_function):
    try:
        component_function.init()
        print(f"{component_name} completed successfully.")
        return
    except Exception as e:
        print(f"Error in {component_name}: {e}")
        return None








def crawler(active=0, update=0):

    if update ==0 and active == 1:
        # update fights for current active fighters
        file_path =r'extract\data\outputs\ufc_ActiveFighters.json'
        timestamp = os.path.getmtime(file_path)
        last_modified_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        print('Updating fights for active UFC fighters as of:', last_modified_date)

        with open(file_path, 'r') as json_file:
            activeFighterIds = json.load(json_file)

        fighterDim       = crawl_fighterDim(activeFighterIds)
        fighterOutcome   = crawl_FightOutcomeFact(activeFighterIds)

        fightIds = crawl_FightData(activeFighterIds)
        main_fight_fact, fighter_record_fact, fight_strike_location_fact = crawl_main_fight_and_strike_and_record_fact(fightIds)

        update_csv(fighterDim, 'fighter_dim.csv')
        update_csv(fighterOutcome,'fight_outcome_fact.csv')

        update_csv(main_fight_fact, 'main_fight_fact.csv')
        update_csv(fighter_record_fact, 'fighter_record_fact.csv')
        update_csv(fight_strike_location_fact, 'fight_strike_location_fact.csv')

    if update == 1 and active == 1:

        #use updated list of active fighter IDs and update fighterDim + fighterOutcome
        fighterIds       = list(get_all_ufc_fighterIDs().keys())
        activeFighterIds = get_active_fighters(fighterIds)

        fighterDim       = crawl_fighterDim(activeFighterIds)
        fighterOutcome   = crawl_FightOutcomeFact(activeFighterIds)

        fightIds    =  crawl_FightData(activeFighterIds)
        newfightIds = fights_to_update(fightIds)
        main_fight_fact, fighter_record_fact, fight_strike_location_fact = crawl_main_fight_and_strike_and_record_fact(newfightIds)

        update_csv(fighterDim, 'fighter_dim.csv')
        update_csv(fighterOutcome,'fight_outcome_fact.csv')
        update_csv(main_fight_fact, 'main_fight_fact.csv')
        update_csv(fighter_record_fact, 'fighter_record_fact.csv')
        update_csv(fight_strike_location_fact, 'fight_strike_location_fact.csv')

    if update == 0 and active == 0:
        # If update == 0, then use all fighter IDs from outputs folder
        # would just be rerunning the pipeline for all fighters...database rebuild

        file_path ='extract/data/outputs/ufc_fighterIDs.json'
        timestamp = os.path.getmtime(file_path)
        last_modified_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

        print('Updating fights for all UFC fighters as of:', last_modified_date)

        with open(file_path, 'r') as json_file:
            fighterIds = json.load(json_file)

        fighterIds = list(fighterIds.keys())

        fighterDim     = crawl_fighterDim(fighterIds)
        fighterOutcome = crawl_FightOutcomeFact(fighterIds)

        update_csv(fighterDim, 'fighter_dim.csv')
        update_csv(fighterOutcome,'fight_outcome_fact.csv')
        update_csv(main_fight_fact, 'main_fight_fact.csv')
        update_csv(fighter_record_fact, 'fighter_record_fact.csv')
        update_csv(fight_strike_location_fact, 'fight_strike_location_fact.csv')

    if update == 1 and active == 0:
        #Initiate fresh scrape of UFC website for all fighter IDs
        #new fighters arrive
        fighterIds     = list(get_all_ufc_fighterIDs().keys())
        ##with updated (all) FighterIDs, update fighterDim+fighterOutcome
        fighterDim     = crawl_fighterDim(fighterIds)
        fighterOutcome = crawl_FightOutcomeFact(fighterIds)

        update_csv(fighterDim, 'fighter_dim.csv')
        update_csv(fighterOutcome,'fight_outcome_fact.csv')
        update_csv(main_fight_fact, 'main_fight_fact.csv')
        update_csv(fighter_record_fact, 'fighter_record_fact.csv')
        update_csv(fight_strike_location_fact, 'fight_strike_location_fact.csv')
    return


# if active == 0:
#    bestOddsDataDf.to_csv('extract/data/database/fight_odds_fact.csv', index=False)
# else:
#    bestOddsDataDf.to_csv('extract/data/database/fight_odds_fact.csv', mode='a'
#                         ,header=False, index = False)

run_component(crawler)
run_component(crawl_odds)