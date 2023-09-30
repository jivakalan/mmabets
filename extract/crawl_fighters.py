import requests
import bs4 as bs
import string
import json
from tqdm import tqdm
from datetime import datetime, timedelta
date_format = "%b. %d, %Y"
##############################################################################
## Output 1 : get the web pages and IDs of all ufc fighters
## Output 2: get the web pages and IDs of all ACTIVE ufc fighters
##############################################################################

def get_alpha_pages():
    alphabet = string.ascii_lowercase
    urls = []
    for letter in alphabet:
        url = "http://ufcstats.com/statistics/fighters?char=%s&page=all" % letter
        urls.append(url)
    return urls

def get_all_ufc_fighterIDs(urls):

    all_fighters = {}
    for url in tqdm(urls):
        r = requests.get(url)
        soup = bs.BeautifulSoup(r.content, 'lxml')
        for a in soup.find_all('a', href=True):
            if "fighter-details" in a['href']:
                if a['href'] not in all_fighters:
                    all_fighters[a['href']] = {}

                    all_fighters[a['href']][a['href'][36:52]] = [a.text]
                else:
                    all_fighters[a['href']][a['href'][36:52]].append(a.text)

    #concat id and names
    for i in all_fighters:
        for j, k in all_fighters[i].items():
            all_fighters[i][j] = ' '.join(k)
    ##all fighters in UFC and IDs
    #with open('extract/data/outputs/ufc_fighterIDs.json', 'w') as json_file:
        #json.dump(all_fighters, json_file)

    return all_fighters


def get_active_fighters(all_fighters, days):

    Active_Fighters = {}

    for url in tqdm(all_fighters.keys()):
        active_fighter = 1
        r = requests.get(url)
        soup = bs.BeautifulSoup(r.content, 'lxml')
        ##find if the fighter is "Active" or not
        container = soup.findAll("tr", {"class",
                                    "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"})
        Fight_Dates = []
        for contain in container:
            fight_date = contain.findAll("td")[6].findAll("p")[1].text.strip()
            Fight_Dates.append(datetime.strptime(fight_date, date_format) )

        if Fight_Dates:
            if max(Fight_Dates) < datetime.now() - timedelta(days):
                active_fighter = 0
        else:
            active_fighter = 0

        Active_Fighters[url]= active_fighter



    Active = []
    for i in Active_Fighters:
        if Active_Fighters[i] == 1:
            Active.append(i)

    #with open('extract/data/outputs/ufc_ActiveFighters.json', 'w') as json_file:
    #    json.dump(Active, json_file)

    return Active_Fighters, Active




