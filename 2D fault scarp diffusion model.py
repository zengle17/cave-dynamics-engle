#construct a 2D numerical model on a raster grid
#erosional degradation of an earthquake fault scarp
#evolves from downhill motion of soil as fault moves vertically
#downhill flow of soil proportional to gradient of land surface * transport coefficient

import numpy as np #for array calculations
from landlab import RasterModelGrid # to create a grid for the model
from matplotlib import pyplot as plt

mg = RasterModelGrid((25, 40), 10.0) #grid "mg" with 25 rows, 40 columns, grid spacing of 10m

z = mg.add_zeros('node', 'topographic__elevation') #call function add zeros from rastermodelgrid

plt.plot(mg.x_of_node, mg.y_of_node, '.')

len(z) #tells that there is 1000 grid nodes
        #one node/grid cell
len(mg.core_nodes) # there are 874 core nodes, 126 boundary nodes

# make plan view fault trace by equation of a line y = mx + b
fault_trace_y = 0.25*mg.x_of_node + 50

# north of the fault trace is the upthrow
upthrown_nodes = np.where(mg.y_of_node > fault_trace_y)
# numpy where function says nodes above fault trace are upthrown

z[upthrown_nodes] += 10 + 0.01*mg.x_of_node[upthrown_nodes]
# adds 10m of elevation to each upthrown node
# also adds 1cm for each node to the east to make scissor fault feel

from landlab.plot.imshow import imshow_grid_at_node
imshow_grid_at_node(mg, 'topographic__elevation')
# plots a plan view map of elevation

D = 0.01  # m2/yr transport coefficient
dt = 0.2 * mg.dx * mg.dx / D # D = c dx^2 / dt
dt
# D is diffusivity coefficient
# dt is time step size dt
# dt is 2000 years
# ASK ANDY TO EXPLAIN THIS

# say the north side and south side are open ot sediment flow
# the east and west sides are closed
mg.set_closed_boundaries_at_grid_edges(True, False, True, False)

qs = mg.add_zeros('link', 'sediment_flux')
# first argument tells landlab - want 1 value for ea grid link
# 2nd says the name for this data field

for i in range(25):
    g = mg.calc_grad_at_link(z)
    qs[mg.active_links] = -D * g[mg.active_links]
    dqsdx = mg.calc_flux_div_at_node(qs)
    dzdt = -dqsdx
    z[mg.core_nodes] += dzdt[mg.core_nodes] * dt
# creates 25 iterations representing dt 2000*25=50000 years
# raster model grid function (array g) gets gradient between adjacent nodes
    # done on links... + when uphill gradient
# calculate sed flux (qs) on active (non boundary) links
# how sed flux changes over space
    # the sed flux away will decrease elevation (- value)
# last line adds dz/dt * dt to current z of core nodes
    # tells elevation after 50000 years based on elevation rate dz/dt
imshow_grid_at_node(mg, 'topographic__elevation')