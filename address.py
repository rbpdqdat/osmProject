import re

street_types = set()

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

#mapping the abbreviations of the street names
mapping = { "St": "Street",
            "St.": "Street",
            "Rd." : "Road",
            "Ave" : "Avenue",
            "Cir" : "Circle",
            "Ct"  : "Court"
            }

k_types = set()

def audit_k_attributes(elem):
    return elem.attrib['k']

def audit_street_type(street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types.add(street_name)
    return update_name(street_name,mapping)

#had to relook at the regular expression I was using
#It was matching all long names and replacing
#creating erronious names such as AveAvenue
def update_name(name, mapping):
    st = re.compile('St\.?\s?$')
    name = st.sub("Street",name)
    rd = re.compile('Rd\.?\s?$')
    name = rd.sub("Road", name)
    ave = re.compile('Ave\.?\s?$')
    name = ave.sub("Avenue", name)
    dr = re.compile('Dr.?\s?$')
    name = dr.sub('Drive',name)
    cir = re.compile('Cir\.?\s?$')
    name = cir.sub('Circle',name)
    ct = re.compile('Ct\.?\s?$')
    name = ct.sub('Court',name)

    return name
