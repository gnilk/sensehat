#! /bin/sh
/usr/bin/python /home/gnilk/src/sense-hat/test/mysense.py -n SensorA -t 192.168.1.12 -p 5000  &
echo "`date` - Sensor Started for `whoami`" >> /home/gnilk/sensor_status.txt

