
import re
import codecs
import xml.etree.ElementTree as ET
import json
import pprint

osmfilenm = 'data/perth_australia.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

street_name_map = { "ave" : "Avenue",
                    "avenuet" : "Avenue",
                    "cres" : "Crescent",
                    "crs" : "Cross",
                    "crt" : "Court",
                    "ct" : "Court",
                    "rd" : "Road",
                    "st" : "Street",
                    "tce" : "Terrace",
                    "terriace" : "Terrace",
                    "wa" : "Way"}

street_name_replace = { "Fitzgerald St (corner View St)" : "Fitzgerald Street",
                        "Tarata Wy E/Ent" : "Tarata Way",
                        "TARATA WY E/ENT" : "Tarata Way",
                        "TARATA WY W/ENT" : "Tarata Way",
                        "TARATA WY E/ENT (LANEWAY)" : "Tarata Way",
                        "TARATA WAY E/ENT" : "Tarata Way",
                        "TARATA WAY SW ENTRANCE" : "Tarata Way",
                        "E Linden Way (In Laneway)" : "Linden Way" }

postal_code_range = [6000,6999]
postal_code_default = 6000


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def update_street_name(street_name, street_name_map, street_name_replace):
    if street_name in street_name_replace.keys():
        new_name = street_name_replace[street_name]
        return new_name
    
    after = []
    for part in street_name.split(" "):
        part = part.strip(",\.").lower()
               
        if part in street_name_map.keys():
            part = street_name_map[part]
        after.append(part.capitalize())
    
    return " ".join(after)


def update_postal_code(postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
        else:
            return int(postal_code)
    except ValueError:
        return postal_code_default


def shape_element(e):
    node = {}
    node['created'] = {}
    node['pos'] = [0,0]
    if e.tag == "way":
        node['node_refs'] = []
    if e.tag == "node" or e.tag == "way" :
        node['type'] = e.tag
        for k, v in e.attrib.iteritems():
            #latitude
            if k == 'lat':
                try:
                    lat = float(v)
                    node['pos'][0] = lat
                except ValueError:
                    pass
            #longitude
            elif k == 'lon':
                try:
                    lon = float(v)
                    node['pos'][1] = lon
                except ValueError:
                    pass
            elif k in CREATED:
                node['created'][k] = v
            else:
                node[k] = v
        for tag in e.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']
            if problemchars.match(k):
                continue
            elif lower_colon.match(k):
                k_split = k.split(':')
                if k_split[0] == 'addr':
                    k_item = k_split[1]
                    if 'address' not in node:
                        node['address'] = {}
                    #streets
                    if k_item == 'street':
                        v = update_street_name(v, street_name_map, street_name_replace)                    
                    #postal codes
                    if k_item == 'postcode':
                        v = update_postal_code(v)
                    node['address'][k_item] = v
                    continue
            node[k] = v
        if e.tag == "way":
            for n in e.iter('nd'):
                ref = n.attrib['ref']
                node['node_refs'].append(ref);
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


data = process_map(osmfilenm, True)