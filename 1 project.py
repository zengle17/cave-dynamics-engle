# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:14:35 2017

@author: Z Engle
"""
# DUE MARCH 1st
#%%
project ideas

karst and lava tube modeling and mapping GIS sediments/aquifers
water/fluid and ionic movement through these environments 
growth of speleothems and epigenetic deposits (Pb Zn) induced by magmatic
    movement up after a fault
aquifer analyses and where to drill
lava tube growth, mineral crystalization and volcanology
hazards with these environments (landslides, sinkholes, hazardous minerals)
resource management (water and minerals and ores) in these env
how mining consequences/harmful chems can travel through these envionments
    + through mining shafts, tunnels
    environmental travel of hazardous tailings, mercury used in gold mining
    mercury in gw from gold mining... hydraulic mine assessment
    remediation for mercury methylation
understand origin and dynamics of water - springs, streams
how they are affected by warming climate and gw pumping and ET interaction
what if a river erroded down to a karst layer and dumped into the cave?

# Karst forms from the dissolution of soluble rocks 
# such as limestone, dolomite, and gypsum.
# Acidic water breaks these down near cracks or bedding planes
# As they break down, they become wider allowing more water flow
# Allowing for exponentially faster formation

# h2o + co2 -> h2co3 carbonic acid
# caco3 + h2co3 -> Ca + 2hco3-

# in rare cases (lechuguilla cave New Mex)
# oxygen rich surface waters seep into deep anoxic Karst systems
# react with sulfides (pyrite or H2S) to form sulfuric acid that diss CaCO3
# it then goes to precipitate gypsum spleothems 
H2S	+	2 O2	→	H2SO4	
    # (sulfide oxidation)
H2SO4	+	2 H2O	→	SO2−4	+	2 H3O+	
    # (sulfuric acid dissociation)
CaCO3	+	2 H3O+	→	Ca2+	+	H2CO3	+	2 H2O	
    # (calcium carbonate dissolution)
CaCO3	+	H2SO4	→	CaSO4	+	H2CO3	
    # (global reaction leading to calcium sulfate)
CaSO4	+	2 H2O	→	CaSO4 · 2 H2O	
    # (hydration and gypsum formation)

What affects carbonate precipitation/dissolution... temp, pH, Pressure

# Rare, chemolithoautotrophic bacteria are believed to occur in the cave. 
# These bacteria feed on the sulfur, iron, 
# and manganese minerals and may assist in enlarging the cave and determining 
# the shapes of unusual speleothems. 
# the majority are sulfur-oxidizing bacteria that utilize primarily atmospheric 
# oxygen (derived from sunlight-driven photosynthesis) as an electron acceptor.
#%%

gdal and ogr - can import as python modules do all GIS functions 
    does all the basic things
    
how to set up karst grid - start out pretending cave system is 2D
land

start out with some incipient karst conduit - focus on erosion
proportional to discharge 
Have it in 2d plan view... rain fall goes down into area
#%%
import numpy as np # Numerical library
from matplotlib import pyplot as plt # Plotting library
import time

# Global constants
g = 9.8 # [m/s**2]
rho = 1000 # [kg/m**3] density of water at 293K
mu = 0.001 # [kg/m*s] dynamic viscosity of water at 293K

def rain_fall():

# *********************************written as module
# When channel full and P driven flow ***************************************
def single_channel_v_pdriven(p1, p2, x1, x2, y, w):
    """
    what is the velocity as water travels down first crack or bed
    plane. Input channel width (w) and location in channel (y).
    pressure gradient (dp/dx) decreases from x start to x end
    """
    return (1./(2.*mu))*((p2-p1)/(x2-x1))*((y**2.)-(w*y)) # [m/s]
    
def single_channel_vavg_pdriven(p1, p2, x1, x2, w):
    """
    what is the avg velocity in a circular laminar channel. max v / 2
    max v is at center of channel (w/2)
    """
    return ((1./(2.*mu))*((p2-p1)/(x2-x1))*(((w/2.)**2.)-(w*(w/2.))))/2. # [m/s]

def single_channel_tau_pdriven(p1, p2, x1, x2, y, w):
    """
    what is the shear stress on the cave wall edges or fluid solid contact
    (y = 0) or in center
    """
    return ((p2-p1)/(x2-x1))*(y-(w/2.)) # [Pa]

# When channel not full and g driven flow ***********************************
def single_channel_Pgradient_gdriven(theta):
    """
    what is P gradient driving flow when not full.
    depends on g driving the dense fluid down a slope (theta)
    """
    return rho*g*np.sin(theta * (np.pi/180.)) # [Pa/m]

#%%
# *****************************written as class

import numpy as np # Numerical library
from matplotlib import pyplot as plt # Plotting library
import time

# Global constants
g = 9.8 # [m/s**2]
rho = 1000 # [kg/m**3] density of water at 293K
mu = 0.001 # [kg/m*s] dynamic viscosity of water at 293K
    
class conduit_channel_dynamics(object):
  """
  single channel circular pipe flow
  """

  def __init__(self, name='default flow', p1=10, p2=1, x1=0, x2=100, y=1, w=2, z=10, theta=1):
    """
    Set up
    """
    # make these into class variables.
    self.name = name
    self.pressurestart = p1
    self.pressureend = p2
    self.xstart = x1
    self.xend = x2
    self.channellocation = y
    self.channelwidth = w
    self.channeldepth = z
    self.slopedegree = theta
    # And automatically run the first two functions
    # with a class, we can run functions that lie below the current point
    self.single_channel_v_pdriven()
    self.single_channel_vavg_pdriven()
    self.single_channel_shear_pdriven()
    self.single_channel_Pgradient_gdriven()
    self.single_channel_bedshearstress()
    self.single_channel_v_gdriven()
    self.single_channel_vavg_gdriven()
    self.single_channel_discharge()

# When channel full and P driven flow map view of channel flow ****************
  def single_channel_v_pdriven(self):
    """
    what is the velocity as water travels down first crack or bed
    plane. Input channel width (w) and location in channel (y).
    pressure gradient (dp/dx) decreases from x start to x end
    """
    self.vp = (1./(2.*mu))*((self.pressureend-self.pressurestart) \ 
        /(self.xend-self.xstart))*((self.channellocation**2.) \ 
        -(self.channelwidth*self.channellocation)) # [m/s]
    
  def single_channel_vavg_pdriven(self):
    """
    what is the avg velocity in a circular laminar channel. max v / 2
    max v is at center of channel (w/2)
    """
    self.vavgp = ((1./(2.*mu))*((self.pressureend-self.pressurestart) \ 
        /(self.xend-self.xstart))*(((self.channelwidth/2.)**2.) \ 
        -(self.channelwidth*(self.channelwidth/2.))))/2. # [m/s]

  def single_channel_shear_pdriven(self):
    """
    what is the shear stress on the cave wall edges or fluid solid contact
    (y = 0) or in center
    """
    self.taup = ((self.pressureend-self.pressurestart) \ 
        /(self.xend-self.xstart))*(self.channellocation-(self.channelwidth/2.))
        # [Pa]

# When channel not full and g driven flow cross sectionl view *****************
  def single_channel_bedshearstress(self):
    """
    what is tau naught? bed shear stress rho g h S
    the force balance on the bed
    """
    self.bedshear = rho*g*self.channeldepth*np.tan(self.slopedegree*(np.pi/180.))
    #converts degree slope to radians
    # [N/m**2] or [Pa]
  
  def single_channel_Pgradient_gdriven(self):
    """
    what is P gradient driving flow when not full.
    depends on g driving the dense fluid down a slope (theta)
    """
    self.pgradg = rho*g*np.sin(self.slopedegree * (np.pi/180.)) # [Pa/m]
  
  def single_channel_v_gdriven(self):
    """
    what is v of surface flow at a y location when driven by g on a slope
    """
    # **** check that i can do self.pgradg
    # *** does \ symbol allow me to space down the equation?
    self.vg = (1./(2.*mu))*self.pgradg*((self.channellocation**2.) \ 
        -(self.channelwidth*self.channellocation)

  def single_channel_vavg_gdriven(self):
    """
    what is the avg velocity of the flow in a river like channel
    or non-full conduit
    """
    self.vavgg = (self.bedshear*self.channeldepth)/(3*mu) # [m/s]

  def single_channel_discharge(self):
    """
    what is the discharge
    """
    self.Q = self.channeldepth*self.channelwidth*self.vavgg # [m**3/s]

# Print outputs of the two flow types****************************************
  def print_output_pdriven(self):
    print self.name, 'is a saturated channel driven by pressure flow'
    print 'that moves with a mean velocity of', round(self.vavgp,1), 'm/s'
    print 'which produces a shear of', round(self.taup,1), 'at a y location of'
    print self.channellocation, 'across the channel where min and max y are'
    print 'cave walls.'
  
  def print_output_gdriven(self):
    print self.name, 'is an unsaturated channel driven by gravity flow'
    print 'that moves with a mean velocity of', round(self.avgg,1), 'm/s'
    print 'which produces a bed shear of', round(self.bedshear,1), 'Pa'
    print 'and has a discharge of', round(self.Q,1), 'cubed meters per sec.'


