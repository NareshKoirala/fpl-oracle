import requests as req
from bs4 import BeautifulSoup as bs
from pprint import pprint

base_url = "https://www.fotmob.com/leagues/47/overview/premier-league"
request_raw_data = req.get(base_url)

soup = bs(request_raw_data.text, features="html.parser")
nav = soup.nav

for a in nav.find_all('a'):
    print(a['href'])
