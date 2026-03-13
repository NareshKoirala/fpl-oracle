import requests as req
from bs4 import BeautifulSoup as bs
from pprint import pprint

base_url = "https://www.fotmob.com/leagues/47/table/premier-league"
request_raw_data = req.get(base_url)

soup = bs(request_raw_data.text, features="html.parser")

#section_clipped = soup.article
#print(section_clipped)

for i in soup.find('div', class_='flipmove'):
    print(i)

def table_scrap(soup):
    pass
