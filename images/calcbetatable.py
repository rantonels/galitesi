import numpy as np

q = 5
p = 1
c = 0

l = 2*c + ((p*q)%2)

x,y = np.mgrid[0:q,0:q]

r = np.exp(1j*np.pi/float(q))


summands = np.power(r, p*(x*x-y*y) + l * (x-y) )

print np.sum(summands)

import pandas as pd

df = pd.DataFrame(np.real(summands))
print df.round(2)
