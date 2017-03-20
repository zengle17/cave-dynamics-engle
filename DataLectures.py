# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 16:12:18 2017

@author: Zach
"""
# kml and shapfiles are both vector layer files
# google earth uses kml
# can go to google earth - draw vectors - and download data as kml and use
# in python

# RegEx is good for searching through huge databases

# binary is good to use to input into GIS for raster sets

import ulmo # is a hydrology library


http://matplotlib.org/users/tutorials.html
# great site for matplotlib help and tutorials

raspberry pi board = an awesome small linux computer chip $20
can stick em in a nalgene bottle or box to waterproof
then collect data in the field
Write code to interpret sensors (usually 0s and 1s)
sends it to a .csv file

inkscape can work well with python
if you are taking a bunch of well log .csv and making an:
    elevation vs latitude profile of the well logs
    color coated by rock formation type
    then in inkscape can draw lines between formations
    but if you add another log later after interpreting it,
    python saves a png that is synced w inkscape so you dont have to
    redo all the drawings
    
a 100 by 500 cell grid is 50,000 cells
that x 8 bytes/cell = 400,000 bytes = 400kb
if you keep adding to that computing then it becomes alot:
... if you started with binary, you would save alot of that space

GIS...
raster is stored as a ascii or binary
python GDAL (raster library) and OGR (vector library)
    use these because a program is reporducable... q, arc and grass are not
GDAL...
getprojectionref() gives all the dif kinds of proj like UTM

netCDF4... is another form of binary
using sattelite data
standard names are set for specific variables... reproducable and shareable
Panoply is what you install online as a NetCDF viewer    

cartopy is a cartography library for python