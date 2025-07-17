from datetime import date, timedelta
import pandas as pd
from io import StringIO

import HtmlParser
from FrameHelper import get_empty_row_indexes, split_Code_Dt_Title_column, realign_frame, FrameHelper

from entities.sqlserver import Fund as sqlserver_fund
from entities.sqlserver import FundValue as sqlserver_fundvalue
from globals.globals import rename_columns_dict
from globals import DateTime

from textserver import TextSource as text_source


frame_helper = FrameHelper()


def insert_fundvalues(begin_date : date = date.min, end_date : date = date.today()):
    
    dates = text_source.list_dates()
    date_values = [x[0] for x in dates.values()]
    
    textfile_count = text_source.count(begin_date, end_date)
    
    if begin_date == date.min:
        begin_date = min(date_values)
    if end_date == date.today():
        end_date = max(date_values)
        
    delta = timedelta(days=1)
    
    iter_date = begin_date
    while (iter_date <= end_date):
        if textfile_count == 0:
            break
        
        print("*" * 100)
        print(f"Date: {iter_date} processing...")
        print("*" * 100)
        daily_textfile_count = text_source.count(iter_date, iter_date)
        # if date in dates:
        #     textfile_count -= daily_textfile_count
        #     continue
        
        if DateTime.is_weekend(iter_date):
            if daily_textfile_count != -1:
                textfile_count -= daily_textfile_count
            iter_date += delta
            continue
        
        text_files = text_source.read(iter_date)
        if not text_files:
            continue
        
        try:
            htmls = [x.Html for x in text_files]
            dts = [x.Dt for x in text_files]
            
            frame_helper.create_frame_dicts(htmls, dts, insert_fundvalue_handler)
            iter_date += delta
            textfile_count -= 1
        
        except Exception as error:
            print(error)

def insert_new_funds(begin_date: date = date.min, end_date: date = date.today()):
    
    dates = text_source.list_dates()
    date_values = [x[0] for x in dates.values()]
    
    textfile_count = text_source.count(begin_date, end_date)
    
    if begin_date == date.min:
        begin_date = min(date_values)
    if end_date == date.today():
        end_date = max(date_values)
    
    delta = timedelta(days=1)
    
    iter_date = begin_date
    while (iter_date <= end_date):
        if textfile_count == 0:
            break
        
        print("*" * 100)
        print(f"Date: {iter_date} processing...")
        print("*" * 100)
        daily_textfile_count = text_source.count(iter_date, iter_date)
        # if date in dates:
        #     textfile_count -= daily_textfile_count
        #     continue
        
        if DateTime.is_weekend(iter_date):
            if daily_textfile_count != -1:
                textfile_count -= daily_textfile_count
            iter_date += delta
            continue
        
        text_files = text_source.read(iter_date)
        if not text_files:
            continue
        
        try:
            htmls = [x.Html for x in text_files]
            dts = [x.Dt for x in text_files]
            
            frame_helper.create_frame_dicts(htmls, dts, insert_fund_handler)
            iter_date += delta
            textfile_count -= 1
        
        except Exception as error:
            print(error)
 
 
def insert_fundvalue_handler(frame_dict: dict):
    
    sqlserver_fundvalue.insert(frame_dict)

def insert_fund_handler(frame_dict):
    
    sqlserver_fund.insertall(frame_dict)