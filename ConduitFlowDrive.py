# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 11:07:49 2017

@author: Z Engle
"""

import ConduitFlow as cf

defaultchannel = cf.conduit_channel_dynamics() #default values

# custom values
karstchannel = cf.conduit_channel_dynamics(name='Insane Laminar Linear Karst Conduit', \
        p1=1000, p2=10, x1=0, x2=2000, y=0, w=10, z=0.5, theta=0.5)


print ""
defaultchannel.print_output_pdriven()
print ""
defaultchannel.print_output_gdriven()
print ""
print ""
karstchannel.print_output_pdriven()
print ""
karstchannel.print_output_gdriven()
print ""
