# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 11:05:16 2017

@author: Z Engle
"""

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

  def __init__(self, name='default laminar flow', p1=10, p2=1, x1=0, x2=100, y=1, w=2, z=10, theta=1):
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
    self.vg = (1./(2.*mu))*self.pgradg*((self.channellocation**2.)\
        -(self.channelwidth*self.channellocation))

  def single_channel_vavg_gdriven(self):
    """
    what is avg velocity of water in channel
    """
    self.vavgg = (self.bedshear*self.channeldepth)/(3*mu) # [m/s]

  def single_channel_discharge(self):
    """
    what is the discharge
    """
    self.Q = self.channeldepth*self.channelwidth*self.vavgg # [m**3/s]

# Print outputs of the two flow types****************************************
  def print_output_pdriven(self):
    print self.name, 'as a saturated channel driven by pressure flow'
    print 'moves with a mean velocity of', round(self.vavgp,1), 'm/s'
    print 'which produces a shear of', round(self.taup,1), 'at a y location of'
    print self.channellocation, 'across the channel where min and max y are'
    print 'cave walls.'
  
  def print_output_gdriven(self):
    print self.name, 'as an unsaturated channel driven by gravity flow'
    print 'moves with a mean velocity of', round(self.vavgg,1), 'm/s'
    print 'which produces a bed shear of', round(self.bedshear,1), 'Pa'
    print 'and has a discharge of', round(self.Q,1), 'cubed meters per sec.'

