from datetime import datetime, date
import pymssql

from bankfund.entities.Interfaces import HtmlSource

import bankfund.utilities.DataFormat as DataFormat
from bankfund.utilities.naming import SQLSERVER_NAME, SQLSERVER_DB


def select(dt : date) -> list:
    
    conn = None
    html_sources = None
    
    try:    
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        cursor = conn.cursor()
        
        sql = "SELECT id, Html, Dt FROM HtmlSource WHERE (SELECT CAST(Dt AS Date)) = %s"
        cursor.execute(sql, (dt, ))
        rows = cursor.fetchall()

        if rows:
            html_sources = []
            for row in rows:
                html_source = HtmlSource(row[0], None, DataFormat.fix_title(DataFormat.fix_comma_symbol(row[1])), row[2])
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
        
        sql = "SELECT COUNT(id) FROM HtmlSource WHERE (SELECT CAST(Dt AS Date) as dt_cast) BETWEEN %s AND %s;"
        
        cursor.execute(sql, (begin_date, end_date, ))
        
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
        conn = pymssql.connect(server=SQLSERVER_NAME, database=SQLSERVER_DB)
        curr = conn.cursor()
        
        sql = "SELECT DISTINCT(Dt) FROM HtmlSource ORDER BY Dt ASC;"
        curr.execute(sql)
        
        rows = curr.fetchall()
        
        if rows:
            for row in rows:
                dates[row[0].date()] = row[0]
                
        return dates
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
            
    finally:
        if conn:
            conn.close()
