from sampler import *

class SenseHatMock(SenseDataProvider):
    def get_temperature(self):
        return float(random.randint(30,40))
    def get_pressure(self):
        return float(random.randint(500,900))
    def get_humidity(self):
        return float(random.randint(40,70))

if __name__ == "__main__":
    main(sys.argv[1:], SenseHatMock())
