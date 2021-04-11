from dateutil.relativedelta import relativedelta
from django.utils.datetime_safe import date, datetime

today = date.today()
week_earlier = today - relativedelta(days=7)
this_month = datetime(today.year, today.month, 1)
