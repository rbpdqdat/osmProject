import re
import phonenumbers
#convert alphabet phone characters to actual phone numbers
#

missphone = '+19999999999'

def phone_letter_tonum(alphaphone):
    char_numbers = [('abc',2), ('def',3), ('ghi',4), ('jkl',5), ('mno',6), ('pqrs',7), ('tuv',8), ('wxyz',9)]
    char_num_map = {c:v for k,v in char_numbers for c in k}
    return("".join(str(char_num_map.get(v,v)) for v in alphaphone.lower()))

def is_phone(elem):
    return (elem.attrib['k'] == "phone")

def audit_phone_number(phone):
    #found some columns had 2 phone numbers
    phone = phone.split(";")[0]
    phone = re.sub("^\++0+1?","+1",phone)
    #some phone numbers were purposely words
    # such as '1-888-AMC-4FUN' for business 
    #the phone number needed to be converted to properly work
    if re.search("[A-Za-z]",phone):
        phone = phone_letter_tonum(phone)
    if (re.search('^[\+1]',phone) == None):
        phone = missphone
    #additional substitution to make sure the 
    #country code was in the phone number
    phone = re.sub("^1+","+1",phone)
    z = phonenumbers.parse(phone, "US")
    phone = phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.NATIONAL)

    return phone
