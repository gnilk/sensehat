from sampler import *
from sense_hat import SenseHat


class SenseHatAdapter(SenseDataProvider) :
    def __init__(self):
        self.sense = SenseHat()
    def get_temperature(self) :
        return self.sense.get_temperature()
    def get_pressure(self) :
        return self.sense.get_pressure()
    def get_humidity(self) : 
        return self.sense.get_humidity()



if __name__ == "__main__":
    main(sys.argv[1:], SenseHatAdapter())
