from contextlib import contextmanager, asynccontextmanager
import pymssql

from globals.globals import SQLSERVER_NAME, SQLSERVER_DB

@contextmanager
def create_connection():
    
    conn = None
    try:
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        yield conn
    finally:
        try:
            conn.close()
            
        except Exception as error:
            print(error)

@asynccontextmanager
async def create_async_connection():
    
    conn = None
    try:
        conn = await pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        yield conn
        
    finally:
        conn.close()

        