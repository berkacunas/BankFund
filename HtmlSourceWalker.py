from datetime import date, timedelta

from globals import DateTime

from FrameHelper import FrameHelper

frame_helper = FrameHelper()

def walk(html_source, callback, begin_date : date = date.min, end_date : date = date.today()):
    
    dates = html_source.select_dates()
    date_values = [x for x in dates.keys()]
    
    if begin_date == date.min:
        begin_date = min(date_values)
    if end_date == date.today():
        end_date = max(date_values)
        
    htmlsource_count = html_source.count(begin_date, end_date)
    
    delta = timedelta(days=1)
    
    iter_date = begin_date
    while (iter_date <= end_date):
        if htmlsource_count == 0:
            break
        
        print("*" * 100)
        print(f"Date: {iter_date} processing...")
        print("*" * 100)
        daily_htmlsource_count = html_source.count(iter_date, iter_date)
        # if date in dates:
        #     textfile_count -= daily_textfile_count
        #    
        
        if DateTime.is_weekend(iter_date):
            if daily_htmlsource_count != -1:
                htmlsource_count -= daily_htmlsource_count
            iter_date += delta
            continue
        
        html_sources = html_source.select(iter_date)
        if not html_sources:
            continue
        
        try:
            htmls = [x.Html for x in html_sources]
            dts = [x.Dt for x in html_sources]
            
            frame_helper.create_frame_dicts(htmls, dts, callback)
            iter_date += delta
            htmlsource_count -= 1
            
        
        except Exception as error:
            raise error
