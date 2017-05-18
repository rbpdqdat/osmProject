import pprint
import re
import codecs
import xml.etree.cElementTree as ET
import phonenumbers
from collections import defaultdict
import pprint
import json
import zipcode
import phone
import address

OSM_PATH = "denverMetro.osm"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
FIELDS = ['type','pos','id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']

street_types = defaultdict(set)

def shape_element(element, attr_fields=FIELDS, 
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):

    nodeway_attribs = {}
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node' | element.tag == 'way':
        for attrib in element.attrib:
            #if attrib in FIELDS:
            #    nodeway_attribs[attrib] = element.attrib[attrib]

        addressDict = {}
        for child in element:
            node_tag = {}
            if is_zip(child):
                    child.attrib['v'] = audit_zip_codes(child.attrib['v'])
            if LOWER_COLON.match(child.attrib['k']):
                if (child.attrib['k'].split(':',1)[0] == 'addr'):
                    if (child.attrib['k'].split(":")[1] == 'postcode'):
                        addressDict.update({'zipcode':child.attrib['v']})
                    else:
                        addressDict.update({child.attrib['k'].split(':',1)[1]:child.attrib['v']})
            elif PROBLEMCHARS.match(child.attrib['k']):
                continue
            elif (child.attrib['k'] == 'phone'):
                node_tag['phone'] = child.attrib['v']
                nodeway_attribs.update(node_tag)
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['value'] = child.attrib['v']
                nodeway_attribs.update(node_tag)
    
            if any(addressDict.keys()) == True :
                node_tag['address'] = addressDict
                nodeway_attribs.update(node_tag)
        return {'node': nodeway_attribs}
        

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to json"""
    data = []
    file_out = "{0}.json".format(OSM_PATH)
    data = []
    with codecs.open(file_out, "w") as fo:
        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                data.append(el)
                fo.write(json.dumps(el) + "\n")

if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)

