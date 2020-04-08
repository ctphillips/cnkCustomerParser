expectedHeader = ['Name', 'Company', 'Customer Type','Email', 'Phone',
    'Mobile', 'Fax', 'Website', 'Street', 'City','State', 'ZIP', 'Country',
    'Opening Balance', 'Date', 'Resale Number']

expectedExportHeader = ['Customer', 'Company', 'Street Address', 'City',
    'State', 'Country', 'ZIP', 'Phone', 'Email', 'Attachments',
    'Open Balance', 'Notes']

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
