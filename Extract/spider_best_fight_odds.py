import pandas as pd
from selenium.webdriver.common.by import By
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


class Fighters(object):

    def __init__(self):
        self.fighters_list = []
        self.data_list = []
        self.chrome_options = Options()
        self.chrome_options.add_argument(
            "--user-agent=Mozilla/5.0")
        self.chrome_options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=self.chrome_options, executable_path=GeckoDriverManager().install())
        self.get_all_profiles_data(self.browser)
        # self.searching_and_scraping_agencies()
        # self.click_open_scrap_agency(agency)
        # self.compare_all_pdf_with_title_write_pdf()

    def get_all_profiles_data(self, browser):
        f = open('fighters.json')
        self.fighters_list = json.load(f)
        for iter_index, fighter in enumerate(self.fighters_list):
            fighter_id = fighter[10:]
            print(fighter_id)
            browser.get(f'https://www.bestfightodds.com{fighter}')
            # player_name = browser.find_element(By.ID, 'team-name').text
            try:
                team_stats_table = browser.find_element(By.CLASS_NAME, 'team-stats-table')
            except:
                continue
            table_rows = team_stats_table.find_elements_by_tag_name('tr')[1:]
            step_forward = False
            for i in range(0, len(table_rows)):
                if i == 0 or i % 3 == 0:
                    continue
                if step_forward:
                    step_forward = False
                    continue
                else:
                    try:
                        player_name = table_rows[i].find_element(By.XPATH, '//th/a').text
                    except:
                        player_name = 'N/A'
                    try:
                        open_text = table_rows[i].find_elements_by_tag_name('td')[0].text
                    except:
                        open_text = 'N/A'
                    try:
                        clossing_range_lower = table_rows[i].find_elements_by_tag_name('td')[1].text
                    except:
                        clossing_range_lower = 'N/A'
                    try:
                        clossing_range_upper = table_rows[i].find_elements_by_tag_name('td')[3].text
                    except:
                        clossing_range_upper = 'N/A'
                    try:
                        event_name = table_rows[i].find_elements_by_tag_name('td')[6].text
                    except:
                        event_name = ''
                    try:
                        opponent_name = table_rows[i+1].find_element_by_tag_name('th').find_element_by_tag_name('a').text
                    except:
                        opponent_name = 'N/A'
                    try:
                        opponent_open_text = table_rows[i+1].find_elements_by_tag_name('td')[0].text
                    except:
                        opponent_open_text = 'N/A'
                    try:
                        opponent_clossing_range_lower = table_rows[i+1].find_elements_by_tag_name('td')[1].text
                    except:
                        opponent_clossing_range_lower = 'N/A'
                    try:
                        opponent_clossing_range_upper = table_rows[i+1].find_elements_by_tag_name('td')[3].text
                    except:
                        opponent_clossing_range_upper = 'N/A'
                    try:
                        event_date = table_rows[i+1].find_elements_by_tag_name('td')[4].text
                        if not event_date:
                            event_date = 'N/A'
                    except:
                        event_date = 'N/A'
                    step_forward = True
                    self.data_list.append([iter_index,fighter_id, player_name, open_text, clossing_range_lower, clossing_range_upper, event_name, event_date, opponent_name, opponent_open_text, opponent_clossing_range_lower, opponent_clossing_range_upper])

        agents_data = pd.DataFrame(self.data_list, columns=['Index', 'ID', 'Fighter Name', 'Open', 'Close_range_lower', 'Close_range_upper',
                                                            'Event_name', 'Event_Date', 'Opponent_Name', 'Opponent_Open', 'Opponent_close_range_lower', 'Opponent_close_range_upper'])
        agents_data.to_csv('data/fighter_test.csv')


if __name__ == "__main__":
    fathom = Fighters()





