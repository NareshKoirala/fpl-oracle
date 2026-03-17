import time
import random
import requests as req
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright

class fotmob_scrapper:

    def __init__(self):
        self.base_url = "https://www.fotmob.com/leagues/47/table/premier-league"
        self.soup = self.playwright_content(self.base_url)

    def playwright_content(self, url):
        with sync_playwright() as p:
                # Launch headless (no window pops up)
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            )
            page = context.new_page()
    
            try:
                page.goto(url)
                
                # This is the magic part: wait for the JS to 'paint' the table
                # Replace '.stats-table' with the actual class name you saw in DevTools
                page.wait_for_selector(".flipmove", timeout=10000) 
                
                # Now grab the 'cooked' HTML
                content = page.content()
                
                return bs(content, 'html.parser')
    
            except Exception as e:
                print(f"Error: {e}")
            finally:
                browser.close()

    
    def get_imp_links(self):
        get_ = self.soup.article

        print(get_)

fotmob = fotmob_scrapper()
fotmob.get_imp_links()
