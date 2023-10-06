import pandas as pd

# def create_fight_dictionary():
#     outdf = pd.DataFrame()
#     for fight in fight_outcome_fact:
#         fight = fight_outcome_fact[fight]
#         # split the fight in half
#         a = fight.1stRow
#         b = fight.2ndRow
#
#         outdf = outdf.append(a + b)
#     return outdf


# fight_w_opponents = create_fight_dictionary(fight_outcome_fact)

#
# def add_fighters_data(main_fight_fact_cumulative)
#     fighter_x_data = pd.merge(fight_w_opponents, main_fight_fact_cumulative, left_on=['Fighter_X_ID', 'Fight_ID'],
#                               right_on=['Fighter_ID', 'Fight_ID'])
#     fighter_y_data = pd.merge(fight_w_opponents, main_fight_fact_cumulative, left_on=['Fighter_Y_ID', 'Fight_ID'],
#                               right_on=['Fighter_ID', 'Fight_ID'])
#
#     return pd.merge(fighter_x_data, fighter_y_data, on=['Fight_ID'])




def create_main_fight_fact_cumulative(main_fight_fact_w_dates):
    main_fight_fact_w_dates['Fight_Date'] = pd.to_datetime(main_fight_fact_w_dates['Fight_Date'])
    main_fight_fact_w_dates = main_fight_fact_w_dates.sort_values(by=['Fighter_ID', 'Fight_Date'])

    cols =['Knockdowns_0',
       'Knockdowns_1', 'Significant_Strikes_0', 'Significant_Strikes_1',
       'Significant_Strike_pct_0', 'Significant_Strike_pct_1',
       'Total_Strikes_0', 'Total_Strikes_1', 'Head_0', 'Head_1', 'Body_0',
       'Body_1', 'Legs_0', 'Legs_1', 'Distance_0', 'Distance_1', 'Clinch_0',
       'Clinch_1', 'Ground_0', 'Ground_1', 'Takedowns_0', 'Takedowns_1',
       'Takedown_pct_0', 'Takedown_pct_1', 'Submission_Attempt_0',
       'Submission_Attempt_1', 'Rev_0', 'Rev_1', 'Control_Time_0',
       'Control_Time_1']

    for col in cols:
        try:
            main_fight_fact_w_dates[col+'_cumulative']= main_fight_fact_w_dates.groupby(['Fighter_ID'])[col].cumsum()
        except:
            pass


    return main_fight_fact_w_dates