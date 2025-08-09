from datetime import date

from FrameHelper import FrameHelper
import HtmlSourceWalker as htmlsource_walker

from entities.sqlserver import Fund as sqlserver_fund
from entities.sqlserver import FundValue as sqlserver_fundvalue
from entities.sqlite import Fund as sqlite_fund
from entities.sqlite import FundValue as sqlite_fundvalue

from entities.textserver import TextSource as text_source

from globals import DateTime

from enum import Enum

class Destination(Enum):
    SQLSERVER = 1
    SQLITE = 2
   
frame_helper = FrameHelper()
destination = Destination.SQLSERVER     # SQL Server is default value.

# def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
#     dates = text_source.list_dates()
#     date_values = [x[0] for x in dates.values()]
    
#     textfile_count = text_source.count(begin_date, end_date)
    
#     if begin_date == date.min:
#         begin_date = min(date_values)
#     if end_date == date.today():
#         end_date = max(date_values)
        
#     delta = timedelta(days=1)
    
#     iter_date = begin_date
#     while (iter_date <= end_date):
#         if textfile_count == 0:
#             break
        
#         print("*" * 100)
#         print(f"Date: {iter_date} processing...")
#         print("*" * 100)
#         daily_textfile_count = text_source.count(iter_date, iter_date)
#         # if date in dates:
#         #     textfile_count -= daily_textfile_count
#         #     continue
        
#         if DateTime.is_weekend(iter_date):
#             if daily_textfile_count != -1:
#                 textfile_count -= daily_textfile_count
#             iter_date += delta
#             continue
        
#         text_files = text_source.read(iter_date)
#         if not text_files:
#             continue
        
#         try:
#             htmls = [x.Html for x in text_files]
#             dts = [x.Dt for x in text_files]
            
#             frame_helper.create_frame_dicts(htmls, dts, insert_fundvalue_handler)
#             iter_date += delta
#             textfile_count -= 1
        
#         except Exception as error:
#             print(error)
#             raise error

# def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
#     dates = text_source.list_dates()
#     date_values = [x[0] for x in dates.values()]
    
#     textfile_count = text_source.count(begin_date, end_date)
    
#     if begin_date == date.min:
#         begin_date = min(date_values)
#     if end_date == date.today():
#         end_date = max(date_values)
    
#     delta = timedelta(days=1)
    
#     iter_date = begin_date
#     while (iter_date <= end_date):
#         if textfile_count == 0:
#             break
        
#         print("*" * 100)
#         print(f"Date: {iter_date} processing...")
#         print("*" * 100)
#         daily_textfile_count = text_source.count(iter_date, iter_date)
#         # if date in dates:
#         #     textfile_count -= daily_textfile_count
#         #     continue
        
#         if DateTime.is_weekend(iter_date):
#             if daily_textfile_count != -1:
#                 textfile_count -= daily_textfile_count
#             iter_date += delta
#             continue
        
#         text_files = text_source.read(iter_date)
#         if not text_files:
#             continue
        
#         try:
#             htmls = [x.Html for x in text_files]
#             dts = [x.Dt for x in text_files]
            
#             frame_helper.create_frame_dicts(htmls, dts, insert_fund_handler)
#             iter_date += delta
#             textfile_count -= 1
        
#         except Exception as error:
#             print(error)
 
def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
    htmlsource_walker.walk(text_source, insert_fundvalue_handler, begin_date, end_date)
    
def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
    htmlsource_walker.walk(text_source, insert_fund_handler, begin_date, end_date)
        
def insert_fundvalue_handler(frame_dict: dict):
    
    if destination == Destination.SQLSERVER:
        sqlserver_fundvalue.insert(frame_dict)
    elif destination == Destination.SQLITE:
        sqlite_fundvalue.insert(frame_dict)

def insert_fund_handler(frame_dict):
    
    if destination == Destination.SQLSERVER:
        sqlserver_fund.insert_frame(frame_dict)
    elif destination == Destination.SQLITE:
        sqlite_fund.insert_frame(frame_dict)
