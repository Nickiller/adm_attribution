import sys,time,datetime
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime as dt

TIME_FORMAT = "%Y%m%d%H%M%S"
def conv_time(time_str):
    return dt.strptime(time_str,TIME_FORMAT)
