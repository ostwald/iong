import datetime
from dateutil.relativedelta import *


def get_iso_day (date_str):
    """
    returns date in form: YYYY-MM-DD
    """

    dt = datetime.datetime.strptime(date_str,'%m/%d/%y')
    return dt.strftime ('%Y-%m-%d')

def get_first_of_next_month (date_str):
    fmt_in = '%m/%d/%y'
    fmt_out = '%-m/%-d/%y'

    n = datetime.datetime.strptime(date_str,fmt_in)
    n = n + relativedelta(months=+1)

    return n.strftime (fmt_out)