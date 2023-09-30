#######This file is work in progress - not sure what the objective is of this file - what is the requirement? What does it need to do...
import json
import re
import Levenshtein
from tqdm import tqdm
##############################################################################
##this file gets the links that will be run to update the odds data on ALL (later, ACTIVE) ufc fighters
##############################################################################

##get the list of best odd fighters -- bestoddfighters.json
with open('extract/data/outputs/bestoddfighters.json','r') as json_file:
    bestodd_fighters = json.load(json_file)

##get the list of all (or active) ufc fighters - ufc fighter IDs or ufcActiveFighters
with open('extract/data/outputs/ufc_fighterIDs.json','r') as json_file:
    all_ufc_fighters = json.load(json_file)

##get the list of all (or active) ufc fighters - ufc fighter IDs or ufcActiveFighters
with open('extract/data/outputs/ufc_ActiveFighters.json','r') as json_file:
    all_ufc_fighters = json.load(json_file)

##get the names for each
ufcFighterNames = []
for dict in all_ufc_fighters.values():
    ufcFighterNames.append(list(dict.values())[0])

best_fighterNames = []
for bestFightoddlink in bestodd_fighters:
    fighterName = bestFightoddlink[10:]
    fighterName = re.sub(r'-\d{3,5}', '', fighterName)
    # Split the string by hyphen
    parts = fighterName.split('-')
    # Remove the hyphen between the first name and last name
    fighterName = ' '.join(parts)
    best_fighterNames.append(fighterName)

##get the list of ufc fighters who are not represented in best odd fighters currently
def find_fuzzy_matches(name, name_list, threshold=80):
    matches = [n for n in name_list if Levenshtein.ratio(name.lower(), n.lower()) >= threshold / 100.0]
    return matches
threshold = 80  # Adjust the threshold as needed
ufcfighters_NOT_in_bo_Yet =[]

with tqdm(total=len(ufcFighterNames)) as pbar:
    for name in ufcFighterNames:
        if not find_fuzzy_matches(name, best_fighterNames, threshold):
            ufcfighters_NOT_in_bo_Yet.append(name)
        pbar.update(1)  # Update the progress bar

##the list of ufc fighters not represented...go get the list manually ...

