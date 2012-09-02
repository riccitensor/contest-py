from scipy.stats.distributions import random
import numpy as np
from pandas import *
import matplotlib.pyplot as plt


randn = np.random.randn
#s = Series(data, index=index)
#s = Series(randn(5), index=['a', 'b', 'c', 'd', 'e'] )

mydata = { 'h:1' : 3, 'h:2' : 5, 'h:3' : 10, 'h:4' : 14, 'h:5' : 10, 'h:6' : 8, 'h:7' : 6, 'h:8' : 3 }
s1 = Series(mydata)
mydata = { 'h:1' : 5, 'h:2' : 6, 'h:3' : 11, 'h:4' : 12, 'h:5' : 11, 'h:6' : 7, 'h:7' : 2, 'h:8' : 1 }
s2 = Series(mydata)




#ts = Series(randn(1000), index=date_range('1/1/2000', periods=1000))
#ts = ts.cumsum()

#s.plot()
#plt.figure(); df.plot(); plt.legend(loc='best')
#plt.figure(); ts.plot(style='k--', label='Series'); plt.legend()


#plt.show()
#ts = Series(randn(1000), index=DateRange('1/1/2000', periods=1000))

#ts = ts.cumsum()
#df = DataFrame(randn(1000, 2), index=ts.index, columns=['A', 'B'])

x = random(10)
print x
d = {'one' : s1,
     'two' : s2}
df = DataFrame(d)
df.plot()

plt.show()