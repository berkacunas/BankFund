SQLITE_DB_PATH = "C:/berk/Documents/Databases/BankFunds/sqlite/BankFunds.db"
URL = "https://www.isportfoy.com.tr/getiri-ve-fiyatlar"

SQLSERVER_NAME = "PC-WINDOWS10"
SQLSERVER_DB = "BankFunds"

HTML_DIR = "./html"
XLSX_DIR = "./xlsx"

REMOVE_STRINGS = [u"Yurt dışı piyasaların kapalı olduğu günlerde açıklanan fon fiyatı. piyasaların açık olduğu son gün hesaplanan değerleme fiyatıdır.",
                  u"İş Portföy Hedef Serbest Fon  Günlük fiyat açıklamamakta olup. web sitesinde yer alan fiyatlar alım-satım günlerinde alım-satıma konu olan resmi fiyatlar. diğer günlerde ise referans fiyatlardır.",
                  u"Günlük fiyat açıklamamakta olup. web sitesinde yer alan fiyatlar alım-satım günlerinde alım-satıma konu olan resmi fiyatlar. diğer günlerde ise referans fiyatlardır."]
                  
DEFAULT_JULIAN_FORMAT = 'jd'

DEFAULT_DATETIME_FORMAT = '"%Y-%m-%d %H:%M:%S.%f"'
DATETIME_NOW_FORMAT = "%d-%m-%Y %H:%M:%S"
DATETIME_NOW_FILE_FORMAT = "%Y-%m-%d_%H-%M-%S"

rename_columns_dict = {
    'Fon Kodu Fon Adı': 'Code Dt Title', 
    'Para Birimi': 'Currency', 
    'Birim Pay Fiyatı': 'UnitSharePrice', 
    'Risk Seviyesi': 'RiskLevel',
    'Günlük Getiri': 'DailyReturn', 
    'Aylık Getiri': 'MonthlyReturn', 
    '3 Aylık Getiri': 'ThreeMonthReturn', 
    'Yılbaşından': 'FromNewYear' 
}


