from datetime import datetime


def format_date(date):
    date_string = str(date)[:10]
    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    month_name = date_obj.strftime("%B")
    day = date_obj.day
    year = date_obj.year
    return f"{month_name} {day}, {year}"
