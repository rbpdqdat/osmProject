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

k_types = set()
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
CREATE_META = ['version', 'uid', 'user', 'changeset', 'timestamp']

street_types = defaultdict(set)

def shape_element(element, meta_fields=CREATE_META, 
                default_tag_type='regular'):
    nodeway = {}
    #simple check to determine if the parent element is 
    #of type 'node' or tyep 'way'  
    if element.tag == 'node' | element.tag == 'way':
        node['type'] = element.tag
        node['pos'] = [floatorNone(element.get("lat")), floatorNone(element.get("lon"))]
        node['id'] = element.get("id")
        node['visible'] = element.get("visible")
        node["created"] = {}
        for key in meta_fields:
            nodeway["created"][key] = element.get(key)
        for child in element.getchildren:
            parseChild(node,child):
         return node
    else:
        return None

#parsing the child elements of the 'way' and 'node' types
def parseChild(node,children):
    k = children.get("k")
    r = children.get("r")
    #create a unique list of the key types
    k_types.add(k)
    if k and not re.search(problemchars, k):
    #if is_zip(child):
    #    child.attrib['v'] = audit_zip_codes(child.attrib['v'])
        if LOWER_COLON.match(k):
            if (k.split(':',1)[0] == 'addr'):
                node["address"] = node["address"] if node.get("address") else {}
                if (k.split(":")[1] == 'postcode'):
                    #audit the zip code to a standard format
                    node["address"]["zipcode"] = audit_zip_codes(children.attrib['v'])
                elif is_street_name(k):
                    #audit the street names to a standard format
                    node["address"]["street"] = audit_street_type(street_types, 
                             children.attrib['v'])(k.split(":")[1] == 'street')
               else:
                    node["address"][k.split(':',1)[1]] = children.attrib['v']
        elif ( k == 'phone'):
            #audit phone numbers to a standard format
            node['phone'] = audit_phone_number(children.attrib['v'])
        else:
            node[k] = children.attrib['v']
    
    elif r:
        node["node_refs"] = node["node_refs"] if node.get("node_refs") else []
        node["node_refs"].append(ref)
        

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

