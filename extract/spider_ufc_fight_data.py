from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

FighterLink = []
FightLink = []

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

Fighterr_ID = []
Fight_ID = []
Result = []
Fight_Name = []
Fight_Date = []
METHOD = []
ROUND = []
TIME = []

alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
          'w', 'x', 'y', 'z', ]
for alpha in alphas:
    main_url = 'http://ufcstats.com/statistics/fighters?char=' + alpha + '&page=all'
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
    print(main_url)

for fl in FighterLink:
    fighter_url = fl
    req2 = Request(fighter_url, headers={'User-Agent': 'Mozilla/5.0'})
    page_html2 = uReq(req2).read()
    page_soup2 = soup(page_html2, "html.parser")
    page_soup2.findAll("a", {"class", "b-flag b-flag_style_green"})
    fighterr_ID = fighter_url.split("/")[-1]
    container = page_soup2.findAll("tr", {"class",
                                          "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click"})
    for contain in container:
        Fighterr_ID.append(fighterr_ID)
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
        time = contain.findAll("td")[9].text.strip()
        TIME.append(time)
        print(fight_ID, "     ", time)

data1 = {'Fighter_ID': Fighter_ID, 'Fighter_name': Fighter_name, 'HT': HT, 'WT': WT, 'REACH': REACH,
         'STANCE': STANCE, 'W': W, 'L': L, 'D': D, 'BELT': BELT, }
df1 = pd.DataFrame(data=data1)
df1.index += 1
df1.to_excel("~/Desktop/Main_page.xlsx")

data2 = {'Fighterr_ID': Fighterr_ID, 'Fight_ID': Fight_ID, 'Result': Result, 'Fight_Name': Fight_Name,
         'Fight_Date': Fight_Date,
         'METHOD': METHOD, 'ROUND': ROUND, 'TIME': TIME, }
df2 = pd.DataFrame(data=data2)
df2.index += 1
df2.to_excel("~/Desktop/Fighter_Page.xlsx")
