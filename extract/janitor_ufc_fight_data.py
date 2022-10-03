from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd
import time

Fighter_ID = []
Fight_ID = []
Fight_Name = []
Round = []
Knockdowns_0 = []
Knockdowns_1 = []
Significant_Strikes_0 = []
Significant_Strikes_1 = []
Significant_Strike_pct_0 = []
Significant_Strike_pct_1 = []
Total_Strikes_0 = []
Total_Strikes_1 = []
Head_0 = []
Head_1 = []
Body_0 = []
Body_1 = []
Legs_0 = []
Legs_1 = []
Distance_0 = []
Distance_1 = []
Clinch_0 = []
Clinch_1 = []
Ground_0 = []
Ground_1 = []
Takedowns_0 = []
Takedowns_1 = []
Takedown_pct_0 = []
Takedown_pct_1 = []
Submission_Attempt_0 = []
Submission_Attempt_1 = []
Rev_0 = []
Rev_1 = []
Control_Time_0 = []
Control_Time_1 = []

Fighters_ID = []
Fights_ID = []
Fights_Name = []
Weight_Class = []
Opponent = []
Method = []
Round_End = []
Time_End = []
Fight_format = []
Referee = []
Details = []

Fighterss_ID = []
Fightss_ID = []
Fighter_0 = []
Fighter_1 = []
Head_0_Pct = []
Head_1_Pct = []
Body_0_Pct = []
Body_1_Pct = []
Leg_0_Pct = []
Leg_1_Pct = []
Distance_0_Pct = []
Distance_1_Pct = []
Clinch_0_Pct = []
Clinch_1_Pct = []
Ground_0_Pct = []
Ground_1_Pct = []

urls = ['http://ufcstats.com/fight-details/fd76b75c28dc247a',
        'http://ufcstats.com/fight-details/1f2f27b36e79da74',
        'http://ufcstats.com/fight-details/cb1e57b5f8c92922',
        'http://ufcstats.com/fight-details/7de9867b7cc2b1b1',
        ]

FighterLink = []
FightLink = []
Fighterr_ID = []
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
        print(fightlink)

for url in FightLink:
    req1 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page_html1 = uReq(req1).read()
    page_soup1 = soup(page_html1, "html.parser")

    try:
        fighter_ID = page_soup1.findAll("a", {"class", "b-link b-fight-details__person-link"})[0]['href'].split('/')[-1]
    except:
        fighter_ID = ''
    try:
        fight_ID = url.split('/')[-1]
    except:
        fight_ID = ''

    try:
        fight_name = page_soup1.findAll("h2", {"class", "b-content__title"})[0].text.strip()
    except:
        fight_name = ''
    roundlenght = len(
        page_soup1.findAll("thead", {"class", "b-fight-details__table-row b-fight-details__table-row_type_head"})) // 2
    for r in range(0, roundlenght):
        Fighter_ID.append(fighter_ID)
        Fight_ID.append(fight_ID)
        Fight_Name.append(fight_name)
        rounnd = r + 1
        Round.append(rounnd)
        try:
            knockdown_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[1].findAll("p")[
                0].text.strip()
            Knockdowns_0.append(knockdown_0)
        except:
            knockdown_0 = ''
            Knockdowns_0.append(knockdown_0)
        try:
            knockdown_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[1].findAll("p")[
                1].text.strip()
            Knockdowns_1.append(knockdown_1)
        except:
            knockdown_1 = ''
            Knockdowns_1.append(knockdown_1)
        try:
            significant_strikes_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[2].findAll("p")[
                0].text.strip().split()[0]
            Significant_Strikes_0.append(significant_strikes_0)
        except:
            significant_strikes_0 = ''
            Significant_Strikes_0.append(significant_strikes_0)
        try:
            significant_strikes_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[2].findAll("p")[
                1].text.strip().split()[0]
            Significant_Strikes_1.append(significant_strikes_1)
        except:
            significant_strikes_1 = ''
            Significant_Strikes_1.append(significant_strikes_1)
        try:
            significant_strike_pct_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[3].findAll("p")[
                0].text.strip()
            Significant_Strike_pct_0.append(significant_strike_pct_0)
        except:
            significant_strike_pct_0 = ''
            Significant_Strike_pct_0.append(significant_strike_pct_0)
        try:
            significant_strike_pct_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[3].findAll("p")[
                1].text.strip()
            Significant_Strike_pct_1.append(significant_strike_pct_1)
        except:
            significant_strike_pct_1 = ''
            Significant_Strike_pct_1.append(significant_strike_pct_1)
        try:
            total_strikes_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[4].findAll("p")[
                0].text.strip().split()[2]
            Total_Strikes_0.append(total_strikes_0)
        except:
            total_strikes_0 = ''
            Total_Strikes_0.append(total_strikes_0)
        try:
            total_strikes_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[4].findAll("p")[
                1].text.strip().split()[2]
            Total_Strikes_1.append(total_strikes_1)
        except:
            total_strikes_1 = ''
            Total_Strikes_1.append(total_strikes_1)

        try:
            head_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                3].findAll("p")[0].text.strip().split()[0]
            Head_0.append(head_0)
        except:
            head_0 = ''
            Head_0.append(head_0)
        try:
            head_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                3].findAll("p")[1].text.strip().split()[0]
            Head_1.append(head_1)
        except:
            head_1 = ''
            Head_1.append(head_1)
        try:
            body_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                4].findAll("p")[0].text.strip().split()[0]
            Body_0.append(body_0)
        except:
            body_0 = ''
            Body_0.append(body_0)
        try:
            body_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                4].findAll("p")[1].text.strip().split()[0]
            Body_1.append(body_1)
        except:
            body_1 = ''
            Body_1.append(body_1)
        try:
            legs_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                5].findAll("p")[0].text.strip().split()[0]
            Legs_0.append(legs_0)
        except:
            legs_0 = ''
            Legs_0.append(legs_0)
        try:
            legs_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                5].findAll("p")[1].text.strip().split()[0]
            Legs_1.append(legs_1)
        except:
            legs_1 = ''
            Legs_1.append(legs_1)
        try:
            distance_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                6].findAll("p")[0].text.strip().split()[0]
            Distance_0.append(distance_0)
        except:
            distance_0 = ''
            Distance_0.append(distance_0)
        try:
            distance_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                6].findAll("p")[1].text.strip().split()[0]
            Distance_1.append(distance_1)
        except:
            distance_1 = ''
            Distance_1.append(distance_1)
        try:
            clinch_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                7].findAll("p")[0].text.strip().split()[0]
            Clinch_0.append(clinch_0)
        except:
            clinch_0 = ''
            Clinch_0.append(clinch_0)
        try:
            clinch_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                7].findAll("p")[1].text.strip().split()[0]
            Clinch_1.append(clinch_1)
        except:
            clinch_1 = ''
            Clinch_1.append(clinch_1)
        try:
            ground_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                8].findAll("p")[0].text.strip().split()[0]
            Ground_0.append(ground_0)
        except:
            ground_0 = ''
            Ground_0.append(ground_0)
        try:
            ground_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[6 + roundlenght + r].findAll("td")[
                8].findAll("p")[1].text.strip().split()[0]
            Ground_1.append(ground_1)
        except:
            ground_1 = ''
            Ground_1.append(ground_1)

        try:
            takedowns_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[5].findAll("p")[
                0].text.strip().split()[0]
            Takedowns_0.append(takedowns_0)
        except:
            takedowns_0 = ''
            Takedowns_0.append(takedowns_0)
        try:
            takedowns_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[5].findAll("p")[
                1].text.strip().split()[0]
            Takedowns_1.append(takedowns_1)
        except:
            takedowns_1 = ''
            Takedowns_1.append(takedowns_1)
        try:
            takedown_pct_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[6].findAll("p")[
                0].text.strip()
            Takedown_pct_0.append(takedown_pct_0)
        except:
            takedown_pct_0 = ''
            Takedown_pct_0.append(takedown_pct_0)
        try:
            takedown_pct_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[6].findAll("p")[
                1].text.strip()
            Takedown_pct_1.append(takedown_pct_1)
        except:
            takedown_pct_1 = ''
            Takedown_pct_1.append(takedown_pct_1)
        try:
            submission_attempt_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[7].findAll("p")[
                0].text.strip()
            Submission_Attempt_0.append(submission_attempt_0)
        except:
            submission_attempt_0 = ''
            Submission_Attempt_0.append(submission_attempt_0)
        try:
            submission_attempt_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[7].findAll("p")[
                1].text.strip()
            Submission_Attempt_1.append(submission_attempt_1)
        except:
            submission_attempt_1 = ''
            Submission_Attempt_1.append(submission_attempt_1)
        try:
            rev_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[8].findAll("p")[
                0].text.strip()
            Rev_0.append(rev_0)
        except:
            rev_0 = ''
            Rev_0.append(rev_0)
        try:
            rev_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[8].findAll("p")[
                1].text.strip()
            Rev_1.append(rev_1)
        except:
            rev_1 = ''
            Rev_1.append(rev_1)
        try:
            control_time_0 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[9].findAll("p")[
                0].text.strip()
            Control_Time_0.append(control_time_0)
        except:
            control_time_0 = ''
            Control_Time_0.append(control_time_0)
        try:
            control_time_1 = \
            page_soup1.findAll("tr", {"class", "b-fight-details__table-row"})[3 + r].findAll("td")[9].findAll("p")[
                1].text.strip()
            Control_Time_1.append(control_time_1)
        except:
            control_time_1 = ''
            Control_Time_1.append(control_time_1)

    print(fight_name, "   ", fight_ID)

    Fighters_ID.append(fighter_ID)
    Fights_ID.append(fight_ID)
    Fights_Name.append(fight_name)

    try:
        weight_class = page_soup1.findAll("i", {"class", "b-fight-details__fight-title"})[0].text.strip()
        Weight_Class.append(weight_class)
    except:
        weight_class = ''
        Weight_Class.append(weight_class)
    try:
        opponent = page_soup1.findAll("h3", {"class", "b-fight-details__person-name"})[1].text.strip()
        Opponent.append(opponent)
    except:
        opponent = ''
        Opponent.append(opponent)
    try:
        method = page_soup1.findAll("i", {"class", "b-fight-details__text-item_first"})[0].findAll("i")[1].text.strip()
        Method.append(method)
    except:
        method = ''
        Method.append(method)
    try:
        round_End = page_soup1.findAll("i", {"class", "b-fight-details__text-item"})[0].text.strip().split()[-1]
        Round_End.append(round_End)
    except:
        round_End = ''
        Round_End.append(round_End)
    try:
        time_End = page_soup1.findAll("i", {"class", "b-fight-details__text-item"})[1].text.strip().split()[-1]
        Time_End.append(time_End)
    except:
        time_End = ''
        Time_End.append(time_End)
    try:
        fight_format = \
        page_soup1.findAll("i", {"class", "b-fight-details__text-item"})[2].text.strip().replace("\n     ", "").split(
            ":")[-1]
        Fight_format.append(fight_format)
    except:
        fight_format = ''
        Fight_format.append(fight_format)
    try:
        referee = \
        page_soup1.findAll("i", {"class", "b-fight-details__text-item"})[3].text.strip().replace("\n", "").split(":")[
            -1].replace("  ", "")
        Referee.append(referee)
    except:
        referee = ''
        Referee.append(referee)
    try:
        details = page_soup1.findAll("p", {"class", "b-fight-details__text"})[-1].text.replace("\n", "").split(":")[
            -1].replace("  ", "")
        Details.append(details)
    except:
        details = ''
        Details.append(details)

    Fighterss_ID.append(fighter_ID)
    Fightss_ID.append(fight_ID)

    try:
        fighter_0 = page_soup1.findAll("h3", {"class", "b-fight-details__person-name"})[0].text.strip()
        Fighter_0.append(fighter_0)
    except:
        fighter_0 = ''
        Fighter_0.append(fighter_0)
    try:
        fighter_1 = page_soup1.findAll("h3", {"class", "b-fight-details__person-name"})[1].text.strip()
        Fighter_1.append(fighter_1)
    except:
        fighter_1 = ''
        Fighter_1.append(fighter_1)
    try:
        head_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[0].findAll("i")[0].text.strip()
        Head_0_Pct.append(head_0_Pct)
    except:
        head_0_Pct = ''
        Head_0_Pct.append(head_0_Pct)
    try:
        head_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[0].findAll("i")[2].text.strip()
        Head_1_Pct.append(head_1_Pct)
    except:
        head_1_Pct = ''
        Head_1_Pct.append(head_1_Pct)
    try:
        body_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[1].findAll("i")[0].text.strip()
        Body_0_Pct.append(body_0_Pct)
    except:
        body_0_Pct = ''
        Body_0_Pct.append(body_0_Pct)
    try:
        body_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[1].findAll("i")[2].text.strip()
        Body_1_Pct.append(body_1_Pct)
    except:
        body_1_Pct = ''
        Body_1_Pct.append(body_1_Pct)
    try:
        leg_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[2].findAll("i")[0].text.strip()
        Leg_0_Pct.append(leg_0_Pct)
    except:
        leg_0_Pct = ''
        Leg_0_Pct.append(leg_0_Pct)
    try:
        leg_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[2].findAll("i")[2].text.strip()
        Leg_1_Pct.append(leg_1_Pct)
    except:
        leg_1_Pct = ''
        Leg_1_Pct.append(leg_1_Pct)
    try:
        distance_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[3].findAll("i")[
            0].text.strip()
        Distance_0_Pct.append(distance_0_Pct)
    except:
        distance_0_Pct = ''
        Distance_0_Pct.append(distance_0_Pct)
    try:
        distance_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[3].findAll("i")[
            2].text.strip()
        Distance_1_Pct.append(distance_1_Pct)
    except:
        distance_1_Pct = ''
        Distance_1_Pct.append(distance_1_Pct)
    try:
        clinch_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[4].findAll("i")[
            0].text.strip()
        Clinch_0_Pct.append(clinch_0_Pct)
    except:
        clinch_0_Pct = ''
        Clinch_0_Pct.append(clinch_0_Pct)
    try:
        clinch_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[4].findAll("i")[
            2].text.strip()
        Clinch_1_Pct.append(clinch_1_Pct)
    except:
        clinch_1_Pct = ''
        Clinch_1_Pct.append(clinch_1_Pct)
    try:
        ground_0_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[5].findAll("i")[
            0].text.strip()
        Ground_0_Pct.append(ground_0_Pct)
    except:
        ground_0_Pct = ''
        Ground_0_Pct.append(ground_0_Pct)
    try:
        ground_1_Pct = page_soup1.findAll("div", {"class", "b-fight-details__charts-row"})[5].findAll("i")[
            2].text.strip()
        Ground_1_Pct.append(ground_1_Pct)
    except:
        ground_1_Pct = ''
        Ground_1_Pct.append(ground_1_Pct)

data1 = {'Fighter_ID': Fighter_ID, 'Fight_ID': Fight_ID, 'Fight_Name': Fight_Name, 'Round': Round,
         'Knockdowns_0': Knockdowns_0,
         'Knockdowns_1': Knockdowns_1, 'Significant_Strikes_0': Significant_Strikes_0,
         'Significant_Strikes_1': Significant_Strikes_1,
         'Significant_Strike_pct_0': Significant_Strike_pct_0, 'Significant_Strike_pct_1': Significant_Strike_pct_1,
         'Total_Strikes_0': Total_Strikes_0, 'Total_Strikes_1': Total_Strikes_1, 'Head_0': Head_0, 'Head_1': Head_1,
         'Body_0': Body_0,
         'Body_1': Body_1, 'Legs_0': Legs_0, 'Legs_1': Legs_1, 'Distance_0': Distance_0, 'Distance_1': Distance_1,
         'Clinch_0': Clinch_0, 'Clinch_1': Clinch_1, 'Ground_0': Ground_0, 'Ground_1': Ground_1,
         'Takedowns_0': Takedowns_0,
         'Takedowns_1': Takedowns_1, 'Takedown_pct_0': Takedown_pct_0, 'Takedown_pct_1': Takedown_pct_1,
         'Submission_Attempt_0': Submission_Attempt_0, 'Submission_Attempt_1': Submission_Attempt_1,
         'Rev_0': Rev_0, 'Rev_1': Rev_1, 'Control_Time_0': Control_Time_0, 'Control_Time_1': Control_Time_1, }
df1 = pd.DataFrame(data=data1)
df1.index += 1
df1.to_excel("~/Desktop/output_1.xlsx")

data2 = {'Fighters_ID': Fighters_ID, 'Fights_ID': Fights_ID, 'Fights_Name': Fights_Name, 'Weight_Class': Weight_Class,
         'Opponent': Opponent, 'Method': Method, 'Round_End': Round_End, 'Time_End': Time_End,
         'Fight_format': Fight_format,
         'Referee': Referee, 'Details': Details, }
df2 = pd.DataFrame(data=data2)
df2.index += 1
df2.to_excel("~/Desktop/output_2.xlsx")

data3 = {'Fighterss_ID': Fighterss_ID, 'Fightss_ID': Fightss_ID, 'Fighter_0': Fighter_0, 'Fighter_1': Fighter_1,
         'Head_0_Pct': Head_0_Pct,
         'Head_1_Pct': Head_1_Pct, 'Body_0_Pct': Body_0_Pct, 'Body_1_Pct': Body_1_Pct, 'Leg_0_Pct': Leg_0_Pct,
         'Leg_1_Pct': Leg_1_Pct, 'Distance_0_Pct': Distance_0_Pct, 'Distance_1_Pct': Distance_1_Pct,
         'Clinch_0_Pct': Clinch_0_Pct, 'Clinch_1_Pct': Clinch_1_Pct, 'Ground_0_Pct': Ground_0_Pct,
         'Ground_1_Pct': Ground_1_Pct, }
df3 = pd.DataFrame(data=data3)
df3.index += 1
df3.to_excel("~/Desktop/output_3.xlsx")
