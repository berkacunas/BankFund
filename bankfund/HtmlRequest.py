from io import StringIO
import pandas as pd
import requests
import sqlite3
from datetime import datetime

from entities.sqlserver import HtmlSources as sqlserver_htmlsources

from entities.sqlserver import HtmlSource as sqlserver_htmlsource
from entities.sqlserver import FundValue as sqlserver_fundvalue

from entities.sqlite import HtmlSource as sqlite_htmlsource

from entities.textserver import TextSource as text_source

from globals.globals import SQLITE_DB_PATH, URL, DATETIME_NOW_FILE_FORMAT, rename_columns_dict
from globals.DateTime import to_julian

from FrameHelper import get_empty_row_indexes, realign_frame, split_Code_Dt_Title_column

import HtmlParser

def get_response(url) -> requests.Response:
    
    response = requests.get(url)

    if response:
        print("Success!")
    else:
        raise Exception(f"Non-success status code: {response.status_code}")

    return response
    

def create_framedict_from_html(html_source):
    
    frame_dict = None
    
    try:
        m_frame = pd.read_html(html_source.Html)[0]
        HtmlParser.rename_frame(m_frame, rename_columns_dict, True)
        HtmlParser.mask_frame(m_frame, m_frame == '', inplace=True)
        m_frame.dropna(axis=1, how='any', inplace=True)
        m_frame = split_Code_Dt_Title_column(m_frame, html_source.Dt)
        m_frame = realign_frame(m_frame)
                
        indexes = get_empty_row_indexes(m_frame)
        fund_types_frame = HtmlParser.get_fund_types_frame(m_frame)
        frame_dict = HtmlParser.create_framedict(m_frame, fund_types_frame["Code"], indexes)
                
    except Exception as error:
        print(error)
    
    return frame_dict


def insert_fundvalues_from_html_source(html_source):
    
    frame_dict = create_framedict_from_html(html_source.Dt, html_source.Html)
    
    try:
        sqlserver_fundvalue.insert(frame_dict)
    except Exception as error:
        print(error)
        

def main():

    html = None
    try:
        response = get_response(URL)
        # html = TextFile.read(r"./html/03-07-2025_21-26-15.txt")
    except Exception as error:
        print(error)
    
    try:
        filename = fr"C:\berk\GitHub\berk\BankFund\html\{datetime.now().strftime(DATETIME_NOW_FILE_FORMAT)}.txt"
        text_source.insert(filename, response.text)
    except Exception as error:
        print(error)
        
    try:
        sqlite_htmlsource.insert(response.text)
    except Exception as error:
        print(error)
    
    try: 
        sqlserver_htmlsource.insert(response.text)
        sqlserver_htmlsources.insert_fundvalues(datetime.now().date())
        
    except Exception as error:
        print(error)

        
if __name__ == '__main__':
    main()