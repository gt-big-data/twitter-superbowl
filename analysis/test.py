from datetime import datetime
import calendar

start = '2014-02-02 23:30:00' #6:30 pm EST
startdate = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
millistart = calendar.timegm(startdate.utctimetuple())
