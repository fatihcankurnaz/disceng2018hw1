import sys
import utils
import zmq
import time

from vehicle import Vehicle

start_node_name = sys.argv[1]
next_node_name  = sys.argv[2]
'''
context = zmq.Context()

#  Socket to talk to server
print("The algorithm starts from node " + start_node_name +' to '+next_node_name )
socket = context.socket(zmq.REQ)
socket.connect("tcp://"+ utils.resolveHostName(next_node_name) +":12345")



socket.send(next_node_name +'|'+start_node_name+',')
'''
print 'END'
v = Vehicle( 'h2' )
print 'END'
v.openGPS('satellite.txt')
print 'END'
v.openWifi('satellite.txt')
print 'END'

v.startRouting()
print 'END'
