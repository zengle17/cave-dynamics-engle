# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 10:20:25 2017

@author: User1
"""

import numpy as np
from scipy.sparse import spdiags, identity
from scipy.sparse.linalg import spsolve, isolve
from landlab import RasterModelGrid
from landlab.plot.imshow import imshow_grid_at_node
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
pco2 = .01 # [mol/L]  # ~400ppm in rainwater = 400mg/L = .4g/L * mol/44g =...
ch2o = 55.5 # [mol/L] # assume other 999,600ppm is H2O = 999g/L * mol/18g =...
r = .039 # [reactions/sec] for co2+h20 to carbonic acid
tfall = 200 # [sec] how long it takes for a raindrop to hit ground
K = 1.7E-3 # K equilibrium for H2CO3/CO2
lrain = 1 # [L] when rain falls on a 1mx1m patch of limestone for a brief dt

cacid = K * pco2 # [C carbonic acid]
macid = cacid * lrain # [mol carbonic acid in __ liters of rain]


# this rain will come down onto a pure sheet of CaCO3... so Ca ion concentration is zero
# dependent (vertical axis) will be concentration of Ca ion... telling how much dissolution happened

# Time
dt = 1 # [s]
Tend = 3000 # [s] ~30minutes of rainfall

# Grid of [Ca2+] concentration
Cstart = np.zeros(1000) # there is zero concentration of Ca ions at the start
C = Cstart.copy()
C[100] = 2 # this is the zone of the 50th grid on the 100grid array, where it is raining... the carbonic acid will react to form Ca ions
C[700] = 2
dx = 0.01 # [m]
x = np.arange(0, len(Cstart)*dx, dx)

# Parameters
D = 1E-9 # molecular diffusion coefficient [mL/molsec]

# Boundary conditions -- Dirichlet
bcl = np.array([0]) # 0 Ca ions... only pure caco3
bcr = np.array([0]) # 0 Ca ions... only pure caco3

# Put boundary conditions into the RHS "a" array
a = np.hstack(( bcl, np.zeros(len(C)-2), bcr ))

# Build tridiagonal matrix
left =   np.ones(len(C)) # If these weren't all the same value, would have
                         # to use np.roll() to arrange in proper order due
                         # to values being outside of matrix
center = -2 * np.ones(len(C))
right =   np.ones(len(C))

diagonals = (kappa * dt / dx**2) * np.vstack((left, center, right))
offsets = np.array([-1, 0, 1])

# Build it as a sparse matrix to save on memory
# Very important if you are building a big system!
A = spdiags(diagonals, offsets, len(C), len(C), format='csr')
AI = A + identity(A.shape[0])

# Solve as a forward difference
for i in range(int(np.floor(Tend/dt))):
  C = AI*C + (D * dt / dx**2)*a

# Plot
plt.plot(x, C); plt.show()