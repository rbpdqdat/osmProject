import re

def is_zip(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip_codes(zip_code):
    #making zip codes consistent
    #filter out possible non-numeric zip codes
    #I didn't find any non-numeric zip codes, but I 
    #thought it was likely
    nonnumber = re.compile('[A-Za-z]')
    if nonnumber.search(zip_code) is not None:
        zip_code = '99999'
    if len(zip_code)<5:
        zip_code = '99999'
    #follow conventional length of 5 digits
    if len(zip_code)>6 :
        #unsupported operand type| zip_beginning.match(zip_code)==False :
        #split zipcode if 'dash' present
        # or take the first 5 digits
        if (re.search('-',zip_code) is not None):
            zip_code=zip_code.split('-')[0]
            zip_code = zip_code[0:5]
        else:
            zip_code = zip_code[0:5]    
    return zip_code
