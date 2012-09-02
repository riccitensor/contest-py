from matplotlib.pyplot import hist

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#fig = plt.figure()

#ax = fig.add_subplot(111)
#ax.plot([1,2,3])
#fig.savefig('test.png')



import numpy as np
from pandas import *


randn = np.random.randn
x = randn(10000)
hist(x, 100)

plt.show()