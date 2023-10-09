#####################################################################
##                          Imports                              ###
####################################################################
import unidecode as decode
####################################################################



def test_create_scoring_record():
    fighter_0 ='Marc-André Barriault'
    fighter_1 ='Michel Pereira'
    fighter_0 = decode.unidecode(fighter_0)
    fighter_1 = decode.unidecode(fighter_1)

    # lookup fighter metrics and construct the match up
    record = create_scoring_record(fighter_0, fighter_1)

    record = records[0]

    df = pd.DataFrame()
    for component in record:
        print(component)
        df = pd.concat([df,component], axis=1)


    assert