import os
from datetime import datetime
from io import StringIO
import re
import pandas as pd
import numpy as np

from globals.globals import XLSX_DIR, DATETIME_NOW_FORMAT
from Exceptions import HtmlContentNotFoundError

def read_html_from_file(html_source_file: str) -> str:
    
    html = None
    try:
        with open(html_source_file, 'r', encoding='UTF-8') as f: 
            html = f.read()
    except: 
        raise
        
    if not html:
        raise HtmlContentNotFoundError(f"Cannot find html in {html}")

    return clear_html(html)


def clear_html(html: str) -> str:
    
    html = remove_unwanted_texts(html)
    html = replace_decimal_separator(html)
    
    return html
    
def remove_unwanted_texts(html: str) -> str:
    
    replace_substrings = ["<p>Yurt dışı piyasaların kapalı olduğu günlerde açıklanan fon fiyatı, piyasaların açık olduğu son gün hesaplanan değerleme fiyatıdır.</p>",
                          "<p>Günlük fiyat açıklamamakta olup, web sitesinde yer alan fiyatlar alım-satım günlerinde alım-satıma konu olan resmi fiyatlar, diğer günlerde ise referans fiyatlardır.</p>"
                         ]
    
    for replace_substring in replace_substrings: 
        pos = html.find(replace_substring)
        if pos != -1:
            html = html.replace(replace_substring, "")
            
    return html


def replace_decimal_separator(html) -> str:
    
    return html.replace(",", ".")


def get_fund_types_frame(frame: pd.DataFrame) -> pd.DataFrame:
    
    temp_fund_types_frame = pd.DataFrame()
    fund_types_frame = frame.query("Title.isnull()", engine='python')
    temp_fund_types_frame["Code Count"] = fund_types_frame["Currency"]
    temp_fund_types_frame["Code"] = temp_fund_types_frame["Code Count"].str.split("(").str[0].astype(str)
    temp_fund_types_frame["Count"] = temp_fund_types_frame["Code Count"].str.split("(").str[1].str.split(")").str[0].astype(int)
    temp_fund_types_frame.drop(columns=["Code Count"], inplace=True)
    temp_fund_types_frame.reset_index(drop=True, inplace=True)
    
    return temp_fund_types_frame

def get_funds_series(frame: pd.DataFrame) -> pd.Series:
    
    fund_series = frame.Title;
    
    return fund_series

def create_framedict(frame, series, indexes) -> dict:

    frame_dict = {}
    start_index = 1
    for index in indexes:
        sub_frame = frame.iloc[start_index:index]
        key = series.iloc[len(frame_dict)].strip()
        frame_dict[key] = sub_frame
        start_index = index + 1
    
    sub_frame = frame.iloc[start_index:len(frame)]
    key = series.iloc[len(frame_dict)].strip()
    frame_dict[key] = sub_frame
    
    return frame_dict
        
def write_framedict_to_xlsx(frame_dict):
    
    for key, value in frame_dict.items():
        value.to_excel(f"{os.path.join(XLSX_DIR, key)}_{str(datetime.now().strftime(DATETIME_NOW_FORMAT))}.xlsx")
    
def rename_frame(frame: pd.DataFrame, rename_dict: dict, inplace=False):
    
    return frame.rename(columns=rename_dict, inplace=inplace)

def mask_frame(frame, condition, inplace=False):
    
    return frame.mask(condition, inplace=inplace)
    


