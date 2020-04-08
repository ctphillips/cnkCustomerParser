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
