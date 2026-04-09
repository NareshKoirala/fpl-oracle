from utils.log import Logger
import requests as req
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright

LOG = Logger("Scapper")
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
BROWSER = sync_playwright().chromium.launch(headless=False)
context = BROWSER.new_context(user_agent=AGENT)
PAGE = context.new_page()

class Playwright:
    pass
    

class Scapper:
    def __init__(self, url):
        self.url = url
        
    
        