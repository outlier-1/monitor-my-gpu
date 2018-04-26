import serial
import glob
import sys


class ArduinoAPI(object):

    def __init__(self, baudrate):
        self.serial_port = self.get_serial_port()
        self.baudrate = baudrate

    def connect_serial_port(self):
        return serial.Serial(self.serial_port, self.baudrate)

    @staticmethod
    def get_serial_port():
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return "COM3"  # FOR NOW !
