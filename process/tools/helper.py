

def create_fight_dictionary():
    outdf = pd.DataFrame()
    for fight in fight_outcome_fact:
        fight = fight_outcome_fact[fight]
        # split the fight in half
        a = fight.1stRow
        b = fight.2ndRow

        outdf = outdf.append(a + b)
    return outdf


fight_w_opponents = create_fight_dictionary(fight_outcome_fact)


def add_fighters_data(main_fight_fact_cumulative)
    fighter_x_data = pd.merge(fight_w_opponents, main_fight_fact_cumulative, left_on=['Fighter_X_ID', 'Fight_ID'],
                              right_on=['Fighter_ID', 'Fight_ID'])
    fighter_y_data = pd.merge(fight_w_opponents, main_fight_fact_cumulative, left_on=['Fighter_Y_ID', 'Fight_ID'],
                              right_on=['Fighter_ID', 'Fight_ID'])

    return pd.merge(fighter_x_data, fighter_y_data, on=['Fight_ID'])




def initalize_metrics():
    metrics ={}
    metrics['Knockdowns_0']                 = 0
    metrics['Significant_Strikes_0']        = 0
    metrics['Significant_Strike_pct_0']     = 0
    metrics['Total_Strikes_0']              = 0
    metrics['Head_0']                       = 0
    metrics['Body_0']                       = 0
    metrics['Legs_0']                       = 0
    metrics['Distance_0']                   = 0
    metrics['Clinch_0']                     = 0
    metrics['Ground_0']                     = 0
    metrics['Takedowns_0']                  = 0
    metrics['Takedown_pct_0']               = 0
    metrics['Submission_Attempt_0']         = 0
    metrics['Rev_0']                        = 0
    metrics['Control_Time_0']               = 0
    ##add fight strike location


def get_cumulative(df, fighter):
    cumulative = pd.DataFrame()
    metrics = initalize_metrics()
    for round in df:
        for metric in metrics:
            metrics[metric] += df[round.metric]
            cumulative.append(metrics)
    return cumulative


def create_main_fight_fact_cumulative(df, fighters):
    main_fight_fact_in = pd.merge(main_fight_fact, fight_outcome_fact, on=['Fighter_ID', 'Fight_Name'])
    main_fight_fact_in = main_fight_fact_in.rename(columns={'Fight_ID_x': 'Fight_ID'})

    df = pd.merge(main_fight_fact_in, fight_strike_location_fact, on=['Fight_ID', 'Fighter_ID'])

    df = df[df.Fighter_ID == '22a92d7f62195791']
    df = df.rename(columns={'Fight_Date_x': 'Fight_Date'})
    df['Fight_Date'] = pd.to_datetime(df['Fight_Date'])
    df = df.sort_values(by=['Fighter_ID', 'Fight_Date'])

    outdf = pd.DataFrame()
    for fighter in fighters:
        cumulative = get_cumulative(df, fighter)
    outdf.append(cumulative)


    # unit test
    print(len(outdf) == len(main_fight_fact))

    return outdf