from collections import namedtuple
from datetime import datetime, date
from decimal import Decimal
import csv
import pymssql

from contextmanager import MsSqlContext as sqlserver_context

from entities.Interfaces import FundValue, FundValueDuplicate

from entities.sqlserver import Fund as fund
from entities.sqlserver import FundType as fund_type

from globals.DateTime import is_weekend
import globals.DataFormat as DataFormat
from globals.globals import SQLSERVER_NAME, SQLSERVER_DB


def select_by_code(code: str, begin_date : date = date.min, end_date : date = date.today()) -> list:
    
    fundvalues = None
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT id, Code, Dt, FundId, Currency, UnitSharePrice, RiskLevel, DailyReturn, MonthlyReturn, ThreeMonthReturn, FromNewYear, Description FROM FundValue WHERE Code = %s AND (Dt >= %s AND Dt <= %s);"
            
            curr.execute(sql, (code, begin_date, end_date, ))
            rows = curr.fetchall()
            curr.close()
            
            if rows:
                fundvalues = []
                for row in rows:
                    fundvalue = FundValue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    fundvalues.append(fundvalue)
        
            return fundvalues
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
                 
def select_by_date(dt: date) -> list:
    
    fundvalues = None
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT id, Code, Dt, FundId, Currency, UnitSharePrice, RiskLevel, DailyReturn, MonthlyReturn, ThreeMonthReturn, FromNewYear, Description FROM FundValue WHERE Dt = %s;"
            
            curr.execute(sql, (dt, ))
            rows = curr.fetchall()
            curr.close()
                        
            if rows:
                fundvalues = []
                for row in rows:
                    fundvalue = FundValue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                    fundvalues.append(fundvalue)
            
            return fundvalues
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")

def select_all() -> list:
    
    fundvalues = None
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT id, Code, Dt, FundId, Currency, UnitSharePrice, RiskLevel, DailyReturn, MonthlyReturn, ThreeMonthReturn, FromNewYear, Description FROM FundValue;"
            
            curr.execute(sql)
            rows = curr.fetchall()
            curr.close()
            
            if rows:
                fundvalues = []
                for row in rows:
                    fundvalue = FundValue(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    fundvalues.append(fundvalue)
            
            return fundvalues
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")

def select_id_list(code: str, dt: datetime, fund_id: int) -> list:
    
    id_list = None
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT id FROM FundValue WHERE Code = %s AND Dt = %s AND FundId = %s"
            
            curr.execute(sql, (code, dt, fund_id, ))
            rows = curr.fetchall()
            curr.close()
            
            if rows:
                id_list = []
                for row in rows:
                    id = int(row[0])
                    id_list.append(id)
        
        return id_list
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
        
def is_exists(fund_id: int, dt: date) -> bool:
    
    is_exists = False;
    try:    
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT COUNT(id) FROM FundValue WHERE FundId = %s AND (SELECT CAST(Dt AS Date)) = %s;"
            
            curr.execute(sql, (fund_id, dt, ))
            row = curr.fetchone()
            curr.close()
            
            if row and row[0]:
                if isinstance(row[0], int):
                    is_exists = int(row[0]) > 0
            
            return is_exists
    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
def insert(frame_dict: dict):
    
    try:    
        with sqlserver_context.create_connection() as conn:
            sql = "INSERT INTO FundValue(Code, Dt, FundId, Currency, UnitSharePrice, RiskLevel, DailyReturn, MonthlyReturn, ThreeMonthReturn, FromNewYear, Description) " \
                                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            curr = conn.cursor()
            
            for key, value in frame_dict.items():
                fundtype_id = fund_type.select_id(key)
                
                if fundtype_id > 0:
                    for index, row in value.iterrows():
                        print(f"{key} => {row.Title}")

                        fund_id = fund.select_id(row.Title)
                        if is_exists(fund_id, row.Dt.date()):
                            continue
                    
                        # print(f"1 - UnitSharePrice: {row.UnitSharePrice} | DailyReturn: {row.DailyReturn} | MonthlyReturn: {row.MonthlyReturn} | ThreeMonthReturn: {row.ThreeMonthReturn} | FromNewYear: {row.FromNewYear} | Dt: {row.Dt}")
                        unit_share_price = DataFormat.clear_text(row.UnitSharePrice)
                        daily_return = DataFormat.clear_text(row.DailyReturn)
                        monthly_return = DataFormat.clear_text(row.MonthlyReturn)
                        three_month_return = DataFormat.clear_text(row.ThreeMonthReturn)
                        from_new_year = DataFormat.clear_text(row.FromNewYear)
                        # print(f"2 - UnitSharePrice: {unit_share_price} | DailyReturn: {daily_return} | MonthlyReturn: {monthly_return} | ThreeMonthReturn: {three_month_return} | FromNewYear: {from_new_year} | Dt: {row.Dt}")
                        
                        if fund_id > 0:
                            curr.execute(sql, (row.Code, row.Dt, fund_id, row.Currency, unit_share_price, row.RiskLevel, 
                                            daily_return, monthly_return, three_month_return, from_new_year, row.Title, ))
                            conn.commit()
                            print(f"FundValue => Code: {row.Code} | Title: {row.Title} | UnitSharePrice: {unit_share_price} | DailyReturn: {daily_return} | MonthlyReturn: {monthly_return} | ThreeMonthReturn: {three_month_return} | FromNewYear: {from_new_year} | Dt: {row.Dt} added.")
                            
                        else:
                            print(f"Cannot find fund: {row.Title}")
                            new_fund = fund.create(row.Code, row.Title, 1, fundtype_id, row.Dt)
                            fund.insert(new_fund)
                            print(f"Fund created: {row.Title}")
                            insert(frame_dict)
                else:
                    print(f"Cannot find fund type: {key}")
                    
            curr.close()
            
                    
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
        

def select_dates(begin_date: date = date.min, end_date: date = date.today()) -> list:
    
    dates = []
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "SELECT DISTINCT(Dt) FROM FundValue WHERE (SELECT CAST(Dt AS Date)) BETWEEN %s AND %s ORDER BY Dt ASC;"
            curr.execute(sql, (begin_date, end_date, ))
            rows = curr.fetchall()
            
            if rows:
                for row in rows:
                    date = row[0].date()
                    dates.append(date)
                    
            curr.close()
            
            return dates
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
            
def get_duplicate_entries(code: str = None) -> list:
    
    duplicates = None
    try:
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
        
            if code:
                sql = "SELECT Code, FundId, Dt, UnitSharePrice, COUNT(*) FROM FundValue WHERE Code = %s GROUP BY Code, FundId, Dt, UnitSharePrice HAVING COUNT(Dt) > 1 AND COUNT(UnitSharePrice) > 1"
                curr.execute(sql, (code, ))
            else:
                sql = "SELECT Code, FundId, Dt, UnitSharePrice, COUNT(*) FROM FundValue GROUP BY Code, FundId, Dt, UnitSharePrice HAVING COUNT(Dt) > 1 AND COUNT(UnitSharePrice) > 1"
                curr.execute(sql)
            
            rows = curr.fetchall()
            
            if rows:
                duplicates = []
                for row in rows:
                    duplicate = FundValueDuplicate(row[0], int(row[1]), row[2], Decimal(row[3]), int(row[4]))
                    duplicates.append(duplicate)
                    
            curr.close()
                
            return duplicates
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")

def get_weekend_entries(code: str = None) -> list:
    
    raise NotImplementedError(f"FundValue::get_weekend_entries(code: str = None) -> list not implemented yet !")

def delete(id: int):
    
    try:    
        with sqlserver_context.create_connection() as conn:
            curr = conn.cursor()
            
            sql = "DELETE FROM FundValue WHERE id = %s;"

            curr.execute(sql, (id, ))
            conn.commit()
            curr.close()
        
    except Exception as error:
        raise Exception(f"{type(error)}: {error}")
    
def delete_duplicate_entries(duplicates: list = None) -> int:
    
    deleted = 0
    
    if not duplicates:
        duplicates = get_duplicate_entries()
        
    if not duplicates:
        return
    
    for duplicate in duplicates:
        id_list = select_id_list(duplicate.Code, duplicate.Dt, duplicate.FundId)
        
        for i in range(1, len(id_list)):    # First record is not duplicate. Skip it.
            delete(id_list[i])
            deleted += 1
            
    return deleted

def delete_weekend_entries() -> int:
    
    deleted = 0
    fund_values = select_all()
    for fund_value in fund_values:
        if is_weekend(fund_value.Dt):
            delete(fund_value.id)
            deleted += 1
    
    return deleted
             
def to_csv(filename):

    fund_values = select_all()
    
    with open(filename, "w", newline='', encoding="UTF-8") as f:
        
        header = ['id', 'Code', 'Dt', 'FundId', 'Currency', 'UnitSharePrice','RiskLevel', 'DailyReturn', 'MonthlyReturn', 'ThreeMonthReturn', 'FromNewYear', 'Description']
        
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        
        row_list = []
        for fund_value in fund_values:
            row_dict = {
                header[0]: fund_value.id,
                header[1]: fund_value.Code,
                header[2]: fund_value.Dt,
                header[3]: fund_value.FundId,
                header[4]: fund_value.Currency,
                header[5]: fund_value.UnitSharePrice,
                header[6]: fund_value.RiskLevel,
                header[7]: fund_value.DailyReturn,
                header[8]: fund_value.MonthlyReturn,
                header[9]: fund_value.ThreeMonthReturn,
                header[10]: fund_value.FromNewYear,
                header[11]: fund_value.Description
            }
            
            row_list.append(row_dict)
        
        if len(row_list) > 0:
            writer.writerows(row_list)
        
        #     writerows([["foo", "bar", "spam"],
        #    ["oof", "rab", "maps"],
        #    ["writerow", "isn't", "writerows"]])
            
        # writer.writerow(
        #     {'Organization' : 'Google', 
        #      'Established': '1998', 
        #      'CEO': 'Sundar Pichai'}
        #     )
