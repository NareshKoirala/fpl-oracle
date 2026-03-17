import requests as req
from bs4 import BeautifulSoup as bs


class fotmob_scrapper:

    def __init__(self):
        self.base_url = "https://www.fotmob.com/leagues/47/table/premier-league"
        request_raw_data = req.get(self.base_url)
        self.soup = bs(request_raw_data.text, features="html.parser")
    
    def get_imp_links(self):
        get_nav = self.soup.nav

        for x in get_nav:
            print(x.get('href'))
    



fotmob = fotmob_scrapper()
fotmob.get_imp_links()



#section_clipped = soup.article
#print(section_clipped)

#for i in soup.find('div', class_='flipmove'):
#    print(i)

#def table_scrap(soup):
#    pass
