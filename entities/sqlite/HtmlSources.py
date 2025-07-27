from datetime import date

import HtmlSourceWalker as htmlsource_walker

from entities.sqlite import Fund as sqlite_fund
from entities.sqlite import FundValue as sqlite_fundvalue
from entities.sqlite import HtmlSource as html_source

def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fundvalue_handler, begin_date, end_date)
    
def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fund_handler, begin_date, end_date)
        
def insert_fundvalue_handler(frame_dict: dict):
    
    sqlite_fundvalue.insert(frame_dict)

def insert_fund_handler(frame_dict):
    
    sqlite_fund.insertall(frame_dict)
