from datetime import datetime, date
import sqlite3

from entities.Interfaces import Fund

from entities.sqlite import FundType
from entities.sqlite import Bank

from globals.globals import SQLITE_DB_PATH


def select_id(fund_title: str) -> int:
    
    conn = None
    id = -1
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "SELECT id FROM Fund WHERE Title = ?"
        cursor.execute(sql, (fund_title, ))
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
        
        sql = "SELECT COUNT(id) FROM Fund WHERE Title = ?"
        
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

def insert_many(frame_dict: dict, bank_title :str = 'İş Bankası'):
    
    bank_id = Bank.select_id(bank_title)
    conn = None
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "INSERT INTO Fund(Code, Title, BankId, TypeId, CreatedOn) VALUES(?, ?, ?, ?, ?)"
        
        for frame in frame_dict:
            
            for key, value in frame_dict.items():
                fundtype_id = FundType.select_id(key)
                if fundtype_id > 0:
                    
                    for index, row in value.iterrows():
                        # if not is_fund_exists(row.Title):
                        fund = Fund(None, row.Code, row.Title, bank_id, fundtype_id, datetime.now())
                        insert(fund)
                        # cursor.execute(sql, (row.Code, row.Title, bank_id, fundtype_id, None))
                        print(f"Fund: {fund.Title} added.")
                        
            break
                
        conn.commit()
        cursor.close()
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def insert(fund: Fund):
    
    conn = None
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
            
        sql = "INSERT INTO Fund(Code, Title, BankId, TypeId, CreatedOn) VALUES(?, ?, ?, ?, ?)"
        
        cursor.execute(sql, (fund.Code, fund.Title, fund.BankId, fund.TypeId, fund.CreatedOn, ))
        
        conn.commit()
        cursor.close()
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()
            
def insertall(frame_dict: dict):
    
    conn = None
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "INSERT INTO Fund(Code, Title, BankId, TypeId, CreatedOn) VALUES(?, ?, ?, ?, ?)"

        for key, value in frame_dict.items():
            fundtype_id = FundType.select_id(key)
            
            if fundtype_id > 0:
                for index, row in value.iterrows():
                    print(f"{key} => {row.Title}")

                    fund_id = select_id(row.Title)
                   
                    if fund_id <= 0:
                        print(f"Cannot find fund: {row.Title}")
                        fund = create(row.Code, row.Title, 1, fundtype_id, row.Dt)
                        insert(fund)
                        print(f"Fund created: {row.Title}")
            else:
                raise Exception(f"Error! Undefined FundType: {key}")
                        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()
        
    
def find_new(fund: Fund) -> Fund:
    
    if not is_exists(fund.Title):
        return fund
    return None

def create(code: str, title: str, bank_id: int, type_id: int, created_on: date) -> Fund:
    
    return Fund(None, code, title, bank_id, type_id, created_on)
