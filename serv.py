import sys
import math
import socket, optparse

# global variables to keep position info of the host
my_x = 0
my_y = 0
# global variable to keep acceptable distance get as an argument
my_dis = sys.argv[2]

# function to calculate distance with current host and another given x,y of other host
def calc_dis(other_x, other_y):
    global my_x
    global my_y
    return math.sqrt( ( (my_x-other_x)*(my_x-other_x) ) + ( (my_y-other_y)*(my_y-other_y) ) )


# gets information about position of the host from the host specisific txt which created by my_way.py
with open(sys.argv[1]+".txt","r") as f:
    line = f.readline()
    my_x = int(line.split(",")[0])
    my_y = int(line.split(",")[1])


# found from net but sets the server parameters
parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='')
parser.add_option('-p', dest='port', type='int', default=12345)
(options, args) = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# binds the server and waits
s.bind( (options.ip, options.port) )


# we are starting server as background process so we are keeping the outputs in a file specific to host
with open(sys.argv[1]+"output","w+") as f:
    f.write(sys.argv[1]+" location "+str(my_x)+" -- "+str(my_y))


# waiting for connection
while True:

    data, addr = s.recvfrom(512)
    # puts the received data to output file to check whether the connection successful or not
    with open(sys.argv[1]+"output","a") as f:
        f.write(data)
        f.write(addr)
  