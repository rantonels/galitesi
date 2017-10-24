import matplotlib.pyplot as plt
import numpy as np
from fractions import gcd

rse = []
qse = []
rso = []
qso = []

q = 1

for q in range(1,500):
    for p in range(q+1):
        if(gcd(p,q)>1):
            continue

        if (((p*q) % 2) == 1):
            rso.append(p/float(q))
            qso.append(q)
        else:
            rse.append(p/float(q))
            qse.append(q)

S = 30

ye = [0]*len(rse)
se = S*S* 1/np.array(qse)

yo = [0]*len(rso)
so = S*S* 1/np.array(qso)

plt.scatter(rse,ye,s=se, facecolors="k",edgecolors="k",marker='|')
plt.scatter(rso,yo,s=so, facecolors="none",edgecolors="k",marker='o')

plt.show()
