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
#from __future__ import print_function
from landlab import RasterModelGrid as rmg
from landlab import load_params
from Ecohyd_functions_flat import (Initialize_, Empty_arrays,
                                   Save_, Plot_)
from landlab.plot.imshow import imshow_grid_at_node
from landlab.plot import imshow_grid
import matplotlib as mpl

#construct a 2D numerical model on a raster grid
#erosional degradation of a karst sinkhole
#randomly generate rain onto the grid
#evolves from downhole vertical movement of aqueous carbonate rock and hole radially widens
#downhole vert movement and hole widening proportional water input (w carbonic acid) * transport coefficient
#should make a 3d conical shape


##### set up grid to make rain randomly fall ########################################
grid1 = rmg((100, 100), spacing=(5., 5.)) #master grid
grid = rmg((5, 4), spacing=(5., 5.)) 

#load storm parameters
InputFile = 'FinalProjStormParameters.txt'
data = load_params(InputFile)

PD_D, PD_W = Initialize_(
            data, grid, grid1)


n_years = 600      # Approx number of years for model to run
# Calculate approximate number of storms per year
fraction_wet = (data['doy__end_of_monsoon']-data['doy__start_of_monsoon'])/365.
fraction_dry = 1 - fraction_wet
no_of_storms_wet = (8760 * (fraction_wet)/(data['mean_interstorm_wet'] +
                    data['mean_storm_wet']))
no_of_storms_dry = (8760 * (fraction_dry)/(data['mean_interstorm_dry'] +
                    data['mean_storm_dry']))
n = int(n_years * (no_of_storms_wet + no_of_storms_dry)) # total number of storms through years of model

                
# # Represent current time in years
current_time = 0            # Start from first day of Jan

# Keep track of run time for simulation - optional
Start_time = time.clock()     # Recording time taken for simulation

# declaring few variables that will be used in the storm loop
time_check = 0.     # Buffer to store current_time at previous storm
yrs = 0             # Keep track of number of years passed
WS = 0.             # Buffer for Water Stress
Tg = 270        # Growing season in days


# # Run storm Loop
for i in range(0, n):
    # Update objects

    # Calculate Day of Year (DOY)
    Julian = np.int(np.floor((current_time - np.floor(current_time)) * 365.))

    # Generate seasonal storms
    # for Dry season
    if Julian < data['doy__start_of_monsoon'] or Julian > data[
                        'doy__end_of_monsoon']:
        PD_D.update()
        P[i] = PD_D.storm_depth
        Tr[i] = PD_D.storm_duration
        Tb[i] = PD_D.interstorm_duration
    # Wet Season - Jul to Sep - NA Monsoon
    else:
        PD_W.update()
        P[i] = PD_W.storm_depth
        Tr[i] = PD_W.storm_duration
        Tb[i] = PD_W.interstorm_duration

    # Assign spatial rainfall data
    grid['cell']['rainfall__daily_depth'] = P[i] * np.ones(grid.number_of_cells)

    # Record time (optional)
    Time[i] = current_time

    # Update spatial PFTs with Cellular Automata rules
    if (current_time - time_check) >= 1.:
        if yrs % 100 == 0:
            print('Elapsed time = {time} years'.format(time=yrs))
        yrs += 1

Plot_(grid1, P, yrs, yr_step=100)



###################### construct sinkhole evolution in the spots that it rains ###################


mg = rmg((40, 40), 1.0) #master grid with 40 rows, 40 columns, grid spacing of 1m

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
dt_plot = 2.5 # graphically show evolution in 25year intervals until end

for i in range(25): #25 iterationsxdt of 10 is 250years
    g = mg.calc_grad_at_link(z)
    qs[mg.active_links] = D * g[mg.active_links]
    dqsdx = mg.calc_flux_div_at_node(qs)
    dzdt = -dqsdx
    z[mg.core_nodes] -= dzdt[mg.core_nodes] * dt 
    #want sinkhole nodes to sink down dz amt per dt passed
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

figure(1)
im = imshow_grid_at_node(mg, 'Plan view topography', grid_units = ['m','m'], var_name='Elevation (m)')

figure(2)
elev_rast = mg.node_vector_to_raster(z)
ycoord_rast = mg.node_vector_to_raster(mg.node_y)
ncols = mg.number_of_node_columns
im = plot(ycoord_rast[:, int(ncols // 2)], elev_rast[:, int(ncols // 2)])
xlabel('horizontal distance (m)')
ylim(-2, 2)
ylabel('vertical distance (m)')
title('Topography cross section')



