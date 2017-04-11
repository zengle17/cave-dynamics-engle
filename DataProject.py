# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:24:14 2017

@author: Zach
"""

from osgeo import gdal
from matplotlib import pyplot as plt
import numpy as np

# goals:
# process .jpg .tif .png and so on images of old cave maps into GIS spatial raster frame
# overlay a vector path of the cave tunnels on that map
# overlay a google earth image of that cave location over so you can see the tunnels and entrances on the surface

ds = gdal.Open('C:/Users/Zach/Documents/College/Superman Spring/comp methods in geo/cave-dynamics-engle/cavemaps/J4cavePA.jpg')
# this is an old drawing of the map from 1970... note the tilted north arrow
# cave enterance found at these google map/earth coordinates 40.861626, -77.744863






# Try typing "ds." (without the quotes) and then two tabs in iPython. Look at 
# how much extra information is packaged with this GeoTIFF!
# Try these:
ds.GetProjectionRef()
ds.GetGeoTransform()

band = ds.GetRasterBand(1) # only one band -- elevation
elevation = band.ReadAsArray() # So read it as a numpy array.

# OK -- let's plot it!
plt.imshow(elevation)
plt.colorbar()
plt.title('Berlin and surrounding Brandenburg')
plt.show()

# All right, now let's plot the proper coordinate system.
loc = ds.GetGeoTransform()
x = np.linspace(loc[0], \
                loc[0] + loc[1]*elevation.shape[1], \
                elevation.shape[1])
y = np.linspace(loc[3] + loc[5]*elevation.shape[0], \
                loc[3], \
                elevation.shape[0])

# Now plot
plt.imshow(elevation, extent=[x.min(), x.max(), y.min(), y.max()])
cbar = plt.colorbar() # Instantiate a class so I can modify its characteristics
cbar.set_label('Elevation [m]', fontsize=16, fontweight='bold')
plt.xlabel('Longitude E', fontsize=16, fontweight='bold')
plt.ylabel('Latitude N', fontsize=16, fontweight='bold')
plt.title('Berlin and surrounding Brandenburg\nSRTM 1-arcsecond data', \
           fontsize=20)
plt.tight_layout()
plt.show()