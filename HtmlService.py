from datetime import datetime

from web.HeadlessBrowser import get_browser, get_page_source, WebBrowsers

from bankfund.entities.sqlserver import HtmlSources as sqlserver_htmlsources
from bankfund.entities.sqlserver import HtmlSource as sqlserver_htmlsource
from bankfund.entities.sqlserver import FundValue as sqlserver_fundvalue

from bankfund.entities.sqlite import HtmlSource as sqlite_htmlsource

from bankfund.entities.textserver import TextSource as text_source

from bankfund.utilities.naming import URL, DATETIME_NOW_FILE_FORMAT
        

def main():

    html = None
    try:
        browser = get_browser(WebBrowsers.FIREFOX)
        html = get_page_source(URL, browser)
    except Exception as error:
        print(error)
    
    try:
        filename = fr"C:\berk\GitHub\berk\BankFund\html\{datetime.now().strftime(DATETIME_NOW_FILE_FORMAT)}.txt"
        text_source.insert(filename, html)
    except Exception as error:
        print(error)
        
    try:
        sqlite_htmlsource.insert(html)
    except Exception as error:
        print(error)
    
    try: 
        sqlserver_htmlsource.insert(html)
        sqlserver_htmlsources.insert_fundvalues(datetime.now().date())
        
    except Exception as error:
        print(error)

        
if __name__ == '__main__':
    main()