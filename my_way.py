#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import time

import os
# keeps the position information for each host that is gotten from init.txt
raw_locs = []

# creates a topology with single switch
class SingleSwitchTopo(Topo):
    global raw_locs
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            # for each host that is created creates a position file
            with open('h%s.txt' % (h + 1),"w+") as f:
                f.write(raw_locs[h])
                
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

# creates the network and do the necessary work like starting servers for each host
# argument 1: how much host to create as my_in
# argument 2: how much distance is accepted by the host given as my_dis
def simpleTest(my_in, my_dis):

    # network informations for each of the host kept in this list
    networks = []

    # pids of each server process that started. Kept to close them before shutting down the system
    pids = {}

    # creates the topology with the host as much as given number my_in 
    topo = SingleSwitchTopo(n=my_in)

    # by using created topology creates the mininet network
    net = Mininet(topo)

    # starts the network
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()

    # get the created host inofrmations and puts them in the list named as networks
    for i in range(my_in):
        networks.append(net.get("h" + str(i+1))   )

    # for each host starts the server with the arguments "hostname" and acceptable "distance" 
    # as a background process
    for i in networks:
        print i.name

        # creates the string that will be feed to bash of each host
        mys = "coproc python serv.py  "+ str(i.name) + "  " +str(my_dis)

        # gets the pid of process in order to be able to close them before shutting down the mininet
        pid = str(i.cmd(mys))
        print pid
        pids[i]=pid

    # starts the mininet client used to keep network open for some time
    # you can just close it and system will shutdown
    CLI(net)

    # for each host kills the started server in order to cleanly close the system
    for i in networks:
        i.cmd("kill -9 "+str(pids[i].split(" ")[1]))

    # stops the mininet network
    net.stop()

if __name__ == '__main__':


    global raw_locs
    # gets the working directory of the program
    cwd = os.getcwd()
    # gets the files in that program
    files = os.listdir(cwd)
    # removes the host position files in order to start cleanly in each start
    for file in files:
        if file != "init.txt" and file.endswith(".txt"):
            os.remove(os.path.join(cwd,file))
    flag = 0
    my_in = 1
    my_dis = 1

    # gets the system boot information like how many hosts and position of each of them
    # and creates host spesific position files
    with open('init.txt') as f:
        for line in f:
            # from first line of the file gets the host count and acceptable distance
            if flag == 0:
                my_in = int(line.split(" ")[0])
                my_dis = int(line.split(" ")[1])
                print my_in
                flag = 1
            # rest of the file is acceptable position values for each of the host and 
            # kept in raw_locs until used while creating host and their respected files
            else:
                raw_locs.append(line.split("\n")[0])
    print raw_locs




    # Tell mininet to print useful information
    setLogLevel('info')

    simpleTest(my_in,my_dis)