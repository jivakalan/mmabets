from process.tools.helper import *

def create_scoring_record(fighter_0, fighter_1):
    fighter_name_0 = fighter_0
    fighter_name_1 = fighter_1
    match = [fighter_name_0, fighter_name_1]

    fighter_dim = pd.read_csv('process/data/outputs/fighter_dim_updated.csv')
    fight_outcome_fact_cumulative = pd.read_csv('process/data/outputs/fight_outcome_fact_cumulative.csv')
    main_fight_fact_cumulative = pd.read_csv('process/data/outputs/main_fight_fact_cumulative.csv')


    cols = load_json('process/tools/ds_dataset_cols.json')
    cumulative_cols_0 = cols['cumulative_cols_0']
    cumulative_cols_1 = cols['cumulative_cols_1']
    cumulative_demo_cols = cols['cumulative_demo_cols']
    demo_cols = cols['demo_cols']
    odds_cols = cols['odds_cols'] #todo: from fight odds fact

    # look up the cum totals data upto the date
    try:
        fighter_0 = fighter_dim[fighter_dim.Fighter_name == fighter_0].Fighter_ID.iloc[0]
        fighter_1 = fighter_dim[fighter_dim.Fighter_name == fighter_1].Fighter_ID.iloc[0]

        cumdata_fighter_0 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_0)][cumulative_cols_0].iloc[-1].to_frame().T.reset_index(drop=True)
        cumdata_fighter_1 = main_fight_fact_cumulative[(main_fight_fact_cumulative.Fighter_ID == fighter_1)][cumulative_cols_1].iloc[-1].to_frame().T.reset_index(drop=True)


        # lookup the demographic data
        demos_fighter_0 = fighter_dim[fighter_dim.Fighter_ID == fighter_0][demo_cols].reset_index(drop=True)
        # Rename the columns by adding a suffix "_0"
        demos_fighter_0.columns = [col + '_0' for col in demo_cols]

        demos_fighter_1 = fighter_dim[fighter_dim.Fighter_ID == fighter_1][demo_cols].reset_index(drop=True)
        # Rename the columns by adding a suffix "_0"
        demos_fighter_1.columns = [col + '_1' for col in demo_cols]

        # lookup the cumulative demo data
        demos_cum_fighter_0 = fight_outcome_fact_cumulative[fight_outcome_fact_cumulative.Fighter_ID == fighter_0][cumulative_demo_cols].iloc[-1].to_frame().T.reset_index(drop=True)
        demos_cum_fighter_0.columns = [col + '_0' for col in cumulative_demo_cols]

        demos_cum_fighter_1 = fight_outcome_fact_cumulative[fight_outcome_fact_cumulative.Fighter_ID == fighter_1][cumulative_demo_cols].iloc[-1].to_frame().T.reset_index(drop=True)
        demos_cum_fighter_1.columns = [col + '_1' for col in cumulative_demo_cols]

        # lookup the cumulative PCT metrics
        record = [cumdata_fighter_0, cumdata_fighter_1, demos_fighter_0, demos_fighter_1,demos_cum_fighter_0,demos_cum_fighter_1 ]

    except:
        pass




    return record, match





