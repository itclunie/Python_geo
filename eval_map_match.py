#Faster matching b/t lists:-------------------------------------------------
a= [1,2,3,4,5,6,7]
b = [5,6,7,8,9,19]

# for x in a:
    # for y in b:
        # if x == y:
            # print (x,y)
 
print set(a) & set(b) #faster matching

#Eval-------------------------------------------------------------
testr = ['abc','aaa','qrq']
for item in testr:
    eval(compile("if 'aaa' in '" + item + "': tmp = 'y'", '<string>', 'exec'))
    if tmp == 'y': print 't'
    else: print 'f'
        
    tmp = ''

#iterate over dates----------------------------------------------------------
from datetime import timedelta, date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
start_date = date(2013, 1, 1)
end_date = date(2015, 6, 2)
for single_date in daterange(start_date, end_date):
    print single_date.strftime("%Y,%m,%d")


#json prettyprint-------------------------------------------------------------------
import json
jsonpath = r'J:\Shared\whatever\rawjson.js'
parsed = json.load(jsonpath)
formatted = json.dumps(parsed, indents=4,sort_keys=True)
Then you can just write the 'formatted' string to a text file.


#numpy & map------------------------------------------------------------------------
import numpy as np
import array
def d2s(list):
    # 'digits to string
    return array.array('B', list).tostring()
def s2d(string):
    # 'string to digits
    return map(ord, string)
def npAry(listOdigits):
    return np.array(listOdigits, int)
    
strList = ['a', 'bob', 'cat', 'b'] #list of strings
digitList = map(s2d, strList)      #convert to digits
# reStrLst = map(d2s, digitList)       #back to strings
a = map(npAry,digitList) #put into numpy array
reStrLst = map(d2s, a)
print reStrLst
for item in a:
    print item

#-----------------------------------------------------------like map func
def isMp3(s):
    if s.find(".mp3") == -1:
        return False
    else:
        return True
 
list = ["1.mp3","2.txt", "3.mp3", "4.wmv","5.mp4" ]
temp = filter(isMp3,list)
 
for item in temp:
    print item

#-------------------------------------------------------------

from string import ascii_letters, digits

def ExtractAlphanumeric(InputString):
  return "".join([ch for ch in InputString if ch in (ascii_letters + digits + " '-+.()&:,\/")])

