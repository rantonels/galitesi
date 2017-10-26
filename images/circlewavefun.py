import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

pi = np.pi

CIRC = 1

x = np.arange(0,CIRC+0.002,0.001)


psi0 = np.exp( - (x-CIRC*0.5)**2 / (2*(0.03**2)))


NRANGE = 50



def evolve(t,psi_in):

    z = - x

    kernel = (0.0+0j) * psi_in
    for n in range(-NRANGE, NRANGE+1):
        kernel += np.exp(1j*pi*n*n*t + 2j*pi*z*n)

#    kernel *= np.exp(-1j*z*z*t)

#    print np.sum(np.abs(kernel)**2)

#    print np.fft.fft(kernel)

    psi_t = np.fft.ifft( np.fft.fft(kernel) * np.fft.fft(psi_in) )
    return psi_t
        

def plotPsi(psi,text):

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    fig = plt.figure(figsize=(2,2))
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(-1,1)
    ax.set_ylim3d(-1,1)
#    ax.set_zlim3d(-1,1)
    ax.set_axis_off()
    ax.text2D(0,-0.09,text, 
            horizontalalignment='center',
        verticalalignment='center')
    ax.plot( np.cos(2*pi*x/CIRC), np.sin(2*pi*x/CIRC), np.abs(psi)**2, color='k', linewidth=1.5,
            )
    #circle = ax.plot( np.cos(2*pi*x/CIRC), np.sin(2*pi*x/CIRC), 0, color='k',linewidth=1)
#    plt.show()

for p,q in [
        (0,1),
        (1,5),
        (1,4),
        (2,5),
        (1,3),
        (1,2),
        (3,5),
        (2,3),
        (3,4),
        (4,5),
        (1,1),
        
        ]:
    r = float(p)/q

    if q == 1:
        rname = str(p)
    else:
        rname = r"\frac{%d}{%d}"%(p,q)

    psiTest = evolve(r+0.000001, psi0)


    plotPsi(psiTest,r"$\tau = %s$"%rname)


    plt.savefig("3dplots/%d-%d.pgf"%(p,q), bbox_inches='tight', pad_inches=0.0)

