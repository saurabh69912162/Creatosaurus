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
d = datetime.date(2015,21,5)

print(time.mktime(d.timetuple())
      )
