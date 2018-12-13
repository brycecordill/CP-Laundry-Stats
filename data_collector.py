import requests
from bs4 import BeautifulSoup

class DataCollector:
    def __init__(self):
        self.url = "http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=aef6ddae-b1f3-4bf5-827d-618c7d3ae572"
        self.page = requests.get(self.url)
        if self.page.status_code % 100 != 200:  # Fail if not a 200 type status code
            raise ConnectionError("Unable to connect")
        self.washer_avail = 0
        self.dryer_avail = 0

    def get_machine_status(self):
        soup = BeautifulSoup(self.page.content, 'html.parser')
        available = soup.find_all(class_="MachineReadyMode") + soup.find_all(class_="MachineEndOfCycleMode")
        for type in available:
            if type.find(class_="type").get_text() == "Washer":
                self.washer_avail += 1
            elif type.find(class_="type").get_text() == "Dryer":
                self.dryer_avail += 1
            else:
                raise ValueError("Invalid machine type")

    def get_washers(self):
        return self.washer_avail

    def get_dryers(self):
        return self.dryer_avail
