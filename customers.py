from collections import OrderedDict

expectedHeader = ['Child Name', 'Current Belt', 'Date Belt Received',
    'Days Since Belt Received','Child Birthday', 'Gender', 'First Parent Name',
    'First Parent Email', 'First Parent Phone', 'First Parent Address',
    'First Parent City','First Parent State', 'First Parent Zipcode',
    'Second Parent Name', 'Second Parent Email','Second Parent Phone',
    'Second Parent Address', 'Second Parent City','Second Parent State',
    'Second Parent Zipcode', 'Customer Since', 'Active in Drop-In',
    'Date Drop-In Expires', 'Product', 'Plan', 'Events']

campHeader = ['Child Name', 'First Parent Name', 'First Parent Email',
    'First Parent Phone', 'First Parent Address', 'First Parent City',
    'First Parent State', 'First Parent Zipcode', 'Customer Since',
    'Active in Drop-In','Date Drop-In Expires', 'Product', 'Plan', 'Events']

def verifyHeader(headerToVerify):
    isHeaderOkay = True
    errorList = []
    for headerE, headerV in zip(expectedHeader, headerToVerify):
        if headerV != headerE:
            isHeaderOkay = False
            errorList.append(headerV)
    return isHeaderOkay, errorList

def removeDuplicates(listOfOrderedDict):
    #The first duplicate in the list will remain
    #subsequent duplicates will be removed
    listWithoutDuplicates = []
    for row in listOfOrderedDict:
        isMatch = False
        for entry in listWithoutDuplicates:
            if(entry['Child Name'] == row['Child Name']):
                isMatch = True
        if(not isMatch):
            listWithoutDuplicates.append(row)
    return listWithoutDuplicates

def findCampOnlyCustomers(listToSearch):
    listIndex = 0
    numberOfCampOnlyKids = 0
    numberOfActiveDIs = 0
    numberOfInactiveDIs = 0
    print("Number of items in list to search for camp only ninjas: {}".format(len(listToSearch)))
    listToSearchWithoutDuplicates = listToSearch #for now just make a copy
    #listToSearchWithoutDuplicates = removeDuplicates(listToSearch)
    #print("Number of items in list to search for camp only ninjas after removing duplicates: {}".format(len(listToSearchWithoutDuplicates)))
    campOnlyList = [] #this list contains ordered dictionaries
    for row in listToSearchWithoutDuplicates:
        tempOrderedDict = OrderedDict()
        if(not (row['Active in Drop-In'] == 'Yes')):
            print("{} {} ".format(listIndex, row['Child Name']))
            if(not(row['Events'] == "") and (row['Plan'] == "")): #if the Events is not empty, camp or PNO
                numberOfCampOnlyKids += 1
                for col in campHeader: #grab the columns we want in the output
                    tempOrderedDict[col] = row[col]
                campOnlyList.append(tempOrderedDict)
            else:   #active drop is a No, but there are no events, so must be
                    #a former DI
                numberOfInactiveDIs += 1
        else: #this entry is an Active DI
            numberOfActiveDIs += 1
        # if (listIndex < 10):
        #     print("{} {} ".format(listIndex, row['Child Name']))
        listIndex += 1
    print("Number of Active DIs: {}".format(numberOfActiveDIs))
    print("Number of former DIs: {}".format(numberOfInactiveDIs))
    print("Number of Camp Only Kids: {}".format(numberOfCampOnlyKids))
    return campOnlyList
