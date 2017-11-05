import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

x,sqrtt = np.mgrid[-.5:1.5:200j,0.05:1:70j]

t = sqrtt*sqrtt

theta = x*0

theta += 1

for n in range(1,50):
    theta += 2*np.exp(-np.pi * n*n * t) * np.cos(2*np.pi*n*x)


abt = np.abs(theta)
abt = np.minimum(abt,4)

fig = plt.figure(figsize=(7,7))
ax = fig.gca(projection='3d')

ax.set_zlim(0,4)

ax.plot_surface(x,t,abt,color="w",lw=0.15,shade=False,edgecolors='k')
ax.view_init(30, 40)


ax.set_ylabel(r"$t$")
ax.set_xlabel(r"$z$")
ax.set_zlabel(r"$\vartheta(z,it)")

ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

plt.savefig("heatkernel.pgf",bbox_inches='tight')
