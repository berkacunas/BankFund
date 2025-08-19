from enum import Enum
from selenium import webdriver

class WebBrowsers(Enum):
    FIREFOX = 1
    CHROME = 2
    SAFARI = 3
    
def get_browser(web_browsers: WebBrowsers) -> webdriver:
    
    try:
        if web_browsers == WebBrowsers.FIREFOX:
            return webdriver.Firefox()
        elif web_browsers == WebBrowsers.CHROME:
            return webdriver.Chrome()
        elif web_browsers == WebBrowsers.SAFARI:
            return webdriver.Safari()
        
    except Exception as error:
        raise error

def get_page_source(url: str, browser: webdriver) -> str:
    
    try:
        browser.get(url)
        html = browser.page_source
        
        return html
    
    except Exception as error:
        raise error
