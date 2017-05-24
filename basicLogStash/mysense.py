import logging, logging.handlers
import logstash_formatter
import datetime
import socket
import sys, getopt

from sense_hat import SenseHat
from time import sleep 


class Writer():
	def __init__(self, name):
		pass
	def write(self, message):
		raise NotImplementedError("Implement this!!")

class LogConsoleWriter():
	def __init__(self, name):
		ch = logging.StreamHandler()
		
		self.log = logging.getLogger(name)
		self.log.setLevel(logging.DEBUG)
		self.log.addHandler(ch)

	def write(self, message):
		self.log.info(message)	

class LogFileWriter():
	def __init__(self, name, filename):
		ch = logging.FileHandler(filename)

		self.log = logging.getLogger(name)
		self.log.setLevel(logging.DEBUG)
		self.log.addHandler(ch)

	def write(self, message):
		now = datetime.datetime.utcnow()
		data = now.strftime("%Y-%m-%dT%H:%M:%S") + " - " + message
		self.log.info(data)	


class StashSocketWriter():
	def __init__(self, name, targethost, targetport):
		self.sock = socket.create_connection((targethost, targetport))

	def write(self, message):	
		msg_bytes = message.encode('utf-8')
		self.sock.send(msg_bytes)

	


class SenseSampler():
	def __init__(self, name, freq, writer):
		self.name = name
		self.freq = float(freq)
		self.sense = SenseHat()
		self.writer = writer

	def computeHeight(self,pressure):
	    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));

	def measure(self):
		while True:
			t = self.sense.get_temperature()
			p = self.sense.get_pressure()
			h = self.sense.get_humidity()
			height = self.computeHeight(p)
		
			t = round(t, 1)
			p = round(p, 1)
			h = round(h, 1)
			height = round(height,1)
		
			now = datetime.datetime.utcnow()
			timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%0.3d" % (now.microsecond / 1000) + "Z"
		
			msg = "{"
			msg += "\"@timestamp\":\"{0}\",\"@version\":\"1\",\"@source_host\":\"{1}\",".format(timestamp, self.name)
			msg += "\"temp\":{0}, \"pressure\":{1}, \"humidity\":{2}, \"height\":{3}".format(t,p,h,height)
			msg += "}\n"
		
			self.writer.write(msg)
			
			sleep(self.freq)


def main(argv):
	name = "SensorA"
	freq = 5
	stashHost = "127.0.0.1"
	stashPort = 5000
	max_retries = 5

	log = LogFileWriter("sensor","/tmp/sensor.log")

	# print("Args:",str(sys.argv)) 

	try:
		opts, args = getopt.getopt(argv, "hf:n:t:p:", ["freq=", "name=", "target=", "port="])
	except getopt.GetoptError:
		print("mysense.py -f <freq_sec> -n <name> -t <host> -p <port>")
		sys.exit(2)
	for opt, arg in opts :
		if opt == '-h' :
			printf("mysense.py -n <name> -t <host> -p <port>")
			sys.exit(0)
		elif opt in ("-n","--name"):
			name = arg
		elif opt in ("-t","--target"):
			stashHost = arg		
		elif opt in ("-p","--port"):
			stashPort = arg
		elif opt in ("-f","--freq"):
			freq = arg

	log.write("{0} logging to logStash at {1}:{2}".format(name, stashHost, stashPort))
	try:
		retries = 0
		while retries < max_retries:
			try:
				writer = StashSocketWriter(name, stashHost, stashPort)
				sampler = SenseSampler(name, freq, writer)
				sampler.measure()
			except ConnectionResetError:
				log.write("Connection Reset, retrying... {0} of {1}".format(retries, max_retries))
				retries += 1
		log.write("Max apa retries exceeded, bailing out...")
	except:
		info = sys.exc_info()
		t = info[0]
		value = info[1]
		traceback = info[2]
		log.write("FAILED, Exception: {0}".format(info))

	log.write("Sensor stopped")

if __name__ == "__main__" :
	main(sys.argv[1:])
