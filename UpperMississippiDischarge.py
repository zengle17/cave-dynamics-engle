# Using Ulmo for all of the gauges along the Mississippi

"""
url = 'http://hydroportal.cuahsi.org/nwisdv/cuahsi_1_1.asmx?WSDL'

csites = ulmo.cuahsi.wof.get_sites(url)

Mississippi_Gauges = []

for k in csites:
  v = csites[k]
  if 'MISSISSIPPI R' in v['name']:
     Mississippi_Gauges.append(k)
     
for k in Mississippi_Gauges:
  ulmo.cuahsi.wof.get_values(wsdl_url=url, site_code=k, variable_code
"""

import ulmo #hydrology library
import pandas as pd
import numpy as np

UMR_HUC = '07' #hydrologic unit code for a major US watershed (upper missisp)
Q_daily_code = '00060:00003' # this is the code for USGS gauge data

usgs_gauges = ulmo.usgs.nwis.get_sites(huc=UMR_HUC)

Mississippi_Gauges = []

for k in usgs_gauges:
  v = usgs_gauges[k]
  if 'MISSISSIPPI R' in v['name']:
     Mississippi_Gauges.append(k)

for gauge in Mississippi_Gauges:
  print gauge, usgs_gauges[gauge]['name']

Q_mean = []
lat = []
lon = []
HUC = [] #hydrologic unit code
ID = []
LenRecord = []
for gauge in Mississippi_Gauges:
  try: # use try when there is an exception being thrown
    tmp = ulmo.usgs.nwis.get_site_data(gauge, service="daily", period="all")
    tmp2 = tmp['00060:00003'] #tmp creates a temporary file
    tmp3 = tmp2['values']
    tmplist = []
    for item in tmp3:
      tmplist.append(float(item['value']))
    tmplist = np.array(tmplist)
    Q_mean.append(np.mean(tmplist[tmplist>0]) * 0.0283168466) # ft3/s to m3/s
    # takes all Q that are greater than 0... get rid of faulty data
    lat.append(tmp2['site']['location']['latitude'])
    lon.append(tmp2['site']['location']['longitude'])
    HUC.append(tmp2['site']['huc'])
    ID.append(gauge)
    LenRecord.append(len(tmplist[tmplist>0]))
  except: # except pass takes any error and just moves on past it
          # disregards any data 
    pass
    """
    Q_mean.append(np.nan)
    lat.append(np.nan)
    lon.append(np.nan)
    HUC.append(np.nan)
    ID.append(gauge)
    """

out = np.array([ID, lat, lon, HUC, Q_mean, LenRecord]).transpose()
# Add drainage area in km2 by hand, from
# https://water.usgs.gov/GIS/huc_name.html
np.savetxt('UpperMississippiQ.csv', out, delimiter=',', fmt='%s')


#%%

SITE_ID = '05211000'
Q_daily_code = '00060:00003'

usgs_gauges = ulmo.usgs.nwis.get_sites(sites=SITE_ID)[SITE_ID]

daily_request = ulmo.usgs.nwis.get_sites_data(SITE_ID, service="daily", period = "all")
daily_discharge = daily_request[Q_daily_code]['values']
Q = []
t = []
for row in daily discharge:
    Q.append( float(row['value']))
    t.append( dt.strptime(row['datetime'], '%Y-%m-%dT%H:%M:%S'))
    
Q = np.array(Q)
t = np.array(t)

nodata_value = float(daily_request.values()[0]['variable']['no_data_value'])

t = t[Q != nodata_value]
Q = Q[Q != nodata_value]

plt.ion()
plt.figure(figsize=(18,8))
plt.plot(t, Q, 'k-', linewidth=2)
plt.title(usgs_gauge['name'], fontsize=20)
plt.xlabel('Date', fontsize = 20)
plt.tight_layout()