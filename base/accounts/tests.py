# import random
# import string
#
# def randomString(stringLength=64):
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))
#
#
# print ("Random String is ", randomString() )

#
# import datetime
#
# x = datetime.datetime(2018, 6, 1)
#
# print(x)


import time
import datetime
# d = datetime.date(2015,21,5)
#
# print(time.mktime(d.timetuple())
#       )
from datetime import datetime, timedelta
curr = datetime.now()
fut = datetime.now() + timedelta(days = 30)
import datetime
d = datetime.datetime(fut.year, fut.month, fut.day)
epoch = time.mktime(d.timetuple())
current = int(epoch)
print(current)
print(curr)