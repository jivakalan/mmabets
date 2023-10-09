from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pickle
from score.tools.helper import *
import unidecode as decode
import json


def get_matchup_data(page_soup):

    upcoming_matchups = []
    for i in page_soup.findAll("td",{"class":"tsp-fr tsp-fnsc"}):
        try:
            matchup =[]
            # Find all <div> elements which contain the fighter names
            name_divs = i.select("div.tsp-dib.tsp-w50.tsp-flr.tsp-lhn.tsp-mh2")

            # Extract names from the found <div> element
            for name_div in name_divs:
                name_spans = name_div.select("span.tsp-dib.tsp-npp.tsp-el.tsp-ffnp")
                name = ' '.join([span.text for span in name_spans])
                matchup.append(name)

            upcoming_matchups.append(matchup)
        except:
            pass
    return upcoming_matchups


# def get_upcoming_fights_pagethrough():
#
#     # Set up the Selenium driver (using Chrome in this example)
#     driver = webdriver.Chrome()
#
#     # Open the webpage
#     driver.get('https://www.google.com/search?q=ufc')
#
#     # Let Selenium fetch the entire web page, including any dynamically loaded content
#     page_html = driver.page_source
#
#     # Identify the link or button to click on, for example using its class name or XPath (modify this according to your needs)
#     #next_button = driver.find_element(By.XPATH, '//a[contains(@class, "some-class-representing-the-button")]')
#     next_button = driver.find_element(By.CLASS_NAME,'WuRuJe')
#
#     # Click on the link/button to navigate to the next page
#     next_button.click()
#
#     # Wait for the new page to load completely (waiting for a specific element that indicates the page has loaded)
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME,'WuRuJe')))
#
#     # Retrieve the HTML content of the new page
#     page_html2 = driver.page_source
#
#     # Click on the link/button to navigate to the next page
#     next_button.click()
#
#     # Wait for the new page to load completely (waiting for a specific element that indicates the page has loaded)
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME,'WuRuJe')))
#
#     # Retrieve the HTML content of the new page
#     page_html3 = driver.page_source
#     driver.close()
#
#     return all_matchups

def get_upcoming_fights():

    # Set up the Selenium driver (using Chrome in this example)
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get('https://www.google.com/search?q=ufc+next+event')

    # Let Selenium fetch the entire web page, including any dynamically loaded content
    page_html = driver.page_source

    # Use BeautifulSoup to parse the page content
    page_soup = BeautifulSoup(page_html, 'html.parser')

    # Always remember to close the driver after you're done
    driver.close()

    upcoming_matchups = []
    for i in page_soup.findAll("td",{"class":"tsp-fr tsp-fnsc"}):
        try:
            matchup =[]
            # Find all <div> elements which contain the fighter names
            name_divs = i.select("div.tsp-dib.tsp-w50.tsp-flr.tsp-lhn.tsp-mh2")

            # Extract names from the found <div> element
            for name_div in name_divs:
                name_spans = name_div.select("span.tsp-dib.tsp-npp.tsp-el.tsp-ffnp")
                name = ' '.join([span.text for span in name_spans])
                matchup.append(name)

            upcoming_matchups.append(matchup)
        except:
            pass

    return upcoming_matchups


def score_fights(upcoming_matchups):

    # Load model
    with open('score/model/xgb_model.pkl','rb') as file:
        xgb_model = pickle.load(file)

    upcoming_matchups_df = pd.DataFrame()
    matches = []
    for match in upcoming_matchups:
        fighter_0 = match[0]
        fighter_1 = match[1]
        fighter_0 = decode.unidecode(fighter_0)
        fighter_1 = decode.unidecode(fighter_1)
        # lookup fighter metrics and construct the match up
        try:
            record, match = create_scoring_record(fighter_0, fighter_1)
            # create df from record
            record_df = pd.DataFrame()
            for component in record:
                record_df = pd.concat([record_df, component], axis=1)
            upcoming_matchups_df = pd.concat([upcoming_matchups_df, record_df])
            matches.append(match)

        except:
            pass

    #get predicted probabilty
    prediction = xgb_model.predict_proba(upcoming_matchups_df)

    return prediction, matches



upcoming_matchups = get_upcoming_fights()
predictions, matches = score_fights(upcoming_matchups)
predictions = predictions.tolist()

with open('score/data/outputs/predictions.json','w') as file:
    json.dump(predictions,file)
with open('endpoint/data/predictions.json','w') as file:
    json.dump(predictions,file)

with open('score/data/outputs/matchups.json','w') as file:
    json.dump(matches,file)
with open('endpoint/data/matchups.json','w') as file:
    json.dump(matches,file)
