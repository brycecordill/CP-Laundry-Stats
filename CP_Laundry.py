#!/usr/bin/env python3
import argparse
import logging
import json
import os
import sys
import data_collector
import compile_data

class CP_Laundry:
    def __init__(self):

        logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')  # Enable logging to file
        a_parser = argparse.ArgumentParser()
        a_parser.add_argument("-c", "--collect", action='store_true',
                              help="Collect data on the number of washers and dryers available")
        a_parser.add_argument("-C", "--compile", action='store_true',
                              help="Compile collected data into a human readable format")
        a_parser.add_argument("-u", "--url", type=str,
                              help="Set and save the URL (surrounded by \") for the desired laundry page")
        a_parser.add_argument("-o", "--output", type=str,
                              help="Optionally specify location and name of the output file when compiling data.  "
                                   "Defaults to LaundryTimes.txt if not specified")
        self.args = a_parser.parse_args()
        self.config_data = {}
        self.config_path = 'config/config.json'
        self.compile_OF = "LaundryTimes.txt"


    def run(self):
        if self.args.url:
            if not os.path.exists('config'):
                os.makedirs('config')
            self.config_data['url'] = self.args.url
            self.save_config(self.config_data)
        if self.args.collect:
            self.read_config()
            print(self.config_data.get('url'))
            collector = data_collector.DataCollector(self.config_data.get('url'))
            try:
                collector.run_collector()
            except ConnectionError:
                logging.critical("URL is invalid or the connection was refused")
                print("URL is invalid or the connection was refused")
                sys.exit(1)
            except ValueError:
                print("Invalid machine type detected.  Please send log to developer")
                logging.critical("Invalid machine type detected.  Please send log to developer")
                logging.debug(self.config_data.get('url'))
                sys.exit(1)
        if self.args.compile:
            if self.args.output:
                self.compile_OF = self.args.output
            compiler = compile_data.CompileData(self.compile_OF)
            compiler.run_compiler()




    def read_config(self):
        if not os.path.isfile(self.config_path):
            logging.critical("Config file not found.  Please run with -u")
            print("Config file not found.  Please run with -u")
            raise FileNotFoundError
        with open(self.config_path, 'r') as config:
            self.config_data = json.load(config)

    def save_config(self, data):
        with open(self.config_path, 'w') as config:
            json.dump(data, config)


if __name__ == '__main__':
    cp = CP_Laundry()
    cp.run()