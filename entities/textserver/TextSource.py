import os
from datetime import datetime, date

from entities.Interfaces import HtmlSource
from ios import File

import globals.DataFormat as DataFormat
from globals.globals import HTML_DIR, DATETIME_NOW_FILE_FORMAT


def select(dt: date) -> list:

    html_file_sources = []
    date_dict = select_dates()

    for key, value in date_dict.items():
        
        if key == dt:
            filename = f'{datetime.strftime(value, DATETIME_NOW_FILE_FORMAT)}.txt'
            fullname = os.path.join(HTML_DIR, filename)
    
            with open(fullname, "r", encoding="UTF-8") as f:
                text = f.read()
                text = DataFormat.fix_title(DataFormat.fix_comma_symbol(text))
                file_source = HtmlSource(None, fullname, text, value)
                html_file_sources.append(file_source)
        
    return html_file_sources

def insert(filename, html):
    
    count = -1
    with open(filename, mode="w", encoding="UTF-8") as f:
        count = f.write(html)
        
    return count

def count_range(begin_date : date = date.min, end_date : date = date.today()) -> int:
    
    count = 0
    filenames = File.list_files(HTML_DIR)

    for filename in filenames:
        date = convert_filename_to_datetime(filename).date()
        if date >= begin_date and date <= end_date:
            count += 1
    
    return count

def count(date: date):
    
    return count_range(date, date)

def select_dates() -> dict:
    
    date_dict = {}
    try:
        filenames = File.list_files(HTML_DIR)
        for filename in filenames:
            temp_dt = convert_filename_to_datetime(filename)
            fullname = os.path.join(HTML_DIR, filename)
            date_dict[temp_dt.date()] = temp_dt
        
        return date_dict
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")

def convert_filename_to_datetime(filename: str) -> datetime:
    
    return datetime.strptime(filename.replace('.txt', ''), DATETIME_NOW_FILE_FORMAT)
