import pprint
from datetime import datetime, date, timedelta
from io import StringIO 
import pandas as pd

import HtmlParser

from FrameHelper import get_empty_row_indexes, split_Code_Dt_Title_column, realign_frame

from globals import DateTime
from globals.globals import rename_columns_dict, DATETIME_NOW_FILE_FORMAT

from entities.sqlite import HtmlSources as sqlite_htmlsources
from entities.sqlite import HtmlSources as sqlite_htmlsource
from entities.sqlite import Bank as sqlite_bank
from entities.sqlite import Fund as sqlite_fund
from entities.sqlite import FundType as sqlite_fundtype
from entities.sqlite import FundValue as sqlite_fundvalue

from entities.sqlserver import HtmlSources as sqlserver_htmlsources
from entities.sqlserver import HtmlSources as sqlserver_htmlsource
from entities.sqlserver import FundValue as sqlserver_fundvalue

from entities.textserver import TextSource as text_source
from entities.textserver import TextSources as text_sources

from plots import ScatterPlots

def insert_html_sources(begin_date : date = date.min, end_date : date = date.today()):
    
    dates = sqlserver_fundvalue.select_dates()
    htmlsource_count = sqlserver_htmlsource.count(begin_date, end_date)
    
    delta = timedelta(days=1)
    
    while (begin_date <= end_date):
        if htmlsource_count == 0:
            break
        
        date = end_date
        end_date -= delta
         
        print(date)
        
        daiy_htmlsource_count = sqlserver_htmlsource.count(begin_date=date, end_date=date)
        if date in dates:
            htmlsource_count -= daiy_htmlsource_count
            continue
        
        if DateTime.is_weekend(date):
            if daiy_htmlsource_count != -1:
                htmlsource_count -= daiy_htmlsource_count
            continue
        
        html_sources = sqlite_htmlsource.select(date)
        if not html_sources:
            continue
        
        for html_source in html_sources:
            m_frame = pd.read_html(StringIO(html_source.Html))[0]
            HtmlParser.rename_frame(m_frame, rename_columns_dict, True)
            HtmlParser.mask_frame(m_frame, m_frame == '', inplace=True)
            m_frame.dropna(axis=1, how='any', inplace=True)
            m_frame = split_Code_Dt_Title_column(m_frame, html_source.Dt)
            m_frame = realign_frame(m_frame)
                 
            indexes = get_empty_row_indexes(m_frame)
            fund_types_frame = HtmlParser.get_fund_types_frame(m_frame)
            frame_dict = HtmlParser.create_framedict(m_frame, fund_types_frame["Code"], indexes)
            
            try:
                # SqlServerDatabase.insert_fundtypes(fund_types_frame)
                # SqlServerDatabase.insert_funds(frame_dict)
                    
                sqlserver_fundvalue.insert_frame(frame_dict)
                
            except Exception as error:
                print(error)
            
            htmlsource_count -= 1

def insert_fundvalues_from_htmlsource(html):
    
    frame_dict = create_framedict_from_html(datetime.datetime.now, html)
    
    try:
        sqlserver_fundvalue.insert(frame_dict)
    except Exception as error:
        print(error)

def create_framedict_from_html(dt, html):
    
    m_frame = pd.read_html(StringIO(html))[0]
    HtmlParser.rename_frame(m_frame, rename_columns_dict, True)
    HtmlParser.mask_frame(m_frame, m_frame == '', inplace=True)
    m_frame.dropna(axis=1, how='any', inplace=True)
    m_frame = split_Code_Dt_Title_column(m_frame, dt)
    m_frame = realign_frame(m_frame)
            
    indexes = get_empty_row_indexes(m_frame)
    fund_types_frame = HtmlParser.get_fund_types_frame(m_frame)
    frame_dict = HtmlParser.create_framedict(m_frame, fund_types_frame["Code"], indexes)
    
    return frame_dict



def main():
    
    # check_date = date(2025, 8, 5)
    # if sqlserver_fundvalue.is_date_values_inserted(check_date):
    #     print(f'Fund values inserted for date: {check_date}')
    # else:
    #     print(f'Cannot find Fund values for date: {check_date}')
        
    # sqlite_bank.initialize()
    
    try:
        # sources = text_source.select(date(2025, 6, 26))
        # for source in sources:
        #     frame_dict = create_framedict_from_html(source.Dt, source.Html)
        #     sqlite_fund.insert_frame(frame_dict)
        #     break
        
        # sqlite_htmlsources.insert_fundvalues(date(2025, 7, 29))
        # sqlite_duplicates = sqlite_fundvalue.get_duplicate_entries()
        # pprint.pp(sqlite_duplicates, depth=1)
        # sqlite_deleted_duplicate_count = sqlite_fundvalue.delete_duplicate_entries(sqlite_duplicates)
        # sqlite_deleted_weekend_count = sqlite_fundvalue.delete_weekend_entries()
        
        # sqlserver_htmlsources.insert_fundvalues(date(2025, 8, 1))
        sqlserver_duplicates = sqlserver_fundvalue.get_duplicate_entries()
        pprint.pp(sqlserver_duplicates, depth=1)
        sqlserver_deleted_duplicate_count = sqlserver_fundvalue.delete_duplicate_entries(sqlserver_duplicates)
        sqlserver_deleted_weekend_count = sqlserver_fundvalue.delete_weekend_entries()
        
        # sqlserver_fundvalue.to_csv(f"./csv/FundValue_{datetime.strftime(datetime.now(), DATETIME_NOW_FILE_FORMAT)}.csv")
        # filename = "./csv/FundValue_2025-07-04_21-37-25.csv"

        # fundvalues = sqlserver_fundvalue.select_all()
        # frame = pd.DataFrame(fundvalues)
        # ScatterPlots.plot(frame, date(2025, 6, 10), date(2025, 7, 8))
        # ScatterPlots.scatter(frame)
        
        # html_file_sources = text_source.read(datetime.date.today())
        # text_sources.insert_new_funds()
        # text_sources.insert_fundvalues()
        
    except ValueError as verror:
        print(f"Value error occured in main()::text_source.read()\n{verror}")
    except Exception as error:
        print(f"Exception occured: {error}")
    

if __name__ == "__main__":
    main()