#! /usr/local/bin/python3
#read data from csv file exporting from the empolyee dojo
#environment: source ~/.virtualenvs/cnkenv/bin/activate

import csv
import os
from sys import argv
from datetime import datetime
from collections import OrderedDict

import customers
import customersQBO

#check to be sure that the script was called with a file to parse.
isQBO = False
if len(argv) < 2:
  print("Usage: python3 cnkCustomerParser.py filenameToBeParsed <qbofileToBeParsed>")
  exit(1)
if len(argv) == 2:
    script, infile = argv
if len(argv) == 3:
    script, infile, qboInfile = argv
    isQBO = True
if len(argv) > 3:
    print("Usage: python3 cnkCustomerParser.py filenameToBeParsed <qbofileToBeParsed>")
    exit(1)

# file_path = (os.path.join(os.path.expanduser('~'), 'Projects',
#             'CodeNinjas','cnkCustomerParser', 'data',infile))
file_path = os.path.abspath(infile)

#make sure the file to be parsed exists in the data folder
current_file = file_path

if not(os.path.exists(current_file)):
  print("FILE OR PATH DOES NOT EXIST: {}".format(current_file))
  exit(1)
print(current_file)

if isQBO:
    qbofile_path = os.path.abspath(qboInfile)
    qbo_file = qbofile_path
    if not(os.path.exists(qbo_file)):
      print("FILE OR PATH DOES NOT EXIST: {}".format(qbo_file))
      exit(1)
    print(qbo_file)

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
    #create a list of the orderedDict items from the csv reader
    orderedDictList = []
    for entry in csv_reader:
    #     #print(entry['Child Name'], entry['Active in Drop-In'])
        entryCount+=1
        # if(entryCount == 1):
        #     print(entry)
        orderedDictList.append(entry)
    print("There are {} entries in the file".format(entryCount))

#Make sure the header has the expected column headers
isHeaderOkay, errorHeader = customers.verifyHeader(header)

if isHeaderOkay:
    print("Header in file is as expected.")
else:
    print("Header in input file has the following diffrence(s): {}"
        .format(errorHeader))
    exit(1)

campOnlyCustomersList = customers.findCampOnlyCustomers(orderedDictList)

if isQBO:
    #needed to add 'utf-8-sig' to avoid reading in the byte order mark (BOM)
    #when importing the csv file exported from QBO, not doing this we would
    #read a leading /ufeff in the first element/header value
    with open(qbo_file, 'r', encoding='utf-8-sig') as qboCsv_file:
        qboCsv_reader = csv.DictReader(qboCsv_file)
        #print(type(csv_reader))
        #print(csv_reader.fieldnames)
        qboHeader = qboCsv_reader.fieldnames
        #print("There are {} columns in the file.".format(len(qboHeader)))
        #print("The type of the fieldnames is {}".format(type(qboHeader)))
        # print(qboHeader)
        # for colName in qboHeader:
        #      print(colName)

        qboEntryCount = 0
        #create a list of the orderedDict items from the csv reader
        qboOrderedDictList = []
        for qboEntry in qboCsv_reader:
        #     #print(entry['Child Name'], entry['Active in Drop-In'])
            qboEntryCount+=1
            # if(entryCount == 1):
            #     print(entry)
            qboOrderedDictList.append(qboEntry)
        print("There are {} entries in the QBO file".format(qboEntryCount))
    #Make sure the qbo header has the expected column headers
    isQBOHeaderOkay, errorQBOHeader = customersQBO.verifyHeader(qboHeader)

    if isQBOHeaderOkay:
        print("Header in QBO file is as expected.")
    else:
        print("Header in input QBO file has the following diffrence(s): {}"
            .format(errorQBOHeader))
        exit(1)

modifiedOrderedDictList = []

#build a list of OrderedDict from the Employee Dojo export
#using the necessary keys for the QBO Customer Import Template
for row in orderedDictList:
    ordered_dict = OrderedDict() #make a new orderdict obj
    ordered_dict.fieldnames = customersQBO.expectedHeader
    ordered_dict['Name'] = row['First Parent Name']
    ordered_dict['Company'] = ''
    ordered_dict['Customer Type'] = ''
    ordered_dict['Email'] = row['First Parent Email']
    ordered_dict['Phone'] = row['First Parent Phone']
    ordered_dict['Mobile'] = ''
    ordered_dict['Fax'] = ''
    ordered_dict['Website'] = ''
    ordered_dict['Street'] = row['First Parent Address']
    ordered_dict['City'] = row['First Parent City']
    ordered_dict['State'] = row['First Parent State']
    ordered_dict['ZIP'] = row['First Parent Zipcode']
    ordered_dict['Country'] = ''
    ordered_dict['Fax'] = ''
    ordered_dict['Opening Balance'] = 0
    date_object = datetime.strptime(row['Customer Since'],"%m-%d-%Y")
    ordered_dict['Date'] = date_object.strftime("%Y-%m-%d")
    ordered_dict['Resale Number'] = 0
    modifiedOrderedDictList.append(ordered_dict)

# for row in modifiedOrderedDictList:
    #print(row)
modifiedOrderedDictListWithoutDuplicates = customersQBO.removeDuplicates(modifiedOrderedDictList)

entriesWithoutDuplicates = 0
for entry in modifiedOrderedDictListWithoutDuplicates:
    entriesWithoutDuplicates +=1
    # if(entriesWithoutDuplicates != 0):
    #     print(entry["Name"])
print("Number of entries in Employee Dojo List after duplicates have been removed is {}".format(entriesWithoutDuplicates))

if isQBO:
    # for entry in qboOrderedDictList:
    #     print(entry['Customer'])
    finalOrderedDictList = customersQBO.removeMatches(qboOrderedDictList,
        modifiedOrderedDictListWithoutDuplicates)
else:
    finalOrderedDictList = modifiedOrderedDictListWithoutDuplicates
# for row in finalOrderedDictList:
#     print(row)
entriesAfterMatchesRemoved = 0
for entry in finalOrderedDictList:
    #print(entry['Name'])
    entriesAfterMatchesRemoved +=1
print("Number of entries in Employee Dojo List that are not already in QBO is {}".format(entriesAfterMatchesRemoved))

if(entriesAfterMatchesRemoved != 0):
    #send the processed list to a csv file for importing into QBO
    #grab the tail of the infile
    infileTail = os.path.split(infile)[1]
    outfileForQBOCustomers = infileTail.split(".")[0] + 'QBO' + '.csv'
    outfilePathQBO = (os.path.join(os.path.expanduser('~'), 'Projects',
            'CodeNinjas','cnkCustomerParser', 'data', outfileForQBOCustomers))
    print(outfilePathQBO)
    with open(outfilePathQBO, 'w') as f:
        fWriter = csv.DictWriter(f, fieldnames = customersQBO.expectedHeader,
            delimiter=',')
        fWriter.writeheader() #put the column headers in the csv
        for row in finalOrderedDictList:
            fWriter.writerow(row)

#send the processed list to a csv file for Camp Only Ninjas
outfileForCampOnly = infileTail.split(".")[0] + 'CampOnly' + '.csv'
outfilePathForCampOnly = (os.path.join(os.path.expanduser('~'), 'Projects',
            'CodeNinjas','cnkCustomerParser', 'data', outfileForCampOnly))
print(outfilePathForCampOnly)
with open(outfilePathForCampOnly, 'w') as f:
    fWriter = csv.DictWriter(f, fieldnames = customers.campHeader,
        delimiter=',')
    fWriter.writeheader() #put the column headers in the csv
    for row in campOnlyCustomersList:
        fWriter.writerow(row)
