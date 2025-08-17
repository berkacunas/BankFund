from datetime import date

import bankfund.HtmlSourceWalker as htmlsource_walker

from bankfund.entities.sqlite import Fund as sqlite_fund
from bankfund.entities.sqlite import FundValue as sqlite_fundvalue
from bankfund.entities.sqlite import HtmlSource as html_source

def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fundvalue_handler, begin_date, end_date)
    
def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fund_handler, begin_date, end_date)
        
def insert_fundvalue_handler(frame_dict: dict):
    
    new_fund_dfs = sqlite_fundvalue.insert_frame(frame_dict)
    if len(new_fund_dfs) > 0:
        sqlite_fundvalue.insert_frame(new_fund_dfs)
    
def insert_fund_handler(frame_dict):
    
    sqlite_fund.insert_frame(frame_dict)
