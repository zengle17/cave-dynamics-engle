# -*- coding: utf-8 -*-
"""
Created on Mon May 01 16:23:57 2017

@author: User1
"""

import landlab
from landlab.components.overland_flow.generate_overland_flow import OverlandFlow
from landlab.components.uniform_precip.generate_uniform_precip import PrecipitationDistribution
from pylab import plot, draw, show, contour, imshow, colorbar
import numpy as np

def main():
    """
    do some stuff
    """
    
    # User-defined parameter values
    nr = 40
    nc = 40
    nnodes = nr*nc
    dx=1
    #instantiate grid
    rg = landlab.RasterModelGrid(nr, nc, dx)
    #rg.set_inactive_boundaries(False, False, True, True)
    
    nodata_val=0
    elevations  = nodata_val*np.ones( nnodes )    
    #set-up interior elevations with random numbers
    #for i in range(0, nnodes):
    #    if rg.is_interior(i):
    #        elevations[i]=random.random_sample()
    
    #set-up with prescribed elevations to test drainage area calcualtion
    helper = [7,8,9,10,13,14,15,16]
    elevations[helper]=2
    helper = [19,20,21,22]
    elevations[helper]=3        
    elevations[7]=1    
    
    # Get a 2D array version of the elevations
    elev_raster = rg.node_vector_to_raster(elevations,True)
    
    of=OverlandFlow('input_data.txt',rg,0)
    rainfall = PrecipitationDistribution()
    rainfall.initialize('input_data.txt')
    rainfall.update
    
    #for now this is in hours, so put into seconds
    storm_duration = rainfall.storm_duration*3600
    #in mm/hour, so convert to m/second
    storm_intensity = rainfall.intensity/1000/3600
    print "storm duration, seconds ", storm_duration
    print "storm duration, hours ", rainfall.storm_duration
    print "storm intensity ", storm_intensity
    
    tau = of.run_one_step(rg,elevations,storm_duration,storm_intensity)
    
    
    

if __name__ == "__main__":
    main()