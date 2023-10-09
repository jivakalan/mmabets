#####################################################################
##                          Imports                              ###
import pandas as pd

from process.tools.helper import *
###################################################################


def test_create_main_fight_fact_cumulative():

    src_folder = r'C:\Users\kalan\PycharmProjects\MMABets\extract\data\database'
    main_fight_fact = pd.read_csv(src_folder + "\\" + "main_fight_fact.csv")
    fight_outcome_fact = pd.read_csv(src_folder + "\\" + "fight_outcome_fact.csv")

    #fighters = ['22a92d7f62195791']f4c49976c75c5ab2
    main_fight_fact = main_fight_fact[main_fight_fact.Fighter_ID.isin(['22a92d7f62195791','f4c49976c75c5ab2'])]
    main_fight_fact_w_dates = pd.merge(main_fight_fact, fight_outcome_fact[['Fight_ID', 'Fighter_ID', 'Fight_Date']],
                                       on=['Fight_ID', 'Fighter_ID'])
    main_fight_fact_w_dates['Fight_Date'] = pd.to_datetime(main_fight_fact_w_dates['Fight_Date'])
    outdf = create_main_fight_fact_cumulative(main_fight_fact_w_dates)

    result = outdf[outdf.Fighter_ID =='22a92d7f62195791'].Significant_Strikes_0_cumulative.tolist()[-1]
    expected_result = main_fight_fact[main_fight_fact.Fighter_ID =='22a92d7f62195791'].Significant_Strikes_0.sum()

    assert result == expected_result

def test_create_ds_dataset():

    # generate test case

    src_folder = r'C:\Users\kalan\PycharmProjects\MMABets\process\data\outputs'

    fight_outcome_fact_cumulative = pd.read_csv(src_folder + "\\" + "fight_outcome_fact_cumulative.csv")
    fighter_dim = pd.read_csv(src_folder + "\\" + "fighter_dim_updated.csv")
    main_fight_fact_cumulative = pd.read_csv("process/data/outputs/main_fight_fact_cumulative.csv")
    main_fight_fact_cumulative['Fight_Date'] = pd.to_datetime(main_fight_fact_cumulative['Fight_Date'])

    fight_base = ['7f16e7725245bb2d']  # Adesanya v Strickland
    #fight = fight_base[0]
    records = create_ds_test_set(fight_base, main_fight_fact_cumulative, fighter_dim,fight_outcome_fact_cumulative)
    record = records[0]

    df = pd.DataFrame()
    for component in record:
        print(component)
        df = pd.concat([df,component], axis=1)

    result = df.copy()
    expected_result = pd.read_csv('process/data/testing/test_case_test_create_ds_dataset.csv')

    #ensure the dtypes are equal
    result = result.apply(pd.to_numeric, errors='ignore', downcast='integer')
    expected_result = expected_result.apply(pd.to_numeric, errors='ignore', downcast='integer')

    result.columns.tolist() == expected_result.columns.tolist()

    assert result.equals(expected_result)

def test_create_fighter_outcome_cumulative():
    fighter_0='1338e2c7480bdf9e'

    fight_outcome_fact = pd.read_csv(src_folder + "\\" + "fight_outcome_fact.csv")

    fight_outcome_fact_cumulative = create_fighter_outcome_cumulative(fight_outcome_fact)
    df = fight_outcome_fact_cumulative[fight_outcome_fact_cumulative.Fighter_ID == fighter_0]

    result = df.Result_win_cumulative.iloc[-1]
    expected_result = 13 # current wins Israel Adesanya

    assert expected_result == result




