from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
from tqdm import tqdm
import json
#import pandas as pd
import urllib.request
import socket
#import os
#import datetime
#from extract.crawl_fighters import *
date_format = "%b. %d, %Y"

def make_request(url, max_retries=3, timeout=5):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Define headers
    retries = 0
    while retries < max_retries:
        try:
            req = urllib.request.Request(url, headers=headers)  # Create Request object with headers
            response = urllib.request.urlopen(req, timeout=timeout)  # Make the request
            return response
        except socket.timeout:
            print("Request timed out. Retrying...")
            retries += 1

    print("Exceeded maximum retries. Unable to establish connection.")
    return None


def generate_alphabetic_fighter_list_urls():
    ## gets all the links to UFC page - alphabetic directory of UFc fighters -
    # ## each page holds all the fighters with last name corresponding to the ith letter of the alphabet
    ## and also has their fighter dim data alongside, this data will be scraped in crawl_fighterDim

    alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
              'w', 'x', 'y', 'z', ]
    alphabetic_fighter_list_urls=[]
    for alpha in tqdm(alphas, desc="Progress of Fighter Dim"):
        url= 'http://ufcstats.com/statistics/fighters?char=' + alpha + '&page=all'
        alphabetic_fighter_list_urls.append(url)

    with open('extract/data/outputs/alphabetic_fighter_list_urls.json', 'w') as json_file:
        json.dump(alphabetic_fighter_list_urls, json_file)

    return alphabetic_fighter_list_urls


def crawl_fighterDim(alphabetic_fighter_list_urls):

    #################################################
    ## construct fighter DIM
    ###################################################

    FighterLink = []
    Fighter_ID = []
    Fighter_name = []
    HT = []
    WT = []
    REACH = []
    STANCE = []
    W = []
    L = []
    D = []
    BELT = []


    #with open('extract/data/outputs/alphabetic_fighter_list_urls.json', 'r') as json_file:
        #alphabetic_fighter_list_urls = json.load(json_file)

    for main_url in tqdm(alphabetic_fighter_list_urls, desc='Progress of FighterDim'):

        req = Request(main_url, headers={'User-Agent': 'Mozilla/5.0'})
        page_html = uReq(req).read()
        page_soup = soup(page_html, "html.parser")
        for flink in page_soup.findAll("tr", {"class", "b-statistics__table-row"})[2:]:
            fighterlink = flink.td.a['href']
            FighterLink.append(fighterlink)

            fighter_ID = fighterlink.split("/")[-1]
            Fighter_ID.append(fighter_ID)

            first = flink.findAll("a")[0].text
            second = flink.findAll("a")[1].text
            fighter_name = first + " " + second
            Fighter_name.append(fighter_name)

            ht = flink.findAll("td")[3].text.strip()
            HT.append(ht)
            wt = flink.findAll("td")[4].text.strip()
            WT.append(wt)
            reach = flink.findAll("td")[5].text.strip()
            REACH.append(reach)
            stance = flink.findAll("td")[6].text.strip()
            STANCE.append(stance)
            w = flink.findAll("td")[7].text.strip()
            W.append(w)
            l = flink.findAll("td")[8].text.strip()
            L.append(l)
            d = flink.findAll("td")[9].text.strip()
            D.append(d)
            belt = flink.findAll("td")[10].text.strip()
            BELT.append(belt)

    #save fighter LINKS output
    #with open('extract/data/outputs/fighterDimLinks.json', 'w') as json_file:
     #  json.dump(FighterLink, json_file)

    data1_fighterID = []
    for i in FighterLink:
        data1_fighterID.append(i[-16:])

    data1 = {'Fighter_ID': data1_fighterID, 'Fighter_name': Fighter_name, 'HT': HT, 'WT': WT, 'REACH': REACH,
             'STANCE': STANCE, 'W': W, 'L': L, 'D': D, 'BELT': BELT, }

    return FighterLink, data1


def crawl_FightOutcomeFact(FighterLink):

    FightLink = []
    Fighter_ID = []
    Fight_ID = []
    Result = []
    Fight_Name = []
    Fight_Date = []
    METHOD = []
    ROUND = []
    TIME = []
    data2_fighterID = []

    # if update == 0:
    #     #LOAD fighterIDs output
    #     with open('extract/data/outputs/fighterDimLinks.json', 'r') as json_file:
    #         FighterLink = json.load(json_file)
    # if update == 1:
    #     #load only activefighters
    #     with open('extract/data/outputs/ufc_ActiveFighters.json', 'r') as json_file:
    #         FighterLink = json.load(json_file)


    for fl in tqdm(FighterLink, desc='Progress of FightOutcomeFact'):
        fighter_url = fl

        req2 = Request(fighter_url, headers={'User-Agent': 'Mozilla/5.0'})
        page_html2 = uReq(req2).read()
        page_soup2 = soup(page_html2, "html.parser")
        page_soup2.findAll("a", {"class", "b-flag b-flag_style_green"})
        fighter_ID = fighter_url.split("/")[-1]
        container = page_soup2.findAll("tr", {"class",
                                              "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"})
        for contain in container:
            Fighter_ID.append(fighter_ID)
            data2_fighterID.append(fighter_ID)
            fightlink = contain.a['href']
            FightLink.append(fightlink)
            fight_ID = fightlink.split("/")[-1]
            Fight_ID.append(fight_ID)
            result = contain.a.text
            Result.append(result)
            fight_name = contain.findAll("td")[6].p.text.strip()
            Fight_Name.append(fight_name)
            fight_date = contain.findAll("td")[6].findAll("p")[1].text.strip()
            Fight_Date.append(fight_date)
            method = contain.findAll("td")[7].p.text.strip()
            METHOD.append(method)
            roundd = contain.findAll("td")[8].text.strip()
            ROUND.append(roundd)
            ftime = contain.findAll("td")[9].text.strip()
            TIME.append(ftime)

    data2 = {'Fighter_ID': data2_fighterID, 'Fight_ID': Fight_ID, 'Result': Result, 'Fight_Name': Fight_Name,
             'Fight_Date': Fight_Date,
             'METHOD': METHOD, 'ROUND': ROUND, 'TIME': TIME, }


    return data2




