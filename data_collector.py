import requests
from bs4 import BeautifulSoup
import os.path
import datetime

class DataCollector:
    def __init__(self):
        self.url = "http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=aef6ddae-b1f3-4bf5-827d-618c7d3ae572"
        self.page = requests.get(self.url)
        if self.page.status_code // 100 != 2:  # Fail if not a 200 type status code
            raise ConnectionError("Unable to connect")
        
        self.washer_avail = 0
        self.dryer_avail = 0
        self.washer_file = "data/washer_data"
        self.dryer_file = "data/dryer_data"

    def run_collector(self):
        self.get_machine_status()
        self.write_data()

    def get_machine_status(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        available = soup.find_all(class_="MachineReadyMode") + soup.find_all(class_="MachineEndOfCycleMode")

        for machine in available:
            if machine.find(class_="type").get_text() == "Washer":
                self.washer_avail += 1
            elif machine.find(class_="type").get_text() == "Dryer":
                self.dryer_avail += 1
            else:
                raise ValueError("Invalid machine machine")

    def write_data(self):
        washer_data = self.format_data(self.washer_file, self.washer_avail)
        dryer_data = self.format_data(self.dryer_file, self.dryer_avail)

        with open(self.washer_file, 'w') as wf:
            wf.writelines(washer_data)
        with open(self.dryer_file, 'w') as df:
            df.writelines(dryer_data)

    def format_data(self, filename, available_count):
        date = datetime.datetime.today()
        day = date.strftime("%a")  # Abbreviated day of week
        hour = date.strftime("%H")  # Hour in 24H
        formatted_str = "{} {} {}\n".format(day, hour, available_count)

        if os.path.exists(filename):
            with open(filename, 'r') as fn:
                file_data = fn.readlines()  # Read lines into a list

            line_num = 0
            while file_data[line_num] != formatted_str[:7] and line_num < len(file_data) - 1:
                line_num += 1  # Iterate through lines to find match

            if line_num == len(file_data):  # If line doesn't yet exist
                file_data.append(formatted_str)
            else:  # If Line already exists
                file_data[line_num] = file_data[line_num].replace("\n", " {}\n".format(available_count))

        else:  # If the file doesn't yet exist
            file_data = formatted_str

        return file_data

    def get_washers(self):
        return self.washer_avail

    def get_dryers(self):
        return self.dryer_avail
