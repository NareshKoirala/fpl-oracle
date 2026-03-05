import requests
import json
from pprint import pprint

def api_fetch()-> dict:
    # The 'bootstrap-static' endpoint from your MS link
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        return data
    else:
        print(f"❌ Error: {response.status_code}")


def position_table(raw_data: dict)->dict:

    position_dict = {
    team['position']: {
        team['id']: team['name'],
        'strength': {
            'home_atk': team['strength_attack_home'],
            'away_atk': team['strength_attack_away'],
            'home_def': team['strength_defence_home'],
            'away_def': team['strength_defence_away'],
            'overall_home': team['strength_overall_home'],
            'overall_away': team['strength_overall_away']
         }
    } for team in raw_data['teams']}

    return dict(sorted(position_dict.items()))


def player_fetch(raw_data: dict)-> dict:
    return raw_data['elements']

    
if __name__ == "__main__":
    raw_data = api_fetch()
    #pprint(position_table(raw_data))
    players = [s for s in player_fetch(raw_data) if s['web_name'] == 'Palmer'] 
    pprint(players)
