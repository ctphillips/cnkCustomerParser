expectedHeader = ['Name', 'Company', 'Customer Type','Email', 'Phone',
    'Mobile', 'Fax', 'Website', 'Street', 'City','State', 'ZIP', 'Country',
    'Opening Balance', 'Date', 'Resale Number']

expectedExportHeader = ['Customer', 'Company', 'Street Address', 'City',
    'State', 'Country', 'Zip', 'Phone', 'Email', 'Attachments',
    'Open Balance', 'Notes']

def verifyHeader(headerToVerify):
    isHeaderOkay = True
    errorList = []
    for headerE, headerV in zip(expectedExportHeader, headerToVerify):
        if headerV != headerE:
            isHeaderOkay = False
            errorList.append(headerV)
    return isHeaderOkay, errorList

def removeDuplicates(listOfOrderedDict):
    listWithoutDuplicates = []
    for row in listOfOrderedDict:
        isMatch = False
        for entry in listWithoutDuplicates:
            if(entry['Name'] == row['Name']):
                isMatch = True
        if(not isMatch):
            listWithoutDuplicates.append(row)
    return listWithoutDuplicates

def removeMatchesFromEmployeeDojo(qboList, employeeDojoList):
    #build a list of OrderedDict objects that do not exist
    #in the qboList
    listWithoutMatches = []
    for row in employeeDojoList:
        #grab the next entry in the employeeDojoList
        isMatch = False
        #cycle through each record in the qboList
        #until either the end of the list or if a match is found
        for entry in qboList:
            #first remove any extra spaces in the name fields
            customer = entry['Customer'].replace(" ", "")
            name = row['Name'].replace(" ", "")
            if( customer == name):
                isMatch = True
                break #found a match so stop looking
        #if match is still false, then add the record to the list
        if(not isMatch):
            listWithoutMatches.append(row)
    return listWithoutMatches

def removeMatchesFromQBO(qboList, employeeDojoList):
    #build a list of OrderedDict objects that do not exist
    #in the employeeDojoList
    listWithoutMatches = []
    for entry in qboList:
        #grab the next entry in the qboList
        isMatch = False
        #cycle through each record in the employeeDojoList
        #until either the end of the list or if a match is found
        for row in employeeDojoList:
            #first remove any extra spaces in the name fields
            customer = entry['Customer'].replace(" ", "")
            name = row['Name'].replace(" ", "")
            if( customer == name):
                isMatch = True
                break #found a match so stop looking
        #if match is still false, then add the record to the list
        if(not isMatch):
            listWithoutMatches.append(entry)
    return listWithoutMatches
