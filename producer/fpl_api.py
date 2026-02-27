import requests
import json

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
    position_dict = {}
    
    for team in raw_data['teams']:
        position_dict[team['position']] ={'name': team['name']}
        
    return {k : position_dict[k] for k in sorted(position_dict)}

if __name__ == "__main__":
    raw_data = api_fetch()
    #print(position_table(raw_data))

    print(raw_data['elements'])
