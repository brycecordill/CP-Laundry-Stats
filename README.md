# CP-Laundry-Stats
A program that helps you find the best time to do laundry at Cal Poly by outputting the average number of washers and dryers available at a given hour of a given day of the week.

# Dependencies
In order to run, the pyton modules ```requests``` and ```bs4``` need to be installed.  To install these modules, run
```pip install bs4 requests```

# Usage
This program should really be run on a server (or always-on machine) as a scheduled task every hour.  The more data the program gets, the more accurate the results.  The program can be run multiple times in one hour, but the data is only recorded to the hour.

Note: Linux users can replace ```python3 CP_Laundry.py [options]``` with ```./CP_Laundry.py [options]```

Before running for the first time, you must set the URL of the desired laundry location.  You can find this URL by navigating to http://washalert.washlaundry.com/washalertweb/calpoly/cal-poly.html and selecting your building.  Then, copy the URL from you browser's address bar and input it into this command (Note the surrounding "")
```
python3 CP_Laundry.py -u "your-url-here"
```

In order to collect data, issue the command
```
python3 CP_Laundry.py -c
```

To compile the data into a readable report, run 
```
python3 CP_Laundry.py -C
```
By default, the report will be in named LaundryTimes.txt and will be placed in the current directory.

For more options, use, the ```-h``` flag
