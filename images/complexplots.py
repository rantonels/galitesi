import matplotlib.pyplot as plt
import numpy as np

angstep = np.pi/8
angshift = angstep/2

def plotComplex(z,f,figsize):
    plt.rcParams['contour.negative_linestyle'] = 'solid'
    x,y = np.real(z), np.imag(z)
    arg,norm = np.angle(f),np.absolute(f)

    fig,ax = plt.subplots( figsize=figsize)
    

#    im = ax.imshow(np.log(norm), extent=[y.min(), y.max(),x.min(),x.max()], origin="lower",cmap="YlOrBr")
#    im.set_interpolation('bilinear')
    extent=[y.min(),y.max(),x.min(),x.max()]
    ax.contour(np.log(norm), np.arange(-10,10,0.25) ,extent=extent,colors='k',linewidths=0.25)
    ax.contour(np.abs(arg), np.arange(angshift,2*np.pi-angshift,angstep), vmin = 0, vmax = 2*np.pi, extent=extent, colors='k',linewidths=0.5)
 



x,y = np.mgrid[0:2:0.005 , 0:2:0.005]

z = x + 1j*y

theta = 0*z

for n in range(-50,50):
    theta += np.exp(1j*np.pi*n*n*z)

plotComplex(z,theta,(5,5))

plt.savefig("plots/theta0.pgf")
