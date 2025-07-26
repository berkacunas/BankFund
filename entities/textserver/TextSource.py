import os
from datetime import datetime, date
from collections import namedtuple

from ios import File
import globals.DataFormat as DataFormat
from globals.globals import HTML_DIR, DATETIME_NOW_FILE_FORMAT

HtmlFileSource = namedtuple('HtmlFileSource', ['Filename', 'Html', 'Dt'])

def read(dt: date) -> list:

    html_file_sources = []
    date_dict = list_dates()

    for key, value in date_dict.items():
        
        if value[0] == dt:
            filename = key
    
            with open(filename, "r", encoding="UTF-8") as f:
                text = f.read()
                text = DataFormat.fix_title(DataFormat.fix_comma_symbol(text))
                file_source = HtmlFileSource(filename, text, value[1])
                html_file_sources.append(file_source)
        
    return html_file_sources

def write(filename, html):
    
    count = -1
    with open(filename, mode="w", encoding="UTF-8") as f:
        count = f.write(html)
        
    return count

def count(begin_date : date = date.min, end_date : date = date.today()) -> int:
    
    count = 0
    filenames = File.list_files(HTML_DIR)

    for filename in filenames:
        date = convert_filename_to_datetime(filename).date()
        if date >= begin_date and date <= end_date:
            count += 1
    
    return count

def list_dates() -> dict:
    
    date_dict = {}
    try:
        filenames = File.list_files(HTML_DIR)
        for filename in filenames:
            temp_dt = convert_filename_to_datetime(filename)
            fullname = os.path.join(HTML_DIR, filename)
            date_dict[fullname] = [temp_dt.date(), temp_dt]
        
        return date_dict
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")

def convert_filename_to_datetime(filename: str) -> datetime:
    
    return datetime.strptime(filename.replace('.txt', ''), DATETIME_NOW_FILE_FORMAT)
