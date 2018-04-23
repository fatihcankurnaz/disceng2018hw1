#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

import os


import utils



class SingleSwitchTopo(Topo):
	"""Single switch topology to create Vehicular Ad-Hoc Networks (VANET).

	This class should be called in the the main function to create a Mininet topology
	to simulate VANETs.	


	Attributes
	----------
	attr1 : str
		Description of `attr1`.
	attr2 : :obj:`int`, optional
		Description of `attr2`.

	"""

	def __init__(self, path_to_init_file, **opts):
		"""Create topology, add hosts and create host information files. """
		
		super(SingleSwitchTopo, self).__init__(**opts)
		

		# Create the topology
		# Add single switch
		switch = self.addSwitch('s1')

		# Add hosts
		
		number_of_hosts = utils.getNumberOfHosts(path_to_init_file)

		coordinate_of_hosts = utils.getCoordinateOfHosts(path_to_init_file)

		for h in range(number_of_hosts):
			# for each host that is created creates a position file
			with open('h%s.txt' % (h + 1),"w+") as f:
				f.write(str(coordinate_of_hosts[h]))
				host = self.addHost('h%s' % (h + 1))
				self.addLink(host, switch)
		
	
