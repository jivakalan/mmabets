import pandas as pd
from selenium.webdriver.common.by import By
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from datetime import date
from tqdm import tqdm

##############################################################################
## Output 1 : odds data for all fighters (fighters come from 5000 fighter IDs
##            scraped from best fight odds) - later only get for active fighters
##############################################################################
def get_table_data(table_rows):

    # Initialize a list to store the table data
    table_data = []
    # Iterate through the rows
    for i in range(1, len(table_rows), 4):
        if i + 3 < len(table_rows):
            # Start a new entry
            current_entry = {
                'Matchup': '',
                'Open': '',
                'Closing Range': '',
                'Close Start Range':'',
                'Close End Range':'',
                'Movement': '',
                'Event': ' ',
                'Fight Date':''
            }
            group = table_rows[i:i + 4]
            for row in group:
                if row.startswith('Created'):
                    continue #skip if Created with info
                if 'n/a' in row:
                    continue

                if row.startswith(('+','-','0')):
                    # Check if the row starts with "+"(indicating "Movement"And "event" fields)
                    if '%' in row:
                        current_entry['Movement'] = row.split()[0].replace('▲', '').replace('▼', '')
                        current_entry['Event'] = ' '.join(row.split()[1:])
                    else:
                        current_entry['Movement'] ='N/A'
                        current_entry['Event'] ='N/A'

                else:
                    ##fighter + odds data
                    current_entry['Open'] = row.split()[2]
                    current_entry['Closing Range'] = ' '.join(row.split()[3:6])
                    current_entry['Fight Date'] = ' '.join(row.split()[6:])
                    current_entry['Close Start Range'] =row.split()[3]
                    current_entry['Close End Range'] =row.split()[5]

                    if len(current_entry['Matchup']) > 1:
                        current_entry['Matchup'] += ' vs ' + ' '.join(row.split()[0:2])
                    else:
                        current_entry['Matchup'] = ' '.join(row.split()[0:2])

            # Append the last entry to table_data
        if current_entry['Matchup']:
            table_data.append(current_entry)

    return table_data

def get_all_profiles_data(browser, fighters_list):
    data_list = []
    error_list = []

    for fighter in tqdm(fighters_list):

        browser.get(f'https://www.bestfightodds.com{fighter}')
        try:
            team_stats_table = browser.find_element(By.CLASS_NAME, 'team-stats-table')
        except Exception as e:
            continue

        table_text = team_stats_table.text
        table_rows = table_text.split('\n')

        try:
            table_data = get_table_data(table_rows)
            data_list.append(table_data)
        except Exception as e:
            error_list.append(fighter)

        # Flatten the list of lists into a single list of dictionaries
        flattened_data = [item for sublist in data_list for item in sublist]

        # Create a DataFrame from the flattened data
        bestOddsDataDf = pd.DataFrame(flattened_data)

    return bestOddsDataDf

def crawl_odds(fighters_list):

    ######## #settings# ######################################
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0")
    chrome_options.add_argument('--headless')
    service = Service(executable_path=GeckoDriverManager().install())
    browser = webdriver.Firefox(options=chrome_options, service=service)
    ####### #execute# ###################################################
    bestOddsDataDf = get_all_profiles_data(browser,fighters_list)
    browser.quit()
    return bestOddsDataDf


