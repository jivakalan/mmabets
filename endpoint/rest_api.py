import requests
import json

#todo update not add table
def prep_data():
    # Create the header row
    header = ['Matchup', 'Fighter Prediction', 'Loss', 'Win', 'No Contest', 'Draw']

    # Initialize the data dictionary with the header row
    data = {'rows': [header]}

    # Iterate through matchups and predictions and add them to the data dictionary
    for i, matchup in enumerate(matchups):
        first_fighter = [matchup[0]]  # Get the name of the first fighter in the matchup
        matchup_str = f'{matchup[0]} VS {" VS ".join(matchup[1:])}'  # Add " VS " between fighter names
        matchup_data = [matchup_str]

        # Round and format the predictions as percentages
        formatted_predictions = [f'{pred * 100:.1f}%' for pred in predictions[i]]
        matchup_data.extend(first_fighter)
        matchup_data.extend(formatted_predictions)
        data['rows'].append(matchup_data)

    # Print the data dictionary
    print(data)

    return data

def push_to_wordpress(data):

    # URL for creating a new post via WordPress REST API
    url = 'https://www.ufc-bets.com/wp-json/custom/v1/post-predictions'

    # Authentication
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VmYy1iZXRzLmNvbSIsImlhdCI6MTY5NjczNjA1MSwibmJmIjoxNjk2NzM2MDUxLCJleHAiOjE2OTczNDA4NTEsImRhdGEiOnsidXNlciI6eyJpZCI6IjEifX19.nPSSD8iZlS1YTiZPYBJHsUB3BUoWsAWZKPK8MvC1oPk'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Post created successfully!")
    else:
        print("Failed to create post. Status code:", response.status_code)

    return


# load predictions and matchups
with open('endpoint/data/predictions.json','r') as file:
    predictions = json.load(file)
with open('endpoint/data/matchups.json','r') as file:
    matchups = json.load(file)

# Send Data to WordPress
data = prep_data()
push_to_wordpress(data)



