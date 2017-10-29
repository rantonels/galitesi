import matplotlib.pyplot as plt
import numpy as np

angstep = np.pi/8
angshift = angstep/2

def plotComplex(z,f,figsize):
    plt.rcParams['contour.negative_linestyle'] = 'solid'
    x,y = np.real(z), np.imag(z)

    arg,norm = np.angle(f),np.absolute(f)

    fig,ax = plt.subplots( figsize=figsize)
    

    plt.xticks([0,1,2])
    plt.yticks([0,1])

    ax.set_xlabel(r"$\Re\tau$")
    ax.set_ylabel(r"$\Im\tau$")

#    im = ax.imshow(np.log(norm), extent=[y.min(), y.max(),x.min(),x.max()], origin="lower",cmap="YlOrBr")
#    im.set_interpolation('bilinear')
    delta = 0.005
    extent=[x.min(),x.max()+delta,y.min(),y.max()+delta]
    ax.set_xlim(extent[0],extent[1])
    ax.set_ylim(extent[2],extent[3])
    normContour = ax.contour(x,y,np.log(norm), np.arange(-10,10,0.25) ,extent=extent,colors='k',linewidths=0.25,linestyles='dashed')
    for c in normContour.collections:
        c.set_dashes([(0, (15.0,10.0))])
    ax.contour(x,y,np.abs(arg), np.arange(angshift,2*np.pi-angshift,angstep), vmin = 0, vmax = 2*np.pi, extent=extent, colors='k',linewidths=0.5)
    ax.set_aspect('equal')
 



x,y = np.mgrid[0:2:0.005 , 0:1:0.005]

z = x + 1j*y

theta = 0*z

for n in range(-50,50):
    theta += np.exp(1j*np.pi*n*n*z)

plotComplex(z,theta,(7,7))

plt.savefig("plots/theta0.pgf",bbox_inches='tight')
