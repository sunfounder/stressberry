import time
import glob

class DS18B20:
    
    BASE_DIR = '/sys/bus/w1/devices/'

    def __init__(self, id=None):
        if id is None:
            self.id = self.get_sensor_ids()[0]
        else:
            self.id = id
        self.device_file = self.BASE_DIR + self.id + '/w1_slave'
    
    def get_sensor_ids(self):
        device_folders = glob.glob(self.BASE_DIR + '28*')
        if len(device_folders) == 0:
            raise Exception('No DS18B20 sensor found')
        sensor_ids = [folder.split('/')[-1] for folder in device_folders]
        return sensor_ids

    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            return f.readlines()

    def get_temperature(self, unit='C'):
        lines = self.read_temp_raw()
        print(lines)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            if unit == 'C':
                return temp_c
            elif unit == 'F':
                return temp_f

    @property
    def temperature(self):
        return self.get_temperature()


def test():
    sensor = DS18B20()
    import time
    while True:
        print(sensor.temperature)
        time.sleep(1)

if __name__ == '__main__':
    test()
