import pymssql
import pandas as pd

from globals.globals import SQLSERVER_NAME, SQLSERVER_DB

def select_id(fundtype_title: str) -> int:
    
    conn = None
    id = -1
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "SELECT id FROM FundType WHERE Title = %s"
        cursor.execute(sql, (fundtype_title, ))
        row = cursor.fetchone()
        if row and row[0]:
            if isinstance(row[0], int):
                id = int(row[0])
            
        cursor.close()
        
        return id
    
    except pymssql.exceptions.IntegrityError as i_error:
        raise Exception(f"IntegrityError: {i_error}")
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def is_exists(title: str) -> bool:
    
    conn = None
    is_exists = False
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(id) FROM FundType WHERE Title = %s"
        
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
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "INSERT INTO FundType(Title, FundCount) VALUES(%s, %s)"
        
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
