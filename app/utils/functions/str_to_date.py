import datetime

def str_to_date(s):
    str_date = s[:10].split('-')
    year, month, date = int(str_date[0]), int(str_date[1]), int(str_date[2])
    return datetime.datetime(year, month, date)
    