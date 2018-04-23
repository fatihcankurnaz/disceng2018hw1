#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import time




import SingleSwitchTopo
import utils






def simpleTest():
	"Create and test a simple network"
	topo = SingleSwitchTopo.SingleSwitchTopo('satellite.txt')
	net = Mininet(topo)
	net.start()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"
	net.pingAll()
	
	num_node = utils.getNumberOfHosts('satellite.txt')
	print 'num_node', num_node

	# network informations for each of the host kept in this list
	networks = []

	# pids of each server process that started. Kept to close them before shutting down the system
	pids = {}

	# get the created host inofrmations and puts them in the list named as networks
	for i in range(num_node):
		networks.append( net.get("h" + str(i+1)) )

	# for each host starts the server with the arguments "hostname" and acceptable "distance" 
	# as a background process
	for i in networks:
		print i.name

		# creates the string that will be feed to bash of each host
		mys = "nohup python -u vehicle.py  "+ str(i.name)+ " h1 h5 > "+ str(i.name) +'output &' 

		# gets the pid of process in order to be able to close them before shutting down the mininet
		pid = str(i.cmd(mys))
		print pid

		pids[i]=pid
	print "CREATED"


	start_node = networks[0]
	# creates the string that will be feed to bash of each host
	# mys = "nohup python -u start.py  "+ str(start_node.name)+ " h2 > "+ str(start_node.name) +'start_output &' 

	# gets the pid of process in order to be able to close them before shutting down the mininet
	# start_node_pid = str(start_node.cmd(mys))
	# print start_node_pid

	

	# starts the mininet client used to keep network open for some time
	# you can just close it and system will shutdown
	CLI(net)

	# for each host kills the started server in order to cleanly close the system
	for i in networks:
		i.cmd("kill -9 "+str(pids[i].split(" ")[1]))



	# start_node.cmd('kill -9'+str(start_node_pid.split(' ')[1]))

	# stops the mininet network
	net.stop()




# Tell mininet to print useful information
setLogLevel('info')
utils.visualize_topology("satellite.txt")
simpleTest()






print "HELLO"
