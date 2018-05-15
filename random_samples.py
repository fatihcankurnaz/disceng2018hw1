import sys
import os
import random

node_count = int(sys.argv[1])
distance = int(sys.argv[2])

with open("satellite.txt","w+") as f:
    f.write(str(node_count)+" "+str(distance)+"\n")
    for i in range(node_count):
        temp_x = int(random.uniform(50,950))
        temp_y = int(random.uniform(50,950))
        f.write(str(temp_x)+","+str(temp_y)+"\n")
