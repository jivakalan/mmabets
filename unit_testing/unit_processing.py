#####################################################################
##                          Imports                              ###
from process.tools.helper import *
###################################################################


def test_create_main_fight_fact_cumulative():

    src_folder = r'C:\Users\kalan\PycharmProjects\MMABets\extract\data\database'
    main_fight_fact = pd.read_csv(src_folder + "\\" + "main_fight_fact.csv")
    fight_outcome_fact = pd.read_csv(src_folder + "\\" + "fight_outcome_fact.csv")

    #fighters = ['22a92d7f62195791']f4c49976c75c5ab2
    main_fight_fact = main_fight_fact[main_fight_fact.Fighter_ID.isin(['22a92d7f62195791' ,'f4c49976c75c5ab2'])]
    main_fight_fact_w_dates = pd.merge(main_fight_fact, fight_outcome_fact[['Fight_ID', 'Fighter_ID', 'Fight_Date']],
                                       on=['Fight_ID', 'Fighter_ID'])
    main_fight_fact_w_dates['Fight_Date'] = pd.to_datetime(main_fight_fact_w_dates['Fight_Date'])
    outdf = create_main_fight_fact_cumulative(main_fight_fact_w_dates)

    result = outdf[outdf.Fighter_ID =='22a92d7f62195791'].Significant_Strikes_0_cumulative.tolist()[-1]
    expected_result = main_fight_fact[main_fight_fact.Fighter_ID =='22a92d7f62195791'].Significant_Strikes_0.sum()

    assert result == expected_result