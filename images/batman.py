import matplotlib as mpl
mpl.use('pgf')
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": [],
    "font.sans-serif": ["DejaVu Sans"],
    "pgf.preamble": [
         r"\usepackage{xfrac}"
         ]
    }
mpl.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np

t = np.arange(0,2,0.002)

B = t*0j

for n in range(1,100):
    B += 2/(1j*np.pi) * np.exp(1j*np.pi*t*n*n)/(n*n)


pe_ontop = [path_effects.Stroke(linewidth=10, foreground='white'),
                       path_effects.Normal()]


fig,ax = plt.subplots(figsize=(6,4))

ax.plot(t,B.real,'k',lw=0.5)
ax.plot(t,B.imag,'k', lw=0.5, path_effects = pe_ontop)


from fractions import gcd

for q in range(6):
    for p in range(1,q):
        if(gcd(p,q) > 1):
            continue
        
        r= float(p)/float(q)
        BrI = np.interp(r,t,B).imag
        BrR = np.interp(r,t,B).real
        BrM = max(BrR,BrI)
        Brm = min(BrR,BrI)

        if (p,q) in [(2,3),(3,4),(4,5)]:
            Brm -= 0.1

        txt = ax.text(r,Brm-0.4,r"$\sfrac{%d}{%d}$"%(p,q) , ha='center')
#        txt.set_path_effects(pe_ontop)

        plt.plot([r,r],[Brm-0.05,Brm-0.30],'k--',lw=0.5)

ax.set_xlim([0,2])


#plt.show()
plt.savefig("batman.pgf",bbox_inches='tight')
