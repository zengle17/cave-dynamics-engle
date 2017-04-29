# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 10:20:25 2017

@author: User1
"""

import numpy as np
import random
import time
from scipy.sparse import spdiags, identity
from scipy.sparse.linalg import spsolve, isolve
from matplotlib import pyplot as plt

# model the dissolving of calcium carbonate rock, such as in karst terrain environment
# precipitation/groundwater combines with atmosphere+soil CO2 to form dilute carbonic acid H2CO3
# reaction rate will speed up as P, T, and concentration increase... assume PT are constant STP
# reaction rate = k = -d[CO2]/dt = -d[H2O]/dt = -d[CaCO3]/dt = d[Ca]/dt = d[HCO3]/2dt ... units of C/t = mol/Lsec

# net reactants = H2O + CO2 + CaCO3    products = Ca + 2 HCO3-
# H2O is liquid (1) and CaCO3 solid (1) so equilibrium K = [Ca][HCO3-]**2 / pCO2 gas = 10**(-5.8)
# this relationship is also true, derived from above... [Ca] = ((10**(-5.8) * pCO2) / 4)**(1/3)

# can find pH of the system as well where [H]=(10**(-7.8) * [pCO2])**(1/2)  .... pH = -Log[H]

######## use the above to find out how much [Ca] is going to form to be fluxed into the system #########

# inputs
ipco2 = 0.4*44 # [mol/L] # initial ~400ppm in atmosphere = 400mg/L = .4g/L * mol/44g =...
ich2o = 999*18 # [mol/L] # assume other 999,600ppm is H2O = 999g/L * mol/18g =...
r = .039 # [rxn/sec] reaction rate for co2+h20 to carbonic acid
tfall = 200 # [sec] how long it takes for raindrop to hit limestone ground in the midwest

chco3 = r*tfall*ipco2 #[mol/L] # assume reactions to carbonic acid start happening after raindrop forms and starts falling through the co2 atmosphere
opco2 = ipco2 - (chco3 / 2) #[mol/L] # final co2 concentration in rain after some has been used up in the reaction
och2o = ich2o - (chco3 / 2) #[mol/L] # final h2o concentration in rain after some has been used up in the reaction

# Time
dt = 1 # [s]
Tend = 3000 # [s] ~30minutes of rainfall

raindt = 0.1 # [L/s] what vol of rain falls on a dx patch of limestone for a brief dt?

macid = chco3 * raindt # [total mol H acid released onto the limestone over the entire rainfall]
ph = (math.log10((10**(-7.8)) * (opco2)**(1/2)))*-1 # final estimated pH of system with limestone buffer

# this rain will come down onto a pure sheet of CaCO3... so Ca ion concentration is zero
# dependent (vertical axis) will be mol of Ca ion... telling how much dissolution happened
# for each mol of acid added to the the limestone there will be 1 mol of Ca ions created

# Grid of [Ca2+] spatial distributed concentration
Cstart = np.zeros(100) # there is zero concentration of Ca ions at the start
C = Cstart.copy()
C[random.randint(1, 99)] += macid #randomly rains here
C[random.randint(1, 99)] += macid #randomly rains here
C[random.randint(1, 99)] += macid #randomly rains here
C[random.randint(1, 99)] += macid #randomly rains here
dx = 0.001 # [m]
x = np.arange(0, len(Cstart)*dx, dx) # so grid length (x length) is 0m to length of Cstart(100zero nodes)*.001m dx interval = 0.1m long x axis

# parameters
D = 1E-9 # molecular diffusion coefficient [mL/molsec] estimated from literature

# getting the boundary conditions into the C concentration grid
bcl = np.array([0]) # 0 Ca ions... only pure caco3
bcr = np.array([0]) # 0 Ca ions... only pure caco3
a = np.hstack(( bcl, np.zeros(len(C)-2), bcr ))

# set up tridiagonal matrix
left =   np.ones(len(C))
center = -2 * np.ones(len(C))
right =   np.ones(len(C))

diagonals = (D * dt / dx**2) * np.vstack((left, center, right))
offsets = np.array([-1, 0, 1])

A = spdiags(diagonals, offsets, len(C), len(C), format='csr')
AI = A + identity(A.shape[0])


plt.ion()
fig = plt.figure()
plt.title('Acid Rain Limestone Dissolution Profile', fontsize=20, weight='bold')
plt.xlabel('Distance across limestone slab [m]', fontsize=16)
plt.ylim((0,np.max(C)*1.1))
plt.ylabel('Concentration of aqueous Ca2+ ions [mol]', fontsize=16)
fig.canvas.draw()

plt.plot(x, C, 'b-', linewidth=4) # initial spatial concentration

# Solve concentration through molecular diffision as a forward difference
t_plot = 0
dt_plot = 500 # graphically show evolution in 500sec intervals until Tend
for t in range(int(np.floor(Tend/dt))):
  C = AI*C + (D * dt / dx**2)*a
    
#  if np.array(C) > 0:       make continuous input of acid rain to simulate constant rain for 30sec rather than just a rain drop that that hits and disperses for 3000sec
#    np.nonzero(C) += macid

# graphically show the iterations and diffusion process
  if t >= t_plot:
    t_plot += dt_plot # add dt_plot value 500 to current standing t_plot value
    print 'spatial concentration after', t, 'seconds have passed'
    plt.plot(x,C,'g-',linewidth=1)
    plt.xlim((x[0],x[-1]))
    fig.canvas.draw()
    time.sleep(0.7)

print ph, 'estimated final pH of system' 
# red line showing spatial concentration after molecular diffusion has spread Ca ions out
plt.plot(x, C, 'r-', linewidth=4)
plt.plot(x, C, 'k-', linewidth=1)

plt.show()