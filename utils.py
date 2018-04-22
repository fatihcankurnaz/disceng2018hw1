import math



def getNumberOfHosts(satellite_name):
	with open((satellite_name),'r') as satellite_file:
		return int(satellite_file.readline().split(' ')[0])
	

def getThreshold(path_to_init_file):
	with open(path_to_init_file,'r') as init_file:
		return int(init_file.readline().split(' ')[1])


def getCoordinateOfHosts(satellite_name):
	res = []
	with open(satellite_name,'r') as satellite_file:
		satellite_file.readline()
		for line in satellite_file.readlines():
			res.append( (float(line.split(',')[0]), float(line.split(',')[1])) ) 
	return res

def getCoordinate(host_name, satellite_name):
	coordinates = getCoordinateOfHosts(satellite_name)
	host_index = int(host_name[1:])-1
	return coordinates[host_index]
	


def calc_dis(my_x, my_y, other_x, other_y):
	return math.sqrt( ( (my_x-other_x)*(my_x-other_x) ) + ( (my_y-other_y)*(my_y-other_y) ) )

def convertStrToTuple(str_tuple):
	a1 = str_tuple.split(',')[0].replace('(','')
	a2 = str_tuple.split(',')[1].replace(')','')

	return (float(a1) ,float(a2) )
	
def resolveHostName(host_name):
	number = host_name[1:]
	return "10.0.0."+number

class Wifi:
	def __init__(self, vehicle_name, satellite_name):
		
		self._vehicle_name = vehicle_name	
		self._ip = resolveHostName(vehicle_name)
		self._satellite_name = satellite_name
		

	def getConnections(self):
		connections = []
		x_ref, y_ref = getCoordinate(self._vehicle_name, self._satellite_name)

		coordinates = getCoordinateOfHosts(self._satellite_name)		
		threshold   = getThreshold(self._satellite_name)
		for i in range(len(coordinates)):
			(x,y) = coordinates[i]

			if calc_dis(x_ref, y_ref, x, y) <= threshold and ('h'+str(i+1)!=self._vehicle_name):
				connections.append( 'h'+str(i+1) )

		return connections

	def getIP(self):
		return self._ip

class GPS:
	def __init__(self, vehicle_name, path_to_file):
		self._current_vehicle_name = vehicle_name
		coordinates = getCoordinateOfHosts(path_to_file)
		self._current_vehicle_coordinate = coordinates[int(vehicle_name[1:])-1]

	def getName(self):
		return self._current_vehicle_name

	def getCoordinate(self):
		return self._current_vehicle_coordinate



	
