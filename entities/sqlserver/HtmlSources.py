from datetime import date, timedelta

from FrameHelper import FrameHelper
import HtmlSourceWalker as htmlsource_walker

from entities.sqlserver import Fund as sqlserver_fund
from entities.sqlserver import FundValue as sqlserver_fundvalue
from entities.sqlserver import HtmlSource as html_source

from globals import DateTime


def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fundvalue_handler, begin_date, end_date)
    
def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
    htmlsource_walker.walk(html_source, insert_fund_handler, begin_date, end_date)
        
def insert_fundvalue_handler(frame_dict: dict):
    
    new_fund_dfs = sqlserver_fundvalue.insert_frame(frame_dict)
    if len(new_fund_dfs) > 0:
        sqlserver_fundvalue.insert_frame(new_fund_dfs)

def insert_fund_handler(frame_dict):
    
    sqlserver_fund.insert_frame(frame_dict)
