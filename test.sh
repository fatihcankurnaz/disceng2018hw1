#! /bin/bash
ps aux | grep -i vehicle.py | awk {'print $2'} | sudo xargs kill -9

python random_samples.py 150 100
python main.py h1 h5 example
ps aux | grep -i vehicle.py | awk {'print $2'} | sudo xargs kill -9
