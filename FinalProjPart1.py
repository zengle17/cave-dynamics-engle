# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:11:51 2017

@author: User1
"""

import time
import numpy as np
from scipy.sparse import spdiags, identity
from scipy.sparse.linalg import spsolve, isolve
from matplotlib import pyplot as plt
from landlab import RasterModelGrid
from landlab import load_params
from landlab.plot.imshow import imshow_grid_at_node
from landlab.plot import imshow_grid
from landlab.components import OverlandFlow
import matplotlib as mpl

#construct a 2D numerical model on a raster grid
#erosional degradation of a karst sinkhole
#randomly generate rain onto the grid
#evolves from downhole vertical movement of aqueous carbonate rock and hole radially widens
#downhole vert movement and hole widening proportional water input (w carbonic acid) * transport coefficient
#should make a 3d conical shape


########## set up grid to stimulate rainstorms over the years ########################################

# set up a grid with resolution dx, elevation topography can start out as a flat slab of CaCO3
dx = 1.0
rmg = RasterModelGrid((40, 40), dx) 
#z = 160    
z = rmg.add_ones('node', 'Plan view topography')    
rmg['node']['topographic__elevation'] = z

# set Neumann boundary condition of constant gradient
rmg.set_nodata_nodes_to_fixed_gradient(z, 1) # 1 [m**3 / sec]

# set the OverlandFlow parameters for the rmg grid
of = OverlandFlow(rmg, mannings_n=0.03, steep_slopes=True)

elapsed_time = 0
model_run_time = 3000

storm_duration = 500
rainfall_mmhr = 5

# set the loop for the rainfall over the total elapsed time
while elapsed_time < model_run_time:

    of.dt = of.calc_time_step()

    if elapsed_time < (storm_duration):
        of.rainfall_intensity =  rainfall_mmhr * (0.000001)
    else:
        of.rainfall_intensity = 0

    of.overland_flow()

    elapsed_time += of.dt

# show the grid that has depth of water after rainfall events
imshow_grid(rmg, 'surface_water__depth', plot_name='Water depth across grid after rainfall',
        var_name='Water Depth', var_units='m', grid_units=('m', 'm'), cmap='Blues')


######## model the sinkhole development in plan view and cross section ##################################

mg = RasterModelGrid((40, 40), 1.0) #master grid with 40 rows, 40 columns, grid spacing of 1m

z = mg.add_zeros('node', 'Plan view topography') #call function add zeros

# make plan view sinkhole trace by equation of a circle line (x-h)**2 + (y-k)**2 = r**2
# h,k represents the coordinates of the center of the circle. r is radius
r = 5 #[m]
h = 20
k = 20
sinkhole_trace_y_upper = (((r**2) - ((mg.x_of_node - h)**2))**0.5) + k # half circle upper eq
sinkhole_trace_y_lower = (-1*(((r**2) - ((mg.x_of_node - h)**2))**0.5)) + k # half circle lower eq

# outside of the sinkhole trace, the ground is moving up relative to the sinkhole
sinkdown_nodes1 = np.where(mg.y_of_node < sinkhole_trace_y_upper) 
sinkdown_nodes2 = np.where(mg.y_of_node > sinkhole_trace_y_lower)
# numpy where function calls nodes that are above and below the two half circle lines

# want final depth of sinkhole to be 1m deep
dz = 0.5 #[m] the sinkdown nodes are spatially overlapping so 0.5m dz is really 1m of elevation decrease
z[sinkdown_nodes1] -= dz
z[sinkdown_nodes2] -= dz

# fix nodes that overlap that are falsly sinking to the N and S of sinkhole
fixed_nodes1 = np.where(mg.y_of_node > sinkhole_trace_y_upper) 
fixed_nodes2 = np.where(mg.y_of_node < sinkhole_trace_y_lower)

# reset the falsely sinking nodes to zero
z[fixed_nodes1] += dz
z[fixed_nodes2] += dz

# now you can see a solid location of the sinkhole on the grid
imshow_grid_at_node(mg, 'Plan view topography', grid_units = ['m','m'], var_name='Elevation (m)')

#### make the sinkhole more releastic (conical) and show its soluble degradation #######
# parameters
D = 0.005 # radial diffusion constant... run with different values to find most representitive value 
dt = 10 # years

qs = mg.add_zeros('link', 'sediment_flux')

t_plot = 0
dt_plot = 10 # graphically show evolution

for i in range(30): #30 iterations
    g = mg.calc_grad_at_link(z)
    qs[mg.active_links] = D * g[mg.active_links]
    dqsdx = mg.calc_flux_div_at_node(qs)
    dzdt = -dqsdx
    z[mg.core_nodes] -= dzdt[mg.core_nodes] * dt 
    #want sinkhole nodes to sink down dz amt per dt passed
    # show how sinkhole develops
    if i >= t_plot:
        t_plot += dt_plot # add dt_plot value 500 to current standing t_plot value
        print 'sinkhole after', i*dt, 'years have passed'
        elev_rast = mg.node_vector_to_raster(z)
        ycoord_rast = mg.node_vector_to_raster(mg.node_y)
        ncols = mg.number_of_node_columns
        im = plot(ycoord_rast[:, int(ncols // 2)], elev_rast[:, int(ncols // 2)])
        im
        xlabel('horizontal distance (m)')
        ylim(-2, 2)
        ylabel('vertical distance (m)')
        title('Topography cross section')
        time.sleep(0.5)

# final figure of the sinkhole after all model time has passed
figure(1)
im = imshow_grid_at_node(mg, 'Plan view topography', grid_units = ['m','m'], var_name='Elevation (m)')

#show a cross section of sinkhole
figure(2)
elev_rast = mg.node_vector_to_raster(z)
ycoord_rast = mg.node_vector_to_raster(mg.node_y)
ncols = mg.number_of_node_columns
im = plot(ycoord_rast[:, int(ncols // 2)], elev_rast[:, int(ncols // 2)])
xlabel('horizontal distance (m)')
ylim(-2, 2)
ylabel('vertical distance (m)')
title('Topography cross section')

