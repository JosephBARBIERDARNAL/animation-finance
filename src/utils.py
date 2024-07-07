from datetime import datetime


def format_date(date):
    date_string = str(date)
    date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")
    month_name = date_obj.strftime("%B")
    year = date_obj.year
    return f"{month_name} {year}"
