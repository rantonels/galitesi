import numpy as np
from fractions import gcd
from cmath import phase

for q in range(0,10):
    for p in range(q):
        if (gcd(p,q) > 1):
            continue
        print
        for c in range(q):

            r = np.exp(1j*np.pi / q)

            beta = 0

            parity = (p*q)%2
            twodelta = parity

            for b in range(q):
                beta += r**(p*b*b + 2*b*c + twodelta * b)

            if(abs(phase(beta)) < 0.001):
                phaseNum = 999
            else:
                phaseNum = np.pi/phase(beta)

            print "%d/%d\tc=%d\t%f+%fi\t%f\t%f"%(p,q,c,beta.real,beta.imag,abs(beta)**2 / q, phaseNum)
