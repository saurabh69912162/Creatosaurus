# import time
# from datetime import  datetime
# print(time.time())
# print(int(datetime.now().timestamp()))


import time
import datetime
d = datetime.datetime(2019,10,13,21,37,0)
print(time.mktime(d.timetuple()))