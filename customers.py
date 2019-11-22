expectedHeader = ['Child Name', 'Current Belt', 'Date Belt Received',
    'Days Since Belt Received','Child Birthday', 'Gender', 'First Parent Name',
    'First Parent Email', 'First Parent Phone', 'First Parent Address',
    'First Parent City','First Parent State', 'First Parent Zipcode',
    'Second Parent Name', 'Second Parent Email','Second Parent Phone',
    'Second Parent Address', 'Second Parent City','Second Parent State',
    'Second Parent Zipcode', 'Customer Since', 'Active in Drop-In',
    'Date Drop-In Expires', 'Product', 'Plan', 'Events']

def verifyHeader(headerToVerify):
    isHeaderOkay = True
    errorList = []
    for headerE, headerV in zip(expectedHeader, headerToVerify):
        if headerV != headerE:
            isHeaderOkay = False
            errorList.append(headerV)
    return isHeaderOkay, errorList
