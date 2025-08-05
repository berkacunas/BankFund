from datetime import datetime, date
from collections import namedtuple
import codecs
import sqlite3

from entities.Interfaces import HtmlSource

from globals.globals import SQLITE_DB_PATH
from globals.DateTime import from_julian, to_julian
import globals.DataFormat as DataFormat


def select(dt : date) -> list:
    ''' date format must be YYYY/MM/DD '''
    
    conn = None
    html_sources = None
    
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # sql = "SELECT id, Html, Dt FROM HtmlSource WHERE Dt = ?"
        sql = "SELECT id, Html, Dt FROM HtmlSource WHERE strftime('%Y-%m-%d', Dt) = ?"
        
        cursor.execute(sql, (dt, ))
        rows = cursor.fetchall()
    
        if rows:
            html_sources = []
            for row in rows:
                
                html = None
                if isinstance(row[1], bytes):
                    html = codecs.decode(row[1])
                else:
                    html = row[1]
                
                html_source = HtmlSource(row[0], None, DataFormat.fix_title(DataFormat.fix_comma_symbol(html)), from_julian(row[2]))
                # html_source = HtmlSource(row[0], DataFormat.clear_text(row[1]), from_julian(row[2]))
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

def count(begin_date : date = date.min, end_date : date = date.today()) -> int:
    
    conn = None
    sql = None
    count = -1
    try:    
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        begin_date = datetime(begin_date.year, begin_date.month, begin_date.day, 0, 0, 0)
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
        
        begin_julian = to_julian(begin_date)
        end_julian = to_julian(end_date)
        
        sql = "SELECT COUNT(id) FROM HtmlSource WHERE Dt BETWEEN ? AND ?;"
        
        cursor.execute(sql, (begin_julian, end_julian, ))
        
        row = cursor.fetchone()
        if row and row[0]:
            count = int(row[0])
            
        cursor.close()
        
        return count
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
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
