import os
import datetime


class CompileData:
    """
    This file compiles the data collected from data_collector.py in a more easily readable format.
    The output is then written to self.out_file for viewing by the user.
    """

    def __init__(self, out_file):
        self.data_dir = "data/"
        self.washer_file = self.data_dir + "washer_data"
        self.dryer_file = self.data_dir + "dryer_data"
        self.out_file = out_file

    def run_compiler(self):
        """Runs entire class"""
        self.compile_data()

    def format_data(self):
        """Formats the data given from self.read_file() and sends it off to be written to self.out_file"""
        day_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # List of days (for ordering)
        data_dict = self.read_file()

        date = datetime.datetime.today()
        current_date = date.strftime("%b %d")  # Abbreviated month
        current_time = date.strftime("%H:%M")  # Time
        formatted_time = "Last updated on {} at {}".format(current_date, current_time)

        out_data = "This file displays the average amount of washers and dryers available at a given day and time" \
                   "\n\n" + formatted_time + "\n" \
                   "\n\nDay\tTime \tWashers\tDryers\n"  # File header for usability

        for day in day_list:
            out_data += "\n" + day  # Add day sub-header
            for time in data_dict[day].keys():
                out_data += "\n   \t{}:00  \t{:.2}  \t{:.2}" \
                    .format(time.strip(), data_dict.get(day).get(time)[0], data_dict.get(day).get(time)[1])
                # Format the data (    time  washer  dryer)

        return out_data

    def read_file(self):
        """Reads each file and then puts the data into a list in a dictionary in a dictionary (ridiculous, I know)"""
        day_dict = {"Mon": {}, "Tue": {}, "Wed": {}, "Thu": {}, "Fri": {}, "Sat": {}, "Sun": {}}
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError("Data files not found (have you run the collector yet?)")
        with open(self.dryer_file, 'r') as fn:
            d_data = fn.readlines()
        with open(self.washer_file, 'r') as fn2:
            w_data = fn2.readlines()

        for line in w_data:
            day = line[:3]
            time = line[4:6]
            data = self.do_math(line[7:].split())
            day_dict[day][time] = [data, 0]
        for line in d_data:
            day = line[:3]
            time = line[4:6]
            data = self.do_math(line[7:].split())
            day_dict[day][time] = [day_dict.get(day).get(time)[0], data]

        # day_dict in the format {day{time}[washer, dryer]}}
        return day_dict

    def compile_data(self):
        out_data = self.format_data()
        with open(self.out_file, 'w') as of:
            of.write(out_data)

    def do_math(self, data_list):
        """Gets average of all data points"""
        total = 0
        i = 0
        while i < len(data_list):
            total += int(data_list[i])
            i += 1
        return total/i  # Just get average for now
