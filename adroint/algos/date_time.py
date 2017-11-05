import parsedatetime
from datetime import datetime


# identify date
def get_datetime_details(text):
    p = parsedatetime.Calendar()
    time_struct, parse_status = p.parse(text)
    # print time_struct, parse_status
    if parse_status != 0: return datetime(*time_struct[:6])
    return 'error'


# temp = ['midnight','morning','breakfast','noon','lunch','afternoon','evening','dinner','night']
# temp = ['today','tomorrow','friday','next monday','25th aug','11 jul','15th march next year','12/25','12.25','1/7/2020','1.7.2020']
# temp = ['10 days later','2 weeks later','4 months later','1 year later','in 9 days','5 days from next monday','one week and one day later']


"""print get_datetime_details("this month")"""
"""print get_datetime_details("next month")"""
"""print get_datetime_details("next year")"""
"""print get_datetime_details("next week")"""