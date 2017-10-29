import numpy as np
import matplotlib.pyplot as plt

sz = 800
x,t = np.mgrid[0:1:1./float(sz),0:2:1./float(sz)]

psi0 = np.exp(- (x-0.5)**2/(2*0.005**2) )

#psi0hat = np.fft.fft(psi0,axis=0)

#psihat = psi0hat * 0.0

N = 50

kernel = (0.0+0j)*x
for n in range(-N,N+1):
    kernel += np.exp(1j*np.pi *(t*n*n + 2*n*x))


psi = np.fft.fft(
        np.fft.ifft(psi0,axis=0) * np.fft.ifft(kernel,axis=0),
        axis = 0
        )


psinorm2 = np.abs(psi)**2

plt.imshow(psinorm2,vmin=0,vmax=psinorm2.max()/10.,cmap='Greys',extent=[0,2,0,1])

ax = plt.gca()
ax.set_ylabel(r"$z$")
ax.set_xlabel(r"$\tau$")

#plt.show()
plt.savefig("butterfly.pgf",bbox_inches='tight')
