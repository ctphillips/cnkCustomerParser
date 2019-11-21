#! /usr/local/bin/python3
#read data from csv file exporting from the empolyee dojo
#environment: source ~/.virtualenvs/cnkenv/bin/activate

import csv
import os
from sys import argv
from datetime import datetime
from collections import OrderedDict

import customers

#check to be sure that the script was called with a file to parse.
if len(argv) < 2:
  print("Usage: python3 cnkCustomerParser.py filenameToBeParsed")
  exit(1)
script, infile = argv

file_path = (os.path.join(os.path.expanduser('~'), 'Projects',
            'CodeNinjas','cnkCustomerParser', 'data',infile))

#make sure the file to be parsed exists in the data folder
current_file = file_path
if not(os.path.exists(current_file)):
  print("FILE OR PATH DOES NOT EXIST: {}".format(current_file))
  exit(1)
print(current_file)

with open(current_file, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    #print(type(csv_reader))
    #print(csv_reader.fieldnames)
    header = csv_reader.fieldnames
    print("There are {} columns in the file.".format(len(header)))
    #print("The type of the fieldnames is {}".format(type(header)))
    # for colName in header:
    #     print(colName)

    entryCount = 0
    for entry in csv_reader:
    #     #print(entry['Child Name'], entry['Active in Drop-In'])
        entryCount+=1
        if(entryCount == 1):
            print(entry)
    print("There are {} entries in the file".format(entryCount))

    #Make sure the header has the expected column headers
    isHeaderOkay, errorHeader = customers.verifyHeader(header)

    if isHeaderOkay:
        print("Header in file is as expected.")
    else:
        print("Header in input file has the following diffrence(s): {}"
            .format(errorHeader))

# for customer in customers.expectedHeader:
#     print(customer)
