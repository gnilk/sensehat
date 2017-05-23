Basic sensoring stuff.
By default it logs data to a remote host following LogStash JSON format.
Can be combined with ELK as the remote receiever of log data

Contents:
	mysense.py, python logging script
	start_sensor.sh, wrapper to start it
	sensor, shell script for init.d (boot up start)


In order to get boot running do:
1) copy 'sensor' to /etc/init.d
2) modify path in sensor script and also the path in 'start_sensor'
3) run 'update-rc.d sensor default'

Dependencies:
Python3
SenseHat stuff

Note: 
Upon reboot the code will retry 5 times before bailing. It can be that the network will reset.
Code has been tested with WLAN and never with a LAN connection.
