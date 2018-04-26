from datetime import datetime
import time
import glob
import os
from SMS import SMSAPI
# from src.ArduinoAPI import ArduinoAPI


class Monitor:
    def __init__(self, temperature_limit, maintenance_period):
        self.temperature_limit = temperature_limit
        self.maintenance_period = maintenance_period
        self.logfile_path = None
        self.temperature_info = None
        self.hash_info = None
        self.temperature_dict = {}
        self.fan_dict = {}
        print("{} --> ".format(self.get_current_time()) + " Monitoring Operation Just Started..")

    @staticmethod
    def get_current_time(sensitivity="sec"):
        if sensitivity is "sec":
            return datetime.now().strftime('%H:%M:%S')
        elif sensitivity is "min":
            return datetime.now().strftime('%H:%M')
        elif sensitivity is "hr":
            return datetime.now().strftime('%H')
        elif sensitivity is "omin":
            return datetime.now().strftime('%M')
        else:
            return datetime.now().strftime('%H:%M:%S')

    def get_current_status(self, line_list):
        hr = line_list[len(line_list) - 5].split()[0][0:2]
        hr_condition = (hr == self.get_current_time(sensitivity="hr"))

        min = int(line_list[len(line_list) - 5].split()[0][3:5])
        min_condition = min == int(self.get_current_time("omin")) or min == int(self.get_current_time("omin")) - 1

        mining_crash_alert = "Warning! Mining Operation Might Be Stopped. " \
                                 "Control Software Couldn't Read Any Reported Hash rate"

        api = SMSAPI()
        if not hr_condition or not min_condition:
            api.send_sms(content=mining_crash_alert)
            del api
            return False
        else:
            for item in line_list[len(line_list)-100:]:
                if self.temperature_info is not None and self.hash_info is not None:
                    break
                if 't=' in item and self.temperature_info is None:
                    self.temperature_info = item

                    # Update dictionaries
                    word_list = self.temperature_info.split()
                    counter = 0
                    for word in word_list[2:]:
                        if counter % 3 == 0:
                            self.temperature_dict[word] = word_list[counter+3][2:4]
                            self.fan_dict[word] = word_list[counter+4][4:6]
                        counter += 1
                if 'Total Speed:' in item and self.hash_info is None:
                    self.hash_info = item
            del api
            return True

    def monitor_graphic_cards(self):
        cumulative = 0
        while True:
            cumulative += 1
            # Read log file and get each line into a list
            if cumulative == 60: # Every 3 hours
                self.clean_log_file()
                cumulative = 0

            file = open(self.logfile_path, 'r')
            line_list = file.readlines()

            # Get current status of graphic cards and mining process
            status = self.get_current_status(line_list)
            if status:
                # Check these informations for a dangerous circumstances
                self.check_information()
            else:
                print("{} --> ".format(self.get_current_time()) + " Couldn't Read Any Reported Hash Rate! ")

            time.sleep(self.maintenance_period)


    # def send_to_display_ard(self):
    #     api = ArduinoAPI(baudrate=9600)
    #     port = api.connect_serial_port()
    #     time.sleep(2)
    #     for key, value in self.temperature_dict.items():
    #         print(value)
    #         port.write(value.encode())
    #
    #     # Flush port for new string
    #
    #     for key, value in self.fan_dict.items():
    #         print(value)
    #         port.write(value.encode())
    #     port.close()


    def check_information(self):
        # Before check, send information to display.
        # self.send_to_display() for arduino
        # First, check for temperature
        success = True

        for key, value in self.temperature_dict.items():
            if int(value) > self.temperature_limit:
                overheat_alert = "OVERHEAT ALERT! {} has reached temperature limit." \
                                " Current GPU Temperature: {} C, Time:{}".format(key, value,
                                                                                 self.get_current_time(sensitivity="sec"))
                success = False
                x = SMSAPI()
                x.send_sms(content=overheat_alert)
                print("Heat Alert! Sms warning has just sent.")

        # Second, check for current hash rate
        if float(self.hash_info.split()[6]) < 160:
            hash_crash_alert = "Warning! Reported Hash Just Dropped. Reported Hash Should Be Around 176 MH/s. " \
                               "But it is {} MH/s Right Now.".format(self.hash_info.split()[6])
            success = False
            y = SMSAPI()
            y.send_sms(content=hash_crash_alert)

        if success is True:
            print("{} --> ".format(self.get_current_time()) + " System Status: All Systems Are Fine.")

    def clean_log_file(self):
        # This function cleans log file by deleting old log records
        for filename in glob.glob('../*_log.txt'):
            os.system("del /f " + filename)

        print("{} --> ".format(self.get_current_time()) + " Garbage Collector Is On!")
        print("{} --> ".format(self.get_current_time()) + " Old Log Files Are Deleted Successfully!")

        time.sleep(60) # wait for new log file and temperature data

        for filename in glob.glob('../*_log.txt'):
                    self.logfile_path = filename
        print("{} --> ".format(self.get_current_time()) + " New Log File Assigned Successfully.")


