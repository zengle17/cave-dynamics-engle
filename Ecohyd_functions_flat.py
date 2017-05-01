# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 14:02:59 2017

@author: User1
"""

from __future__ import print_function

# Authors: Sai Nudurupati & Erkan Istanbulluoglu, 21May15
# Edited: 15Jul16 - to conform to Landlab version 1.
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from landlab.plot import imshow_grid
from landlab.components import PrecipitationDistribution
from landlab.components import Radiation
from landlab.components import PotentialEvapotranspiration
from landlab.components import SoilMoisture
from landlab.components import Vegetation
from landlab.components import VegCA

GRASS = 0
SHRUB = 1
TREE = 2
BARE = 3
SHRUBSEEDLING = 4
TREESEEDLING = 5


# Function that converts text file to a dictionary
def txt_data_dict(InputFile):
    f = open(InputFile)
    data1 = {}
    for line in f:
        if line.strip() != '' and line[0] != '#':
            m, n = line.split(':')
            line = f.next()
            e = line[:].strip()
            if e[0].isdigit():
                if e.find('.') != -1:
                    data1[m.strip()] = float(line[:].strip())
                else:
                    data1[m.strip()] = int(line[:].strip())
            else:
                data1[m.strip()] = line[:].strip()
    f.close()
    return data1.copy()

# Function to compose spatially distribute PFT
def compose_veg_grid(grid, percent_bare=1, percent_grass=0,
                     percent_shrub=0, percent_tree=0):
    no_cells = grid.number_of_cells
    V = 3 * np.ones(grid.number_of_cells, dtype=int)
    shrub_point = int(percent_bare * no_cells)
    tree_point = int((percent_bare + percent_shrub) * no_cells)
    grass_point = int((1 - percent_grass) * no_cells)
    V[shrub_point:tree_point] = 1
    V[tree_point:grass_point] = 2
    V[grass_point:] = 0
    np.random.shuffle(V)
    return V


def Initialize_(data, grid, grid1):
    # Plant types are defined as following:
    # GRASS = 0; SHRUB = 1; TREE = 2; BARE = 3;
    # SHRUBSEEDLING = 4; TREESEEDLING = 5
    # Initialize random plant type field
    grid1['cell']['vegetation__plant_functional_type'] = compose_veg_grid(
                grid1, percent_bare=data['percent_bare_initial'],
                percent_grass=data['percent_grass_initial'],
                percent_shrub=data['percent_shrub_initial'],
                percent_tree=data['percent_tree_initial'])
    # Assign plant type for representative ecohydrologic simulations
    grid['cell']['vegetation__plant_functional_type'] = np.arange(0, 6)
    grid1['node']['topographic__elevation'] = (1700. *
                                               np.ones(grid1.number_of_nodes))
    grid['node']['topographic__elevation'] = (1700. *
                                              np.ones(grid.number_of_nodes))
    PD_D = PrecipitationDistribution(
                        mean_storm_duration=data['mean_storm_dry'],
                        mean_interstorm_duration=data['mean_interstorm_dry'],
                        mean_storm_depth=data['mean_storm_depth_dry'])
    PD_W = PrecipitationDistribution(
                        mean_storm_duration=data['mean_storm_wet'],
                        mean_interstorm_duration=data['mean_interstorm_wet'],
                        mean_storm_depth=data['mean_storm_depth_wet'])
                    
    return PD_D, PD_W



def Empty_arrays(n, grid, grid1):
    P = np.empty(n)    # Record precipitation
    Tb = np.empty(n)    # Record inter storm duration
    Tr = np.empty(n)    # Record storm duration
    Time = np.empty(n)  # To record time elapsed from the start of simulation
#    CumWaterStress = np.empty([n/55, grid1.number_of_cells])
    # Cum Water Stress
    P = np.empty([n/55, grid1.number_of_cells], dtype=int)
    PET_ = np.zeros([365, grid.number_of_cells])
    Rad_Factor = np.empty([365, grid.number_of_cells])
    EP30 = np.empty([365, grid.number_of_cells])
    # 30 day average PET to determine season
    PET_threshold = 0  # Initializing PET_threshold to ETThresholddown
    return (P, Tb, Tr, Time, VegType,
            PET_, Rad_Factor, EP30, PET_threshold)



def Save_(sim, Tb, Tr, P, VegType, yrs, Time_Consumed, Time):
    np.save(sim+'Tb', Tb)
    np.save(sim+'Tr', Tr)
    np.save(sim+'P', P)
    np.save(sim+'VegType', VegType)
#    np.save(sim+'CumWaterStress', CumWaterStress)
    np.save(sim+'Years', yrs)
    np.save(sim+'Time_Consumed_minutes', Time_Consumed)
    np.save(sim+'CurrentTime', Time)


def Plot_(grid, VegType, yrs, yr_step=10):
    # # Plotting
    pic = 0
    years = range(0, yrs)
    cmap = mpl.colors.ListedColormap(
                        ['green', 'red', 'black', 'white', 'red', 'black'])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    print('Plotting cellular field of Plant Functional Type')
    print('Green - Grass; Red - Shrubs; Black - Trees; White - Bare')
    # # Plot images to make gif.
    for year in range(0, yrs, yr_step):
        filename = 'Year = ' + "%05d" % year
        pic += 1
        plt.figure(pic)
        imshow_grid(grid, P[year], values_at='cell', cmap=cmap,
                    grid_units=('m', 'm'), norm=norm, limits=[0, 5],
                    allow_colorbar=False)
        plt.title(filename)
        plt.savefig(filename)
    pic += 1
    plt.figure(pic)
    plt.show