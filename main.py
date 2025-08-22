import pprint
from datetime import datetime, date, timedelta
from io import StringIO 
import pandas as pd

from bankfund import HtmlParser

from bankfund.FrameHelper import get_empty_row_indexes, split_Code_Dt_Title_column, realign_frame

from bankfund.utilities import DateTime
from bankfund.utilities.naming import rename_columns_dict, DATETIME_NOW_FILE_FORMAT

from bankfund.entities.sqlite import HtmlSources as sqlite_htmlsources
from bankfund.entities.sqlite import HtmlSources as sqlite_htmlsource
from bankfund.entities.sqlite import Bank as sqlite_bank
from bankfund.entities.sqlite import Fund as sqlite_fund
from bankfund.entities.sqlite import FundType as sqlite_fundtype
from bankfund.entities.sqlite import FundValue as sqlite_fundvalue

from bankfund.entities.sqlserver import HtmlSources as sqlserver_htmlsources
from bankfund.entities.sqlserver import HtmlSources as sqlserver_htmlsource
from bankfund.entities.sqlserver import FundValue as sqlserver_fundvalue

from bankfund.entities.textserver import TextSource as text_source
from bankfund.entities.textserver import TextSources as text_sources

from bankfund.Exceptions import FundTypeNotFoundError

from bankfund.plots import ScatterPlots


def main():
    
    # check_date = date(2025, 8, 5)
    # if sqlserver_fundvalue.is_date_values_inserted(check_date):
    #     print(f'Fund values inserted for date: {check_date}')
    # else:
    #     print(f'Cannot find Fund values for date: {check_date}')
        
    # sqlite_bank.initialize()
    
    try:
        # sources = text_source.select(date(2025, 6, 26))
        # for source in sources:
        #     frame_dict = create_framedict_from_html(source.Dt, source.Html)
        #     sqlite_fund.insert_frame(frame_dict)
        #     break
        
        # sqlite_htmlsources.insert_fundvalues(date(2025, 7, 29))
        # sqlite_duplicates = sqlite_fundvalue.get_duplicate_entries()
        # pprint.pp(sqlite_duplicates, depth=1)
        # sqlite_deleted_duplicate_count = sqlite_fundvalue.delete_duplicate_entries(sqlite_duplicates)
        # sqlite_deleted_weekend_count = sqlite_fundvalue.delete_weekend_entries()
        
        
        # sqlserver_htmlsources.insert_fundvalues(date(2025, 8, 16))
        # sqlserver_duplicates = sqlserver_fundvalue.get_duplicate_entries()
        # if sqlserver_duplicates:
        #     pprint.pp(sqlserver_duplicates, depth=1)
        #     sqlserver_deleted_duplicate_count = sqlserver_fundvalue.delete_duplicate_entries(sqlserver_duplicates)
        sqlserver_deleted_weekend_count = sqlserver_fundvalue.delete_weekend_entries()
        
        # sqlserver_fundvalue.to_csv(f"./csv/FundValue_{datetime.strftime(datetime.now(), DATETIME_NOW_FILE_FORMAT)}.csv")
        # filename = "./csv/FundValue_2025-07-04_21-37-25.csv"

        # fundvalues = sqlserver_fundvalue.select_all()
        # frame = pd.DataFrame(fundvalues)
        # ScatterPlots.plot(frame, date(2025, 6, 10), date(2025, 7, 8))
        # ScatterPlots.scatter(frame)
        
        # html_file_sources = text_source.select(datetime.now().date())
        # text_sources.insert_new_funds()
        # text_sources.insert_fundvalues(datetime.now().date())
        
        # fundvalues = sqlserver_fundvalue.select_last_day_entries()
        # print(fundvalues)
        print()
        
    except ValueError as verror:
        print(f"Value error occured in main()::text_source.read()\n{verror}")
    except FundTypeNotFoundError as ft_error:
        print(f"{type(ft_error)}: {ft_error}")
    except Exception as error:
        print(f"Exception occured: {error}")
    

if __name__ == "__main__":
    main()