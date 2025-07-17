from datetime import datetime, date
from collections import namedtuple
from decimal import Decimal
import sqlite3

from globals.globals import SQLITE_DB_PATH
from globals.DateTime import from_julian, to_julian
import globals.DataFormat as DataFormat

HtmlSource = namedtuple('HtmlSource', ['id', 'Html', 'Dt'])

def select(dt : date) -> list:
    ''' date format must be YYYY/MM/DD '''
    
    date_dict = select_dates()
    
    conn = None
    html_sources = None
    
    julian_dt = -1
    for key, value in date_dict.items():
        if dt == key.date():
            julian_dt = value
    
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # SELECT * FROM HtmlSource WHERE (SELECT CAST(Dt AS Date)) = '2025-06-17'
        sql = "SELECT id, Html, Dt FROM HtmlSource WHERE Dt = ?"
        cursor.execute(sql, (julian_dt, ))
        rows = cursor.fetchall()
    
        if rows:
            html_sources = []
            for row in rows:
                html_source = HtmlSource(row[0], DataFormat.clear_text(row[1]), from_julian(row[2]))
                html_sources.append(html_source)
            
        cursor.close()
        
        return html_sources
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def insert(html: str):
    
    sql = "INSERT INTO HtmlSource(dt, html) VALUES(?, ?)"

    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        curr = conn.cursor()
        
        curr.execute(sql, (to_julian(datetime.now()), html, ))
        conn.commit()
        
    except Exception as error:
        conn.rollback()
        print(error)

    finally:
        if conn:
            conn.close()

def select_dates() -> dict:
    
    conn = None
    dates = {}
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        curr = conn.cursor()
        
        sql = "SELECT DISTINCT(Dt) FROM HtmlSource ORDER BY Dt ASC;"
        curr.execute(sql)
        
        rows = curr.fetchall()
        
        if rows:
            for row in rows:
                # 'dates' dict object stores Sqlite 'Dt' column value in two different forms. 
                # Key stores Dt value as datetime. 
                # Value stores Dt Value julian date as Decimal.
                dates[from_julian(row[0])] = row[0]
                
        return dates
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
            
    finally:
        if conn:
            conn.close()
