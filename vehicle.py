import sys
import utils
import zmq
import time


class Vehicle():

	def __init__(self, node_name):
		self._node_name = node_name
		self._ip = None
		self._gps  = None
		self._wifi = None
		
		print '--- Car is create with name ' + self._node_name

	def openGPS(self, satellite_name):
		self._gps = utils.GPS(self._node_name, satellite_name)
		print '--- GPS Device is ON for '+ str(self._node_name)
		print '----- Coordinate is '+str(self.getCoordinate())+ ' according to satellite : ' + satellite_name

	def openWifi(self, satellite_name):
		self._wifi = utils.Wifi(self._node_name, satellite_name)
		print '--- WIFI Device is ON for '+ str(self._node_name)
		print '----- IP: ' + str(self.getIP())
		print '----- Avaliable Wireless Networks: ' + str(self._wifi.getConnections())

	def getCoordinate(self):
		return self._gps.getCoordinate()

	def getName(self):
		return self._node_name

	def getIP(self):
		return self._wifi.getIP()

	def getConnections(self):
		return self._wifi.getConnections()


	 
	def requestCoordinatesFromNeighbors(self):
		""" Part of Network Layer """
		neighbor_coordinates = []
		for h in self.getConnections():
			context = zmq.Context()
			socket = context.socket(zmq.REQ)
			socket.connect("tcp://"+utils.resolveHostName(h)+":12345")
			socket.send('C|')
			got_message = socket.recv()
			print got_message
			neighbor_coordinates.append( (h, utils.convertStrToTuple(got_message)) )
		print "--- Neighbor Coordinates are requested"
		return neighbor_coordinates


	def decideNextNode(self, neighbor_coordinates, d_x, d_y):
		""" Part of Network Layer """
		# Calculate neighbor distances to the destination
		neighbor_distances_to_destination = [(n,utils.calc_dis(x,y,d_x,d_y))  for (n,(x,y)) in neighbor_coordinates ]
		print "--- Distances of neighbors to the destination are calculated: "
		for ndd in neighbor_distances_to_destination:
			print "----- ", ndd		

		(my_x, my_y) = self.getCoordinate()
		my_dist = utils.calc_dis(my_x, my_y, d_x,  d_y)
		min_index = None
		min_dist  = my_dist

		# Find next node according to thier distances to the destianation node.
		for i in range(len(neighbor_distances_to_destination)):
			if  neighbor_distances_to_destination[i][1] <= min_dist:
				min_index = i
				min_dist  = neighbor_distances_to_destination[i][1]

		if min_index == None:
			return "STUCK in Greedy Mode"
		else:
			return neighbor_distances_to_destination[min_index][0]
		

	def routeMessage(self, message):
		""" Part of Network Layer """
		dest_info = message.split('|')[1].split(',')
		
		destination_node = dest_info[0]
		d_x = float(dest_info[1])
		d_y = float(dest_info[2])

		print "--- New routing is started from "+self.getName()+" to " + destination_node + " " + str((d_x,d_y))
		
		# Request neighbor coordinates
		neighbor_coordinates = self.requestCoordinatesFromNeighbors()			
		for nc in neighbor_coordinates:
			print "----- " + str(nc)
		
		# Decide next node
		next_node = self.decideNextNode(neighbor_coordinates, d_x, d_y)
		print "----- Next node is "+ next_node

		# Send message to the next node
		message = message+','+self.getName()

		
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://"+(utils.resolveHostName(next_node))+":12345")
		socket.send(message)
		socket.close()
		print "----- Message: "+message+" is sent to "+next_node

	def activateRouting(self):
	
		
		print '--- Routing Mechanism is activated'
		
		while True:
			context = zmq.Context()
			listen_socket = context.socket(zmq.REP)
			listen_socket.bind("tcp://*:12345")

			#  Wait for next request from client
			
			message = listen_socket.recv()
			
			#message = listen_socket.send('')
			print("Message Received : %s" % message)

			args = message.split('|')

			# Message type is C: request for coordinate
			if(args[0]=='C'):
				listen_socket.send(str(self.getCoordinate()))

				#  Do some 'work'
				# time.sleep(1)

			elif(args[0]=='M'):
				dest_info = args[1].split(',')
		
				destination_node = dest_info[0]
				d_x = float(dest_info[1])
				d_y = float(dest_info[2])

				(my_x, my_y) = self.getCoordinate()
				
				print my_x, my_y, d_x, d_y
				if(my_x == d_x and my_y==d_y):
					print "--- Packet reached the target."
					break

				self.routeMessage(message)				
		
				

			'''
			next = int(message[-2:-1]) + 2			
			if next > 6:
				break

			message += self.getName()+','

			print utils.resolveHostName('h'+str(next))
			print "tcp://"+utils.resolveHostName('h'+str(next))+":12345"

			send_socket = context.socket(zmq.REQ)
			send_socket.connect("tcp://"+utils.resolveHostName('h'+str(next))+":12345")
			send_socket.send(message)
			send_socket.close()
			print 'HERE'
			'''
if __name__ == '__main__':
	 
	v = Vehicle( sys.argv[1] )
	v.openGPS('satellite.txt')
	v.openWifi('satellite.txt')

	
	

	if sys.argv[2] == sys.argv[1]:
		print "This is start node of routing."
		print v.routeMessage( 'M|h6,200.,300.|')

	print v.activateRouting()

	
'''
# Create a GPS device for node_name.
# Coordinate is set by using global satellite.txt file.
gps = utils.GPS(node_name, 'satellite.txt')

print gps.getName()
print gps.getCoordinate()





context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:12345")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
'''
