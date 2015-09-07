
# coding: utf-8

# In[47]:

from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')


# #Data Analyst Nanodegree
# ##Project 3: Data Wrangling with MongoDB

# ###1.0 Introduction

# This document presents the results of Project 3: Data Wrangling with MongoDB for the Udacity Data Science Nanodegree. This assessment required the student to choose any area of the world from OpenStreetMaps here https://www.openstreetmap.org and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the map data.

# ###2.0 Background

# For this project, I chose my place of birth (Perth, Australia) and downloaded the according MapZen OSM XML metro extract here https://mapzen.com/data/metro-extracts. Results within this document are based on data retrieved on the 7th of September 2015. Note that the boundary box geographical coordinate system ranges on the OpenStreetMap website for Perth, Australia are latitude: 115.4340, 116.2862, longitude -31.6867, -32.2174.

# ###3.0 Data Wrangling

# ####Data Audit

# In order to audit the perth_australia.osm file, the map file was first processed to find tag properties. The output generated below is a dictionary with tag name as the key and number of times this tag can be found.

# In[1]:

import xml.etree.ElementTree as ET
import collections
import pprint

osmfilenm = 'data/perth_australia.osm'


def count_tags(filename):
    count = collections.defaultdict(int)
    for line in ET.iterparse(filename, events=("start",)):
        current = line[1].tag
        count[current] += 1
        
    return count


tags = count_tags(osmfilenm)
pprint.pprint(tags)


# Each tag was checked against a string of valid keys in MongoDB in order to identify whether there are any problematic characters.

# In[2]:

import re
import xml.etree.ElementTree as ET
import pprint

osmfilenm = 'data/perth_australia.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value) is not None:
            keys['lower'] += 1
        elif lower_colon.search(k_value) is not None:
            keys['lower_colon'] += 1
        elif problemchars.search(k_value) is not None:
            keys["problemchars"] += 1
        else:
            keys['other'] += 1
            
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        
    return keys


keys = process_map(osmfilenm)
pprint.pprint(keys)


# The below shows an audit the map file to return a list of contributing users.

# In[7]:

import xml.etree.ElementTree as ET
import pprint

osmfilenm = 'data/perth_australia.osm'


def get_user(element):
    user = element.attrib['user']
    
    return user


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if element.tag == "node":
            users.add(get_user(element))
            
    return users


users = process_map(osmfilenm)
pprint.pprint(users)


# The below shows an audit the map file to return a list of street names.

# In[23]:

import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint

osmfilenm = 'data/perth_australia.osm'

street_name_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")


def audit_street_name(street_names, street_name):
    m = street_name_re.search(street_name)
    if m:
        street = m.group()
        street_names[street] += 1


def audit(filename):
    osm_file = open(filename, "r")
    street_names = collections.defaultdict(int)
    for event, elem in ET.iterparse(osm_file):
        if is_street_name(elem):
            audit_street_name(street_names, elem.attrib['v'])   
    print_sorted_dict(street_names)


def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 


streets = audit(osmfilenm)
pprint.pprint(streets)


# ####Encountered Problems

# A number of street name abbreviations and errors were identified from the street name audit. In order to correct these for consistency, a list of expected street names were prepared and checked against. All street names which failed to match against the expected list were replaced with proposed correct names. A list of the identified street name errors and proposed changes are shown below.

# In[24]:

import xml.etree.ElementTree as ET
import collections

osmfilenm = 'data/perth_australia.osm'

street_name_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

street_name_expected = ["Avenue", "Beaufort", "Boulevard", "Boulevarde", "Broadway", "Circle", "Circuit", "Close", "Corner",
                        "Court", "Courtyard", "Cove", "Crescent", "Cross", "Crossway", "Dale", "Drive", "East", "Edge",
                        "Elbow", "Entrance", "Elbow", "Esplanade", "Fairway", "Gap", "Garden", "Gardens", "Gate", "Gates",
                        "Gelderland", "Grade", "Grange", "Green", "Grove", "Haven", "Heights", "Highgate", "Highway", "Hill",
                        "Lane", "Laneway", "Link", "Loop", "Mews", "Morrison", "North", "Oxford", "Parade", "Parkway", "Pass",
                        "Place", "Promenade", "Quarry", "Quays", "Ramble", "Road", "Retreat", "Ridgeway", "Rise", "Sava",
                        "Square", "Street", "Terrace", "Trail", "Turn", "University",  "Vale", "View", "Vista", "Way", "West",
                        "Wharf"]

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


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit_street_name(invalid_street_names, street_name):
    m = street_name_re.search(street_name)
    if m:
        street_names = m.group()
        if street_names not in street_name_expected:
            invalid_street_names[street_names].add(street_name)


def audit(osmfile):
    osm_file = open(osmfile, "r")
    invalid_street_names = collections.defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_name(invalid_street_names, tag.attrib['v'])
                    
    return invalid_street_names
  

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


ret_st_types = audit(osmfilenm)

for st_type, ways in ret_st_types.iteritems():
    for name in ways:
        proposed_name = update_street_name(name, street_name_map, street_name_replace)
        print name, "=>", proposed_name


# A number of postal code errors were also found within the original dataset. Each postcode was checked against a correct range (6000 to 6999), with errors replaced with a default code of 6000. Again, a list of the identified incorrect postal codes and proposed changes are shown below.

# In[25]:

import xml.etree.ElementTree as ET
import collections

osmfilenm = 'data/perth_australia.osm'

postal_code_range = [6000,6999]
postal_code_default = 6000


def is_postal_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit_postal_code(invalid_postal_codes, postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
    except ValueError:
        invalid_postal_codes[postal_code] += 1


def audit(osmfile):
    osm_file = open(osmfile, "r")
    invalid_postal_codes = collections.defaultdict(int)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(invalid_postal_codes, tag.attrib['v'])

    return invalid_postal_codes


def update_postal_code(postal_code):
    try:
        if not (postal_code_range[0] <= int(postal_code) <= postal_code_range[1]):
            raise ValueError
        else:
            return int(postal_code)
    except ValueError:
        return postal_code_default


ret_codes = audit(osmfilenm)

for ways in ret_codes.iteritems():
    for code in ways:
        proposed_code = update_postal_code(code)
        print code, "=>", proposed_code


# ####Creating the .json map file

# Check first five entries to see if data matches what is expected.

# In[28]:

pprint.pprint(data[0:5])


# ###4.0 Data Exploration

# ####Load data into MongoDB instance

# In[29]:

from pymongo import MongoClient
#from data import *

def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


db = get_db('test')
#data = process_map(osmfilenm, True)

[db.perth.insert(e) for e in data]


# ####Database structure

# File size comparison:

# perth_australia.osm: 204 MB (214,742,096 bytes)
# perth_australia.osm.json: 320 MB (335,878,944 bytes)

# Total number of documents in database:

# In[31]:

db.perth.find().count()


# Number of nodes in database:

# In[32]:

db.perth.find({'type':'node'}).count()


# Number of ways in database:

# In[33]:

db.perth.find({'type':'way'}).count()


# Number of cafe's in database:

# In[46]:

db.perth.find({'amenity':'cafe'}).count()


# Number of cinema's in database:

# In[42]:

db.perth.find({'amenity':'cinema'}).count()


# Number of bank's in database:

# In[43]:

db.perth.find({'amenity':'bank'}).count()


# In[35]:

from pymongo import MongoClient
from pprint import pprint

class pipe_list(object):
    def top_post_user(self):
        return [
                {'$group': {'_id': '$created.user',
                            'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 1}
        ]

    def top_three_post_users(self):
        return [
                {'$group': {'_id': '$created.user',
                            'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 3}
        ]
    
    def single_post_users(self):
        return [
            {'$group': {'_id': '$created.user',
                        'count': {'$sum': 1}}}, 
            {'$group': {'_id': '$count',
                        'num_users': {'$sum': 1}}},
            {'$sort': {'_id': 1}},
            {'$limit': 1}
        ]

    def top_five_amenity(self):
        return [
            {'$match': {'amenity': {'$exists': 1}}},
            {'$group': {'_id': '$amenity', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 5}
        ]

    def top_five_fastfood(self):
        return [
            {'$match': {'amenity': 'fast_food'}},
            {'$group': {'_id': '$name', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 5}
        ]
    
pipeline = pipe_list()


# User with highest post count:

# In[36]:

print(list(db.perth.aggregate(pipeline.top_post_user())))


# Top three users by post count:

# In[37]:

print(list(db.perth.aggregate(pipeline.top_three_post_users())))


# Count of users who have made a single post:

# In[38]:

print(list(db.perth.aggregate(pipeline.single_post_users())))


# Top five amenity by count:

# In[40]:

print(list(db.perth.aggregate(pipeline.top_five_amenity())))


# Top five fast food by count:

# In[41]:

print(list(db.perth.aggregate(pipeline.top_five_fastfood())))


# ####Create a sample database

# In[48]:

#!/usr/bin/env python


import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "data/perth_australia.osm"  # Replace this with your osm file
SAMPLE_FILE = "data/perth_australia_sample.osm"


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every 10th top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % 10 == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# perth_australia_sample.osm: 20.7 MB (21,770,717 bytes)

# ###5.0 Conclusion

# Overall, I didnt have too much trouble processing the dataset. There were no 'problemchars' identified as part of the first pass. Based on my memory of Perth, most of the reported amenity counts seem reasonable, however caution should be exercised when interpreting the presented results as the completeness of the data is unknown. Finally, I did not get a chance to exercise MonogDB's geospatial querying, however the original dataset contains a large amount of latitude/longitude data.

# ###References

# * PyMongo Documentation: https://api.mongodb.org/python/current/
# * Udacity Data Wrangling with MonogoDB: https://www.udacity.com/course/data-wrangling-with-mongodb--ud032
