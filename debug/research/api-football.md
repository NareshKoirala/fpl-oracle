https://dashboard.api-football.com/profile?access

So current season is not given here but a good source but wouldnt be using as its expensive

import requests
url = "https://v3.football.api-sports.io/leagues?name=premier%20league&season=2025"

headers = {
  'x-apisports-key': 'xxx',
}

response = requests.request("GET", url, headers=headers)

print(response.text)

{
    "get":"leagues",
    "parameters":{
        "name":"premier league",
        "season":"2025"
    },
    "errors":{
        "plan":"Free plans do not have access to this season, try from 2022 to 2024."
    },
    "results":0,
    "paging":{
        "current":1,
        "total":1
    },
    "response":[]
}