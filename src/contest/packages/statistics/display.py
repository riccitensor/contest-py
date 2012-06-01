'''
Created on 21.11.2011

@author: christian.winkelmann@plista.com
'''


# do this before importing pylab or pyplot
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([1,2,3])
fig.savefig('test.png')

plt.show()

#from PIL import Image
#im = Image.open("test.png")
#im.rotate(45).show()
