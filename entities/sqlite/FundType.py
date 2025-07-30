import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

from globals.globals import SQLITE_DB_PATH, DATA_DIR

def select_id(fundtype_title: str) -> int:
    
    conn = None
    id = -1
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "SELECT id FROM FundType WHERE Title = ?"
        cursor.execute(sql, (fundtype_title, ))
        row = cursor.fetchone()
        if row and row[0]:
            if isinstance(row[0], int):
                id = int(row[0])
            
        cursor.close()
        
        return id
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def is_exists(title: str) -> bool:
    
    conn = None
    is_exists = False
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(id) FROM FundType WHERE Title = ?"
        
        cursor.execute(sql, (title, ))
        row = cursor.fetchone()
        if row and row[0]:
            is_exists = int(row[0]) > 0
            
        conn.commit()
        cursor.close()
        
        return is_exists
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()
            
def insert(fund_types_frame: pd.DataFrame):

    conn = None
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "INSERT INTO FundType(Title, FundCount) VALUES(?, ?)"
        
        for index, row in fund_types_frame.iterrows():
            if not is_exists(row.Code):
                cursor.execute(sql, (row.Code, row.Count, ))
                print(f"FundType: {row.Code} added.")
                
            
        conn.commit()
        cursor.close()
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def initialize():
    
    fundtypes_file = os.path.join(DATA_DIR, 'Fund-Types.csv')
    try:    
        engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}', echo=False)
        with engine.begin() as conn:
            df = pd.read_csv(fundtypes_file)
            df.to_sql(name='FundType', con=conn, if_exists='fail')
            
    except ValueError as verr:
        print(verr)
        raise verr
    except Exception as error:
        print(error)
        raise error
