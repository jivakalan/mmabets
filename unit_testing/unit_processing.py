from processing.helper import import *

def unit_testing_processing(df, fight_outcome_fact):
    tests={}
    tests['test1'] = df[df.Fighter_ID == '22a92d7f62195791']
    tests['test2'] = df[df.Fighter_ID == '07225ba28ae309b6']
    tests['test3'] = df[df.Fight_ID == 'b7b867eb3c3cf163']
    tests['test4'] = fight_outcome_fact[fight_outcome_fact.Fighter_ID == '07225ba28ae309b6']
    tests['test5'] = fight_outcome_fact[fight_outcome_fact.Fighter_ID == '22a92d7f62195791']

    return tests