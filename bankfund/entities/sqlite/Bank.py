import sqlite3

from bankfund.entities.Interfaces import Bank
from bankfund.utilities.naming import SQLITE_DB_PATH
    
def select_id(bank_name: str) -> int:
    
    conn = None
    id = -1
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        sql = "SELECT id FROM Bank WHERE Title = ?"
        cursor.execute(sql, (bank_name, ))
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

def insert(bank: Bank):
    
    conn = None
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
            
        sql = "INSERT INTO Bank(Title, EFTCode, Tel, Fax, Address, Web, Description, AddedOn, LastUpdated) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
        cursor.execute(sql, (bank.Title, bank.EFTCode, bank.Tel, bank.Fax, bank.Address, bank.Web, bank.Description, bank.AddedOn, bank.LastUpdated))
        
        conn.commit()
        cursor.close()
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def initialize():
    
    bank = Bank(None, 'İş Bankası', None, None, None, None, None, None, None, None)
    insert(bank)
    