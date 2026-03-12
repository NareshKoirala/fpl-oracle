import requests
import json

def api_fetch()-> dict:
    # The 'bootstrap-static' endpoint from your MS link
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
    
        final_data = {}
        raw_data = response.json()
        
        final_data['teams'] = team_table(raw_data)
        final_data['players'] = player_data(raw_data)

        return final_data
    else:
        print(f"❌ Error: {response.status_code}")


def team_table(raw_data: dict)->dict:
    #remove slice before final push
    return raw_data['teams'][:1]


def player_data(raw_data: dict)-> dict:
    #Remove the slice before the final push
    return raw_data['elements'][:1]
