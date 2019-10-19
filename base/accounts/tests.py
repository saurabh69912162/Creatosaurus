import random
import string

def randomString(stringLength=64):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


print ("Random String is ", randomString() )