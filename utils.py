import datetime, sys
from dateutil.relativedelta import *

def unescape (s):
    return s.replace ('%27', '&apos;')

def get_iso_date (date_str):
    in_time_fmt = '%m/%d/%y %H:%M'
    dt = datetime.datetime.strptime(date_str, in_time_fmt)
    sortable_time_fmt = '%Y-%m-%d %H:%M'
    return dt.strftime(sortable_time_fmt)

def get_iso_day (date_str):
    """
    returns date in form: YYYY-MM-DD
    """

    dt = datetime.datetime.strptime(date_str,'%m/%d/%y')
    return dt.strftime ('%Y-%m-%d')

def get_first_of_next_month_OLD (date_str):
    fmt_in = '%m/%d/%y'
    fmt_out = '%-m/%-d/%y'

    n = datetime.datetime.strptime(date_str,fmt_in)
    n = n + relativedelta(months=+1)

    return n.strftime (fmt_out)

def get_first_of_next_month (date_str):
    fmt_in = '%Y-%m-%d'
    fmt_out = '%Y-%m-%d'

    n = datetime.datetime.strptime(date_str,fmt_in)
    n = n + relativedelta(months=+1)

    return n.strftime (fmt_out)

def get_human_date (date_str):
    day_fmt_in = '%Y-%m-%d'
    day_fmt_out = '%-m/%-d/%y'
    try:
        n = datetime.datetime.strptime(date_str,day_fmt_in)
        return n.strftime(day_fmt_out)
    except ValueError:
        try:
            date_fmt_in = '%Y-%m-%d %H:%M'
            date_fmt_out = '%-I:%M %p %-m/%-d/%y '
            n = datetime.datetime.strptime(date_str,date_fmt_in)
            return n.strftime(date_fmt_out)
        except:
            print sys.exc_info()
            print "WARN: could not parse date: {}".format(date_str)
            return date_str


def get_last_name_where_clause(num):
    if num < ord('A'):
        return "UPPER(lastname) < 'A'"
    else:
        return "UPPER(lastname) LIKE '{}%'".format(chr(num))

def print_lastname_where_clauses():

    for i in range (ord('A')-1, ord('Z')+1):
        print get_last_name_where_clause(i)

if __name__ == '__main__':
    date_str = '2017-03-05 09:50'
    print get_human_date(date_str)

    print_lastname_where_clauses()