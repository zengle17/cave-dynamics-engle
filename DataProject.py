# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:24:14 2017

@author: Zach
"""

from osgeo import gdal, osr, ogr
from matplotlib import pyplot as plt
import numpy as np
import sys

# goals:
# process .jpg .tif .png and so on images of old cave maps into GIS spatial raster frame
# set up a .wkt file associated with the geotiff to be able to put vector polygons on the map

# to not print gdal error messages
gdal.UseExceptions()

# laptop source_image = 'C:/Users/Zach/Documents/College/Superman Spring/comp methods in geo/cave-dynamics-engle/cavemaps/J4cavePA.jpg'
source_image = 'E:/College/Superman Spring/comp methods in geo/cave-dynamics-engle/cavemaps/J4cavePA.jpg'
# laptop destination_image = 'C:/Users/Zach/Documents/College/Superman Spring/comp methods in geo/cave-dynamics-engle/geocavemaps/geoJ4cavePA.tif'
destination_image = 'E:/College/Superman Spring/comp methods in geo/cave-dynamics-engle/geocavemaps/geoJ4cavePA.tif'

# http://nodivisions.com/excursions/j4/j4_cave_map_new.jpg
# 10044 x 4944 resolution... 10044 pixels wide, 4944 pixels tall... pixel coords found w GIMP
# jpg compress image blocks (this image changed 2x2pixel to a 1x1 pixel block during compression)
# tif files do not compress at all
# this J4 Cave image is a scanned old drawing of the map from 1970... note the tilted north arrow
# cave enterance found at these google map/earth coordinates 40.861678, -77.744858 (pixel coord 7056 x 549)
# upper left corner of jpg image (pixel 0x0) is roughly at 40.860020, -77.747383 estimated w google earth
# bottom right corner of jpg image (pixel coord 10044 x 4944)

# open source dataset
src_ds = gdal.Open(source_image)
format = "GTiff"
driver = gdal.GetDriverByName(format)

# open destination dataset
dst_ds = driver.CreateCopy(destination_image, src_ds, 0)

# Specify raster location through geotransform array
# (uperleftx, scalex, skewx, uperlefty, skewy, scaley)
# Scale = size of one pixel in units of raster projection
# based on the scale, I assume a pixel is 1x1 meter
gt = [-7774738, 1, 0, 4086002, 0, -1]

# Set location georeference (give pixel coords a geospatial coord)
dst_ds.SetGeoTransform(gt)

# Get raster projection epsg code http://spatialreference.org/ref/epsg/?search=pennsylvania&srtext=Search
epsg = 3651 # epsg 3651 code refers to NAD83(NSRS2007) / Pennsylvania South 
srs = osr.SpatialReference()
srs.ImportFromEPSG(epsg)
dest_wkt = srs.ExportToWkt()

# Set projection for the output georeferenced tif (destination dataset)
dst_ds.SetProjection(dest_wkt)

# Close files into designated folders
dst_ds = None
src_ds = None
# by this point there should now be a created geotiff file in the destination folder

# call the jpg that was georeferenced into a geotiff
geo_image = 'E:/College/Superman Spring/comp methods in geo/cave-dynamics-engle/geocavemaps/geoJ4cavePA.tif'
dsgeo = gdal.Open(geo_image)

# see how there is now geospatial information associated to this geotiff
print dsgeo.ReadAsArray()
print dsgeo.GetMetadata()
print dsgeo.GetProjectionRef()
print dsgeo.GetGeoTransform()

# set up geotiff with a wkt file that can be used as a vector to polygonize the spatial map
data = dsgeo.ReadAsArray()
gt = dsgeo.GetGeoTransform()
proj = dsgeo.GetProjectionRef()

inproj = osr.SpatialReference()
inproj.ImportFromWkt(proj)

print(inproj)