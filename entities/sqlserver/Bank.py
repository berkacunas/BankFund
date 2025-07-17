import pymssql

from globals.globals import SQLSERVER_NAME, SQLSERVER_DB

        
def select_bank_id(bank_name: str) -> int:
    
    conn = None
    id = -1
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "SELECT id FROM Bank WHERE Title = %s"
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
