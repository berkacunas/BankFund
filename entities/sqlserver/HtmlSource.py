from datetime import datetime, date
from collections import namedtuple
import pymssql

import globals.DataFormat as DataFormat
from globals.globals import SQLSERVER_NAME, SQLSERVER_DB

HtmlSource = namedtuple('HtmlSource', ['id', 'Html', 'Dt'])


def select(dt : date) -> list:
    ''' date format must be YYYY/MM/DD '''
    
    conn = None
    html_sources = None
    
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        # SELECT * FROM HtmlSource WHERE (SELECT CAST(Dt AS Date)) = '2025-06-17'
        sql = "SELECT id, Html, Dt FROM HtmlSource WHERE (SELECT CAST(Dt AS Date)) = %s"
        cursor.execute(sql, (dt, ))
        rows = cursor.fetchall()
    
        if rows:
            html_sources = []
            for row in rows:
                html_source = HtmlSource(row[0], DataFormat.clear_text(row[1]), row[2])
                html_sources.append(html_source)
            
        cursor.close()
        
        return html_sources
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
    finally:
        if conn:
            conn.close()

def insert(html: str):
    
    sql = "INSERT INTO HtmlSource(Dt, Html) VALUES(%s, %s)"
    
    try:
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)  
        curr = conn.cursor()
        
        curr.execute(sql, (datetime.now(), html, ))
        conn.commit()
        
    except Exception as error:
        conn.rollback()
        raise Exception(f"{type(error)}: {error}")
        
    finally:
        if conn:
            conn.close()

def count(begin_date : date = date.min, end_date : date = date.today()) -> int:
    
    conn = None
    sql = None
    count = -1
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(id) FROM HtmlSource WHERE (SELECT CAST(Dt AS Date)) <= %s AND (SELECT CAST(Dt AS Date)) >= %s;" 
        cursor.execute(sql, (begin_date, end_date))
        
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

