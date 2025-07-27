import sqlite3

from globals.globals import SQLITE_DB_PATH
    
def select_bank_id(bank_name: str) -> int:
    
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
