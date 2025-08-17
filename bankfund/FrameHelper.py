from datetime import datetime

import numpy as np
import pandas as pd
from io import StringIO

import bankfund.HtmlParser as html_parser
from bankfund.utilities.naming import rename_columns_dict

def split_Code_Dt_Title_column(frame: pd.DataFrame, dt):
    
    temp_frame = frame["Code Dt Title"].str.split(" ", n=4, expand=True)
    frame["Code"] = temp_frame[0]
    frame["Dt"] = dt
    frame["Title"] = temp_frame[4]
    frame.drop(columns=["Code Dt Title"], inplace=True)
    
    return frame

def realign_frame(frame: pd.DataFrame):
    
    return frame.loc[:, ['Code', 'Dt', 'Title', 'Currency', 'UnitSharePrice', 'RiskLevel', 'DailyReturn', 'MonthlyReturn', 'ThreeMonthReturn', 'FromNewYear']]

def get_empty_row_indexes(frame: pd.DataFrame) -> list:
                
    np_idx_empty_rows = np.where(frame.loc[:, 'Title'].isnull())[0]
    indexes = list(np_idx_empty_rows.tolist())
    indexes.pop(0)
    
    return indexes

class FrameHelper:
    
    def create_frame_dict(self, html: str, dt: datetime) -> dict:
        
        m_frame = pd.read_html(StringIO(html))[0]
        html_parser.rename_frame(m_frame, rename_columns_dict, True)
        html_parser.mask_frame(m_frame, m_frame == '', inplace=True)
        m_frame.dropna(axis=1, how='any', inplace=True)
        m_frame = split_Code_Dt_Title_column(m_frame, dt)
        m_frame = realign_frame(m_frame)
                
        indexes = get_empty_row_indexes(m_frame)
        fund_types_frame = html_parser.get_fund_types_frame(m_frame)
        frame_dict = html_parser.create_framedict(m_frame, fund_types_frame["Code"], indexes)
        
        return frame_dict
        
    def create_frame_dicts(self, htmls: list, dts: list, callback=None):
        
        frame_dict_list = []
        for i in range(len(htmls)):
            frame_dict = self.create_frame_dict(htmls[i], dts[i])
            
            if not frame_dict:
                print('frame_dict is None')
            
            frame_dict_list.append(frame_dict)
            
            if callback:
                callback(frame_dict)
        return frame_dict_list
