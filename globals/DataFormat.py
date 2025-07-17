import pymssql
from globals.globals import SQLSERVER_NAME, SQLSERVER_DB, REMOVE_STRINGS

def clear_text(text: str) -> str:
    
    text = fix_title(text)
    text = clear_doublefullstop(text)
    text = fix_minus_and_percentage_symbols(text)
    text = fix_comma_symbol(text)
    text = set_null_for_dash_symbol(text)
    
    return text

def fix_title(text: str) -> str:
    
    for REMOVE_STRING in REMOVE_STRINGS:
        text = text.replace(REMOVE_STRING, '').strip()
        
    return text

def clear_doublefullstop(text: str) -> str:
    
    count = text.count(".")
    if count > 1:
        index = text.index(".")
        text = text.replace(".", "", count - 1)
    
    return text

def fix_minus_and_percentage_symbols(text: str) -> str:
    
    if "-" in text:
        if "%" in text:
            text = text.replace("- %", "-%")
            text = text.replace("%", "")
    elif "%" in text:
        text = text.replace("% ", "")
            
    return text

def fix_comma_symbol(text: str) -> str:
    
    return text.replace(",", ".")

def set_null_for_dash_symbol(text):
    
    if text == "-":
        return None

    return text
