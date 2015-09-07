

```python
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
```




<script>
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
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>



#Data Analyst Nanodegree
##Project 3: Data Wrangling with MongoDB

###1.0 Introduction

This document presents the results of Project 3: Data Wrangling with MongoDB for the Udacity Data Science Nanodegree. This assessment required the student to choose any area of the world from OpenStreetMaps here https://www.openstreetmap.org and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the map data.

###2.0 Background

For this project, I chose my place of birth (Perth, Australia) and downloaded the according MapZen OSM XML metro extract here https://mapzen.com/data/metro-extracts. Results within this document are based on data retrieved on the 7th of September 2015. Note that the boundary box geographical coordinate system ranges on the OpenStreetMap website for Perth, Australia are latitude: 115.4340, 116.2862, longitude -31.6867, -32.2174.

###3.0 Data Wrangling

####Data Audit

In order to audit the perth_australia.osm file, the map file was first processed to find tag properties. The output generated below is a dictionary with tag name as the key and number of times this tag can be found.


```python
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
```

    defaultdict(<type 'int'>, {'node': 1000411, 'nd': 1236818, 'bounds': 1, 'member': 10565, 'tag': 368028, 'osm': 1, 'way': 123824, 'relation': 1505})
    

Each tag was checked against a string of valid keys in MongoDB in order to identify whether there are any problematic characters.


```python
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
```

    {'lower': 328169, 'lower_colon': 39185, 'other': 674, 'problemchars': 0}
    

The below shows an audit the map file to return a list of contributing users.


```python
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
```

    set(['(*steve*)',
         '037adventure',
         '2hands',
         '6wheels',
         'AGreig',
         'Abner',
         'AdmiralTriggerHappy',
         'Aidan82',
         'Airwalk',
         'AlainMehl',
         'AlanGraham',
         'Albany Canucks',
         'Alex Kwiatkowski',
         'Alex McKee',
         'Alex-7',
         'AlexOnTheBus',
         'Andre68',
         'Andrew Gregory',
         'AndrewC',
         'AndrianaTreasure',
         'Andy69',
         'Anirudhk1',
         'Apfelmaennchen',
         'Aredhel',
         'Arjanr',
         'AshKyd',
         'Ats!c',
         u'Aurimas Fi\u0161eras',
         'AusAviator',
         'Aushiker',
         'B Lue',
         'BJ Beej',
         'Babstar',
         'BalancingBean',
         'Basso',
         'Batesy',
         'Batty',
         'Beach Manor Bed and Breakfast Perth',
         'Befrasimo',
         'Ben Caldwell',
         'Bess',
         'BiIbo',
         'BinaryMe',
         'Blackcat',
         'BlueMM',
         'Bluey',
         'BoLLo__',
         'Bob Hoskins',
         'Brendan_Cherry',
         'Brown33z',
         'Bryce C Nesbitt',
         u'B\xfcrste',
         'CAMS',
         'CB89',
         'Cadpete',
         'Cannington Exhibition Centre',
         'CartoDIA',
         'Charles Kottler',
         'Chris Parker',
         'ChrisRG',
         'ChristoRowley',
         'Ciela',
         'Claudius Henrichs',
         'Clinton Gladstone',
         'CloCkWeRX',
         'Condor_25',
         'Corinna Conte',
         'Coxyb76',
         'CyFo',
         'D Worsdell',
         'DJT',
         'Daeron',
         'Damyon',
         'Dan101',
         'DanRyan',
         'Daniel Truslove',
         'Daniel-',
         'Darren Sampson',
         'Dave Bills',
         'Dave Rave',
         'David_mds',
         'Davoz',
         'Deadmeat',
         'Deanhaus',
         'Deezza',
         'Delbo',
         'Denning',
         'DennisL',
         'Dero Bike Racks',
         'DevehJ',
         'Dirk Lohse',
         'Don H',
         'DoubleA',
         'Drewboy',
         'Duncan1',
         'Echo63',
         'Elias',
         'ElliottPlack',
         'Elwell',
         'Eric-N',
         'Evaredy',
         'FXST01',
         'Feet First Podiatry',
         'FireLordScans',
         'Fletty',
         'Frankst',
         'Frederik',
         'Fremantle Stay WA',
         'FreoLocal',
         'FunFrogFacePainting',
         'FvGordon',
         'GLXdazz55',
         'Gareth in Perth',
         'GaryWA',
         'GavinX',
         'Geogast',
         'Glen Prideaux',
         'Godzookee',
         'GregMackay',
         'Gregory J Smith',
         'Gyaos',
         'H3rBz',
         'Hagman',
         'Hanggini Pradani',
         'HeckAreWe',
         'Helifella',
         'HellsBells',
         'HolgerJeromin',
         'HomerT51',
         'Hoppyz',
         'HungryHellcat',
         'HybridAU',
         'I_Spy',
         'I_vanl',
         'Ian Banks',
         'Ian McKellar',
         'IanKulin',
         'Indra Budiman',
         'JKhoo',
         'James Livingston',
         'Jameswa21',
         'JansenCordero',
         'JarmanImaging',
         'JayKae',
         'JennyH',
         'Jester16',
         'Jezagee',
         'Jezzamezzamy',
         'Jim Langford',
         'JimmyAt',
         'JohnElston',
         'JohnSmith',
         'Johnshares',
         'Jon Bright',
         'Josef73',
         'Joshua King',
         'Joslin42',
         'Juffles',
         'Juffy',
         'Justin Bedo',
         'JustinBrennan',
         'KDE',
         'Kai Jaeger',
         'KarlLukan',
         'Ketki Bhagwat',
         'Kie723',
         'Killa',
         'Kirstyr4',
         'Knoxy',
         'LSRONG',
         'Lambretta',
         'Latze',
         'Lawn Gnome',
         'Leon K',
         'Liam Jones',
         'Little Brother',
         'Lloyd268',
         'Luis36995',
         'Lumina',
         'Luminesse',
         'Lungfish83',
         'MCC',
         'MDGPS',
         'MDe',
         'Macca27',
         'Manu1400',
         'Map_baker',
         u'Marcos Ra\xfal Carot',
         'Mark Bolton',
         'Markus B',
         'Markus59',
         'Mathbau',
         'Matt Didcoe',
         'Mauls',
         'Maxwell Robinson & Phelps',
         'MaxwellKeeble',
         'Melmann',
         'Michael Neville',
         'MichaelCollinson',
         'MidGe48',
         'Mike Haydon',
         'Mistikal',
         'Modernian',
         'Morgz64',
         'Mr Shush',
         'Mr_Q_',
         'NBN Choice',
         'NE2',
         'NKX',
         'NaFenn',
         'NakedChris',
         'Narilus',
         'Narx',
         'NearMap Pty Ltd',
         'Neil Penman',
         'Neil Spence',
         'NeilMoseley',
         'Netzwolf',
         'Nichalp',
         'NickNewton',
         'Nicko',
         'Nikki G',
         'Northern Sun Solar Power',
         'Nuko',
         'ORYX',
         'OSMF Redaction Account',
         'OSMNZ',
         'OSMcartay',
         'Odilo',
         'OhrImport',
         'Oliver Cooksey',
         'Optimo',
         'Ori952',
         'Oscar Chee',
         'Otto (aka JohnV)',
         'PERcyclist',
         'Palitu',
         'PaulFisher',
         'Perey',
         'Perth Girl',
         'Perth a la Carte',
         'PerthBitcoinATM',
         'Perthpulse',
         'Pete Northrop',
         'Peter H',
         'Peter Kovesi',
         'Peter W34',
         'PeterDdeL',
         'PeterMcM',
         'Phillip Jubb',
         'PlaneMad',
         'ProfChaos',
         'ProfSmiles',
         'Q4004',
         'RM87',
         'Ramzes',
         'Ransom',
         'RationalTangle',
         'Redbusa07',
         'ReindeerNinja',
         'ReinerMeyer',
         'Rekanlovei',
         'RhianJ',
         'Rhodry Korb',
         'RichRico',
         'Richard Press',
         'Richard Stallard',
         'Riyaz Mukarram',
         'Rob83',
         'RobertH[AU]',
         'RodCub',
         'RodPinna',
         'RodinPerth',
         'Rodney',
         'Rolly4x4',
         'Ronald Lopez',
         'Ropino',
         'Rosscoe',
         'Rovastar',
         'Rowanh',
         'Rub21',
         'Rudy355',
         'RusscO',
         'Russkel',
         'Ryan AU',
         'S2333',
         'SDavies',
         'Sam Wilson',
         'SauloCavalcante',
         'Sci Anderson',
         'ScottDavis',
         'SeanMack',
         'ShadowCyclist',
         'ShannonWAC',
         'ShayneM',
         'SimHayes',
         'Simon Cox',
         'Simon Sacro',
         'Skippern',
         'Sleepyhead',
         'SmokyAu',
         'SomeoneElse',
         'Spindoc Bob',
         'Spindustries',
         'Stazza',
         'Stemby',
         'StevePetty',
         'Stevew1954',
         'Stu274',
         'StuartG',
         'StuartL84',
         'Suhaimi2',
         'Swamp Ig',
         'Syl',
         'SyneRyder',
         'T2000',
         'TRS-80',
         'Team Teri',
         'Ted Williamson',
         'Test360',
         'The Process',
         'The Sound Factory',
         'The Vines Avenue Guesthouse',
         'ThePondBarista',
         'Theodin',
         'Thewinchester',
         'TimU',
         'Timmi27',
         'Tom Brownlie',
         'Tom Layo',
         'Tonky',
         'Treadly',
         'Trev',
         'Trevor in Ashfield',
         'Trevski',
         'UPnAWAY82',
         'UWAStudentGuild',
         'Ulmon Community',
         'Uncoordinated',
         'Unusual User Name',
         'Vader_oz',
         'Viet PHUNG',
         'Wakin',
         u'Walter Schl\xf6gl',
         'WanderingAus',
         'Warin61',
         'WarpSpider74',
         'WarrenP',
         'Wasps1',
         'Wayfarer9',
         'WayneLau',
         'Welshie',
         'Witters00',
         'Wood0362',
         'Woz',
         'Wozzich',
         'XJA',
         'Yoda',
         'Zesh',
         'Zignig',
         'Zulu99',
         'a_isaeva',
         'aaronsta',
         'abel801',
         'acv_critter',
         'adam111316',
         'adjuva',
         'adonm',
         'adonmetcalfe',
         'adriank',
         'aharvey',
         'aighes',
         'al-khowarizmi',
         'alester',
         'amanda dr',
         'amdjong',
         'andjam5',
         'andrew_dennison',
         'andrewpmk',
         'andrewpur',
         'andygol',
         'anthonyp0808',
         'antiussentiment',
         'asdfasdfasdfasdf',
         'astrant82',
         'awici',
         'back4osm',
         'bahnpirat',
         'baradhili',
         'batou',
         'beldin',
         'benshaw',
         'bilbster',
         'blebo',
         'blinken',
         'bluedragon',
         'bob-techniq',
         'bob64',
         'bonnydog',
         'botdidier2020',
         'brainwad',
         'browny_au',
         'busdriver12',
         'busybeexp',
         'cainechennatt',
         'calfarome',
         'cambalam',
         'cambodia',
         'cameron',
         'cameronb50',
         'caughtyou',
         'cdei',
         'cgu66',
         'chaesubrot',
         'chainsaw',
         'chdr',
         'chewym',
         'chippy',
         'chrisdennis',
         'christopherlam',
         'chultink',
         'cipherj',
         'colin_090',
         'coops92',
         'crislippi',
         'csdf',
         'csjohnst',
         'cvl',
         'd1g51',
         'dan-dan',
         'dannykath',
         'daveemtb',
         'davidrollinson',
         'davkni',
         'davoque',
         'dawilkieway',
         'dazr87',
         'dcorunna',
         'dcp',
         'dcs',
         'deanjevans',
         'derden',
         'dhx1',
         'dibouski',
         'dmgroom',
         'dmgroom_ct',
         'dnbastian',
         'domecoffees',
         'drgis',
         'dsafjnneijd',
         'dugite-code',
         'dvaey',
         'eBin',
         'ediyes',
         'ekul444',
         'elbatrop',
         'elemist',
         'elysianmapping',
         'emacsen_dwg',
         'emj',
         'epicsauce',
         'erinlee',
         'eross57',
         'etoastw',
         'explorer59',
         'fakeaccount2428',
         'fcremer',
         'flamed',
         'flangegas',
         'flashjones',
         'fluffylucy',
         'foodmapper',
         'freietonne-db',
         'fx99',
         'gb2516',
         'gdal',
         'geltmar',
         'geodreieck4711',
         'gerhard81',
         'gfpzzz',
         'ghoppy',
         'girlinabox',
         'goatcamp',
         'goldfishxyz',
         'gorj',
         'gormur',
         'grendel',
         'grizz123',
         'gromit60',
         'gvmsia',
         'gwillow',
         'hadry',
         'hank knah',
         'harshbutfair',
         'hashil',
         'hclark',
         'helent55',
         'ianbbear',
         'inas',
         'ivyclark',
         'iwantedue',
         'j_c_n',
         'james marcus',
         'jamesbryant',
         'jayb998',
         'jbyway',
         'jinalfoflia',
         'jjduncs',
         'jmlieon',
         'johndpaw',
         'johnrobot',
         'johnsmorgan',
         'jordanbrock',
         'josh64',
         'josho9',
         'jtb1965',
         'juniorwaugh',
         'karitotp',
         'katpatuka',
         'kerosin',
         'kesaph',
         'kevin mattsson',
         'kiemce',
         'kisaa',
         'kristianlawrence',
         'krw',
         'kshackleton',
         'kurtk',
         'lancep',
         'laughton_andrew',
         'lauradavidow',
         'lcmortensen',
         'leahcim',
         'liftarn',
         'locke',
         'loewenthal',
         'loubla',
         'lrhill',
         'mackerski',
         'maggot27',
         'major_eagle_eye',
         'malcolmh',
         'malenki',
         'mani100',
         'mappingisfun2',
         'mark_rat',
         'markus_g',
         'martotomato',
         'matt1legend',
         'matthewsheffield',
         'mawueth',
         'maxerickson',
         'mayad',
         'mccomatt',
         'mdk',
         'mdp553',
         'meihou',
         'melb_guy',
         'mic1',
         'mikedufty',
         'mikesala',
         'mikey_218',
         'milesrd',
         'mischaael',
         'missinglink',
         'mjulius',
         'mkg',
         'mkj',
         'mkuis',
         'modellerau',
         'morb_au',
         'morpheus_ws',
         'mos6510',
         'mparry',
         'mrpulley',
         'mtholen',
         'nailsub',
         'narazarth',
         'nhawk',
         'nikhilprabhakar',
         'njd27',
         'nm7s9',
         'northernNed',
         "o'cholio",
         'oldenburg69',
         'om3g4',
         'one4all05',
         'orbut',
         'orderinchaos',
         'orion',
         'osmfd',
         'ozhamlet',
         'ozhound',
         'pabs',
         'paulg',
         'paulreidau',
         'pdaemon',
         'petdr',
         'petersfreeman',
         'phonetracks329387',
         'pingoo',
         'pjeaje',
         'plebian',
         'poindexter888',
         'poodle',
         'porjo',
         'pringle',
         'qbabooba',
         'raymond_loo',
         'rbuch703',
         'red5alex',
         'redmeetsblue',
         'reodge',
         'resistance',
         'revert_au',
         'richard worl',
         'robandwend',
         'robbage',
         'robgeb',
         'robisacommonusername',
         'robsyme',
         'roleyscout',
         'romge',
         'rp1220',
         'rroland60',
         'rsbarbosa',
         'rubai',
         'rund',
         'russells',
         'russj79',
         's7209',
         'saaie',
         'salix01',
         'samely',
         'samps',
         'sb9576',
         'scai',
         'scottreed',
         'screenbr',
         'sfox',
         'shinjiman',
         'shravan91',
         'shthed',
         'siege65',
         'simex',
         'simmo',
         'simonkilbane',
         'skinsman',
         'sleeker',
         'smaprs',
         'soko',
         'spatialriq',
         'sperac01',
         'sprocket1597',
         'srividya_c',
         'staffijol',
         'steerage250',
         'stephen_le_page',
         'stephensharpaust',
         'steve91',
         'stuartskinner',
         'supamappa4123',
         'superfriendlyaviator',
         'swannie',
         't-mil',
         'tadanet3',
         'tangoforsyth',
         'tapira',
         'thalass',
         'the Cannington',
         'thedavidthomas',
         'theophrastos',
         'thequickbrown',
         'tianan',
         'tiger',
         'tiger_old',
         'tinnedspicedham',
         'tinom',
         'tixuwuoz',
         'tlaslett',
         'tnreynolds',
         'toffo',
         'tom0485',
         'topstone',
         'tsg20100',
         'tubes41',
         'u14183',
         'uboot',
         'ulfl',
         'ultraBLUE',
         'updater',
         'user_1734',
         'user_5359',
         'user_7568',
         'vanpuk',
         'vkungys',
         'vlemaic',
         'vstm',
         'waosm',
         'watto70',
         'weirdunclebob',
         'werner2101',
         'wheelmap_android',
         'wheelmap_visitor',
         'wiedergaenger',
         'wieland',
         'wildmyron',
         'will2bill',
         'will_map',
         'willhops',
         'wilsonwaters',
         'wintersportler',
         'woodpeck',
         'woodpeck_repair',
         'wtdh',
         'wvdp',
         'xybot',
         'ypid',
         'z-dude',
         'zacmccormick',
         'zagam',
         'zaizone',
         'zeiphon',
         'zibbyc',
         u'\xc5ndrew',
         u'\xc6var Arnfj\xf6r\xf0 Bjarmason'])
    

The below shows an audit the map file to return a list of street names.


```python
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
```

    Ave: 6
    Avenue: 328
    Avenuet: 1
    Beaufort: 1
    Boulevard: 185
    Boulevarde: 23
    Broadway: 2
    Circle: 62
    Circuit: 31
    Close: 129
    Corner: 9
    Court: 304
    Courtyard: 12
    Cove: 18
    Cres: 2
    Crescent: 108
    Cross: 153
    Crossway: 21
    Crs: 1
    CRT: 7
    Crt: 8
    Ct: 2
    Dale: 9
    Drive: 391
    drive: 1
    E/ENT: 3
    E/Ent: 1
    East: 7
    Edge: 8
    Elbow: 55
    Entrance: 153
    ENTRANCE: 1
    Esplanade: 9
    Fairway: 2
    Gap: 14
    Garden: 8
    Gardens: 135
    Gate: 3
    gate: 1
    Gates: 2
    Gelderland: 21
    Grade: 13
    Grange: 1
    Green: 22
    Grove: 87
    Haven: 3
    Heights: 3
    Highgate: 1
    Highway: 89
    Hill: 25
    Lane: 163
    Laneway): 1
    LANEWAY): 1
    Link: 3
    Loop: 29
    Mews: 112
    Morrison: 1
    North: 9
    Oxford: 1
    Parade: 45
    Parkway: 5
    Pass: 48
    Place: 306
    plaza: 1
    Promenade: 2
    Quarry: 10
    Quays: 1
    Ramble: 13
    Rd: 13
    RD: 14
    Retreat: 74
    Ridgeway: 19
    Rise: 98
    Road: 936
    Road,: 1
    Sava: 6
    Square: 54
    St: 20
    ST: 10
    st: 1
    St): 1
    Street: 1203
    Tce: 1
    Terrace: 96
    Terriace: 1
    Trail: 12
    Turn: 3
    University: 16
    Vale: 32
    View: 35
    Vista: 1
    W/ENT: 3
    WA: 1
    Way: 399
    WAY: 11
    West: 12
    Wharf: 1
    None
    

####Encountered Problems

A number of street name abbreviations and errors were identified from the street name audit. In order to correct these for consistency, a list of expected street names were prepared and checked against. All street names which failed to match against the expected list were replaced with proposed correct names. A list of the identified street name errors and proposed changes are shown below.


```python
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
```

    TILLIA CRT => Tillia Court
    POPLAR CRT => Poplar Court
    SORREL CRT => Sorrel Court
    Barrow Cres => Barrow Crescent
    Hero Cres => Hero Crescent
    Fitzgerald St (corner View St) => Fitzgerald Street
    Scarborough Beach Rd => Scarborough Beach Road
    Morilla Rd => Morilla Road
    Rockeby Rd => Rockeby Road
    Runyon Rd => Runyon Road
    Cypress Rd => Cypress Road
    Reynolds Rd => Reynolds Road
    TARATA WY E/ENT (LANEWAY) => Tarata Way
    Starling st => Starling Street
    Boas Avenuet => Boas Avenue
    Beaufort St WA => Beaufort Street Way
    Beasley Road, => Beasley Road
    CYPRESS RD => Cypress Road
    REYNOLDS RD => Reynolds Road
    TARATA WY E/ENT => Tarata Way
    TARATA WAY E/ENT => Tarata Way
    Edjudina gate => Edjudina Gate
    Bradshaw Crs => Bradshaw Cross
    TARATA WAY SW ENTRANCE => Tarata Way
    Tillia Crt => Tillia Court
    Sorrel Crt => Sorrel Court
    Hay St => Hay Street
    William St => William Street
    Hill St => Hill Street
    Foundry St => Foundry Street
    Newcastle St => Newcastle Street
    Fitzgerald St => Fitzgerald Street
    Hicks St => Hicks Street
    CARISSA WAY => Carissa Way
    LINDEN WAY => Linden Way
    E Linden Way (In Laneway) => Linden Way
    St Georges Terriace => Street Georges Terrace
    Waterford plaza => Waterford Plaza
    TARATA WY W/ENT => Tarata Way
    Elderberry drive => Elderberry Drive
    HICKS ST => Hicks Street
    Tarata Wy E/Ent => Tarata Way
    Hobsons Ave => Hobsons Avenue
    Wordsworth Ave => Wordsworth Avenue
    Albion Ave => Albion Avenue
    Parmelia Ave => Parmelia Avenue
    Frobisher Ave => Frobisher Avenue
    St Georges Tce => Street Georges Terrace
    O'Kane Ct => O'kane Court
    Magazine Ct => Magazine Court
    

A number of postal code errors were also found within the original dataset. Each postcode was checked against a correct range (6000 to 6999), with errors replaced with a default code of 6000. Again, a list of the identified incorrect postal codes and proposed changes are shown below.


```python
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
```

    WA 6003 => 6000
    1 => 6000
    WA 6157 => 6000
    2 => 6000
    WA 6156 => 6000
    6 => 6000
    WA 6069 => 6000
    1 => 6000
    WA  6051 => 6000
    1 => 6000
    WA 6062 => 6000
    1 => 6000
    WA 6061 => 6000
    1 => 6000
    WA 6012 => 6000
    2 => 6000
    WA 6111 => 6000
    1 => 6000
    

####Creating the .json map file

Check first five entries to see if data matches what is expected.


```python
pprint.pprint(data[0:5])
```

    [{'created': {'changeset': '12341071',
                  'timestamp': '2012-07-19T17:00:36Z',
                  'uid': '722137',
                  'user': 'OSMF Redaction Account',
                  'version': '9'},
      'id': '2306306',
      'pos': [-32.0388963, 115.7735345],
      'type': 'node'},
     {'created': {'changeset': '12548730',
                  'timestamp': '2012-07-30T14:14:36Z',
                  'uid': '142807',
                  'user': 'SDavies',
                  'version': '3'},
      'id': '21390176',
      'pos': [-31.9624823, 115.9130943],
      'type': 'node'},
     {'created': {'changeset': '12543711',
                  'timestamp': '2012-07-30T06:41:54Z',
                  'uid': '189263',
                  'user': 'wildmyron',
                  'version': '3'},
      'id': '21390184',
      'pos': [-31.9566591, 115.9019806],
      'type': 'node'},
     {'created': {'changeset': '12543711',
                  'timestamp': '2012-07-30T06:41:54Z',
                  'uid': '189263',
                  'user': 'wildmyron',
                  'version': '4'},
      'id': '21390189',
      'pos': [-31.9550943, 115.8999843],
      'type': 'node'},
     {'created': {'changeset': '12543711',
                  'timestamp': '2012-07-30T06:43:33Z',
                  'uid': '189263',
                  'user': 'wildmyron',
                  'version': '3'},
      'id': '21390190',
      'pos': [-31.9545536, 115.8990236],
      'type': 'node'}]
    

###4.0 Data Exploration

####Load data into MongoDB instance


```python
from pymongo import MongoClient
#from data import *

def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db


db = get_db('test')
#data = process_map(osmfilenm, True)

[db.perth.insert(e) for e in data]
```

    C:\Anaconda\lib\site-packages\ipykernel\__main__.py:13: DeprecationWarning: insert is deprecated. Use insert_one or insert_many instead.
    




    [ObjectId('55ed6f634c859c4d50e89cba'),
     ObjectId('55ed6f634c859c4d50e89cbb'),
     ObjectId('55ed6f634c859c4d50e89cbc'),
     ObjectId('55ed6f634c859c4d50e89cbd'),
     ObjectId('55ed6f634c859c4d50e89cbe'),
     ObjectId('55ed6f634c859c4d50e89cbf'),
     ObjectId('55ed6f634c859c4d50e89cc0'),
     ObjectId('55ed6f634c859c4d50e89cc1'),
     ObjectId('55ed6f634c859c4d50e89cc2'),
     ObjectId('55ed6f634c859c4d50e89cc3'),
     ObjectId('55ed6f634c859c4d50e89cc4'),
     ObjectId('55ed6f634c859c4d50e89cc5'),
     ObjectId('55ed6f634c859c4d50e89cc6'),
     ObjectId('55ed6f634c859c4d50e89cc7'),
     ObjectId('55ed6f634c859c4d50e89cc8'),
     ObjectId('55ed6f634c859c4d50e89cc9'),
     ObjectId('55ed6f634c859c4d50e89cca'),
     ObjectId('55ed6f634c859c4d50e89ccb'),
     ObjectId('55ed6f634c859c4d50e89ccc'),
     ObjectId('55ed6f634c859c4d50e89ccd'),
     ObjectId('55ed6f634c859c4d50e89cce'),
     ObjectId('55ed6f634c859c4d50e89ccf'),
     ObjectId('55ed6f634c859c4d50e89cd0'),
     ObjectId('55ed6f634c859c4d50e89cd1'),
     ObjectId('55ed6f634c859c4d50e89cd2'),
     ObjectId('55ed6f634c859c4d50e89cd3'),
     ObjectId('55ed6f634c859c4d50e89cd4'),
     ObjectId('55ed6f634c859c4d50e89cd5'),
     ObjectId('55ed6f634c859c4d50e89cd6'),
     ObjectId('55ed6f634c859c4d50e89cd7'),
     ObjectId('55ed6f634c859c4d50e89cd8'),
     ObjectId('55ed6f634c859c4d50e89cd9'),
     ObjectId('55ed6f634c859c4d50e89cda'),
     ObjectId('55ed6f634c859c4d50e89cdb'),
     ObjectId('55ed6f634c859c4d50e89cdc'),
     ObjectId('55ed6f634c859c4d50e89cdd'),
     ObjectId('55ed6f634c859c4d50e89cde'),
     ObjectId('55ed6f634c859c4d50e89cdf'),
     ObjectId('55ed6f634c859c4d50e89ce0'),
     ObjectId('55ed6f634c859c4d50e89ce1'),
     ObjectId('55ed6f634c859c4d50e89ce2'),
     ObjectId('55ed6f634c859c4d50e89ce3'),
     ObjectId('55ed6f634c859c4d50e89ce4'),
     ObjectId('55ed6f634c859c4d50e89ce5'),
     ObjectId('55ed6f634c859c4d50e89ce6'),
     ObjectId('55ed6f634c859c4d50e89ce7'),
     ObjectId('55ed6f634c859c4d50e89ce8'),
     ObjectId('55ed6f634c859c4d50e89ce9'),
     ObjectId('55ed6f634c859c4d50e89cea'),
     ObjectId('55ed6f634c859c4d50e89ceb'),
     ObjectId('55ed6f634c859c4d50e89cec'),
     ObjectId('55ed6f634c859c4d50e89ced'),
     ObjectId('55ed6f634c859c4d50e89cee'),
     ObjectId('55ed6f634c859c4d50e89cef'),
     ObjectId('55ed6f634c859c4d50e89cf0'),
     ObjectId('55ed6f634c859c4d50e89cf1'),
     ObjectId('55ed6f634c859c4d50e89cf2'),
     ObjectId('55ed6f634c859c4d50e89cf3'),
     ObjectId('55ed6f634c859c4d50e89cf4'),
     ObjectId('55ed6f634c859c4d50e89cf5'),
     ObjectId('55ed6f634c859c4d50e89cf6'),
     ObjectId('55ed6f634c859c4d50e89cf7'),
     ObjectId('55ed6f634c859c4d50e89cf8'),
     ObjectId('55ed6f634c859c4d50e89cf9'),
     ObjectId('55ed6f634c859c4d50e89cfa'),
     ObjectId('55ed6f634c859c4d50e89cfb'),
     ObjectId('55ed6f634c859c4d50e89cfc'),
     ObjectId('55ed6f634c859c4d50e89cfd'),
     ObjectId('55ed6f634c859c4d50e89cfe'),
     ObjectId('55ed6f634c859c4d50e89cff'),
     ObjectId('55ed6f634c859c4d50e89d00'),
     ObjectId('55ed6f634c859c4d50e89d01'),
     ObjectId('55ed6f634c859c4d50e89d02'),
     ObjectId('55ed6f634c859c4d50e89d03'),
     ObjectId('55ed6f634c859c4d50e89d04'),
     ObjectId('55ed6f634c859c4d50e89d05'),
     ObjectId('55ed6f634c859c4d50e89d06'),
     ObjectId('55ed6f634c859c4d50e89d07'),
     ObjectId('55ed6f634c859c4d50e89d08'),
     ObjectId('55ed6f634c859c4d50e89d09'),
     ObjectId('55ed6f634c859c4d50e89d0a'),
     ObjectId('55ed6f634c859c4d50e89d0b'),
     ObjectId('55ed6f634c859c4d50e89d0c'),
     ObjectId('55ed6f634c859c4d50e89d0d'),
     ObjectId('55ed6f634c859c4d50e89d0e'),
     ObjectId('55ed6f634c859c4d50e89d0f'),
     ObjectId('55ed6f634c859c4d50e89d10'),
     ObjectId('55ed6f634c859c4d50e89d11'),
     ObjectId('55ed6f634c859c4d50e89d12'),
     ObjectId('55ed6f634c859c4d50e89d13'),
     ObjectId('55ed6f634c859c4d50e89d14'),
     ObjectId('55ed6f634c859c4d50e89d15'),
     ObjectId('55ed6f634c859c4d50e89d16'),
     ObjectId('55ed6f634c859c4d50e89d17'),
     ObjectId('55ed6f634c859c4d50e89d18'),
     ObjectId('55ed6f634c859c4d50e89d19'),
     ObjectId('55ed6f634c859c4d50e89d1a'),
     ObjectId('55ed6f634c859c4d50e89d1b'),
     ObjectId('55ed6f634c859c4d50e89d1c'),
     ObjectId('55ed6f634c859c4d50e89d1d'),
     ObjectId('55ed6f634c859c4d50e89d1e'),
     ObjectId('55ed6f634c859c4d50e89d1f'),
     ObjectId('55ed6f634c859c4d50e89d20'),
     ObjectId('55ed6f634c859c4d50e89d21'),
     ObjectId('55ed6f634c859c4d50e89d22'),
     ObjectId('55ed6f634c859c4d50e89d23'),
     ObjectId('55ed6f634c859c4d50e89d24'),
     ObjectId('55ed6f634c859c4d50e89d25'),
     ObjectId('55ed6f634c859c4d50e89d26'),
     ObjectId('55ed6f634c859c4d50e89d27'),
     ObjectId('55ed6f634c859c4d50e89d28'),
     ObjectId('55ed6f634c859c4d50e89d29'),
     ObjectId('55ed6f634c859c4d50e89d2a'),
     ObjectId('55ed6f634c859c4d50e89d2b'),
     ObjectId('55ed6f634c859c4d50e89d2c'),
     ObjectId('55ed6f634c859c4d50e89d2d'),
     ObjectId('55ed6f634c859c4d50e89d2e'),
     ObjectId('55ed6f634c859c4d50e89d2f'),
     ObjectId('55ed6f634c859c4d50e89d30'),
     ObjectId('55ed6f634c859c4d50e89d31'),
     ObjectId('55ed6f634c859c4d50e89d32'),
     ObjectId('55ed6f634c859c4d50e89d33'),
     ObjectId('55ed6f634c859c4d50e89d34'),
     ObjectId('55ed6f634c859c4d50e89d35'),
     ObjectId('55ed6f634c859c4d50e89d36'),
     ObjectId('55ed6f634c859c4d50e89d37'),
     ObjectId('55ed6f634c859c4d50e89d38'),
     ObjectId('55ed6f634c859c4d50e89d39'),
     ObjectId('55ed6f634c859c4d50e89d3a'),
     ObjectId('55ed6f634c859c4d50e89d3b'),
     ObjectId('55ed6f634c859c4d50e89d3c'),
     ObjectId('55ed6f634c859c4d50e89d3d'),
     ObjectId('55ed6f634c859c4d50e89d3e'),
     ObjectId('55ed6f634c859c4d50e89d3f'),
     ObjectId('55ed6f634c859c4d50e89d40'),
     ObjectId('55ed6f634c859c4d50e89d41'),
     ObjectId('55ed6f634c859c4d50e89d42'),
     ObjectId('55ed6f634c859c4d50e89d43'),
     ObjectId('55ed6f634c859c4d50e89d44'),
     ObjectId('55ed6f634c859c4d50e89d45'),
     ObjectId('55ed6f634c859c4d50e89d46'),
     ObjectId('55ed6f634c859c4d50e89d47'),
     ObjectId('55ed6f634c859c4d50e89d48'),
     ObjectId('55ed6f634c859c4d50e89d49'),
     ObjectId('55ed6f634c859c4d50e89d4a'),
     ObjectId('55ed6f634c859c4d50e89d4b'),
     ObjectId('55ed6f634c859c4d50e89d4c'),
     ObjectId('55ed6f634c859c4d50e89d4d'),
     ObjectId('55ed6f634c859c4d50e89d4e'),
     ObjectId('55ed6f634c859c4d50e89d4f'),
     ObjectId('55ed6f634c859c4d50e89d50'),
     ObjectId('55ed6f634c859c4d50e89d51'),
     ObjectId('55ed6f634c859c4d50e89d52'),
     ObjectId('55ed6f634c859c4d50e89d53'),
     ObjectId('55ed6f634c859c4d50e89d54'),
     ObjectId('55ed6f634c859c4d50e89d55'),
     ObjectId('55ed6f634c859c4d50e89d56'),
     ObjectId('55ed6f634c859c4d50e89d57'),
     ObjectId('55ed6f634c859c4d50e89d58'),
     ObjectId('55ed6f634c859c4d50e89d59'),
     ObjectId('55ed6f634c859c4d50e89d5a'),
     ObjectId('55ed6f634c859c4d50e89d5b'),
     ObjectId('55ed6f634c859c4d50e89d5c'),
     ObjectId('55ed6f634c859c4d50e89d5d'),
     ObjectId('55ed6f634c859c4d50e89d5e'),
     ObjectId('55ed6f634c859c4d50e89d5f'),
     ObjectId('55ed6f634c859c4d50e89d60'),
     ObjectId('55ed6f634c859c4d50e89d61'),
     ObjectId('55ed6f634c859c4d50e89d62'),
     ObjectId('55ed6f634c859c4d50e89d63'),
     ObjectId('55ed6f634c859c4d50e89d64'),
     ObjectId('55ed6f634c859c4d50e89d65'),
     ObjectId('55ed6f634c859c4d50e89d66'),
     ObjectId('55ed6f634c859c4d50e89d67'),
     ObjectId('55ed6f634c859c4d50e89d68'),
     ObjectId('55ed6f634c859c4d50e89d69'),
     ObjectId('55ed6f634c859c4d50e89d6a'),
     ObjectId('55ed6f634c859c4d50e89d6b'),
     ObjectId('55ed6f634c859c4d50e89d6c'),
     ObjectId('55ed6f634c859c4d50e89d6d'),
     ObjectId('55ed6f634c859c4d50e89d6e'),
     ObjectId('55ed6f634c859c4d50e89d6f'),
     ObjectId('55ed6f634c859c4d50e89d70'),
     ObjectId('55ed6f634c859c4d50e89d71'),
     ObjectId('55ed6f634c859c4d50e89d72'),
     ObjectId('55ed6f634c859c4d50e89d73'),
     ObjectId('55ed6f634c859c4d50e89d74'),
     ObjectId('55ed6f634c859c4d50e89d75'),
     ObjectId('55ed6f634c859c4d50e89d76'),
     ObjectId('55ed6f634c859c4d50e89d77'),
     ObjectId('55ed6f634c859c4d50e89d78'),
     ObjectId('55ed6f634c859c4d50e89d79'),
     ObjectId('55ed6f634c859c4d50e89d7a'),
     ObjectId('55ed6f634c859c4d50e89d7b'),
     ObjectId('55ed6f634c859c4d50e89d7c'),
     ObjectId('55ed6f634c859c4d50e89d7d'),
     ObjectId('55ed6f634c859c4d50e89d7e'),
     ObjectId('55ed6f634c859c4d50e89d7f'),
     ObjectId('55ed6f634c859c4d50e89d80'),
     ObjectId('55ed6f634c859c4d50e89d81'),
     ObjectId('55ed6f634c859c4d50e89d82'),
     ObjectId('55ed6f634c859c4d50e89d83'),
     ObjectId('55ed6f634c859c4d50e89d84'),
     ObjectId('55ed6f634c859c4d50e89d85'),
     ObjectId('55ed6f634c859c4d50e89d86'),
     ObjectId('55ed6f634c859c4d50e89d87'),
     ObjectId('55ed6f634c859c4d50e89d88'),
     ObjectId('55ed6f634c859c4d50e89d89'),
     ObjectId('55ed6f634c859c4d50e89d8a'),
     ObjectId('55ed6f634c859c4d50e89d8b'),
     ObjectId('55ed6f634c859c4d50e89d8c'),
     ObjectId('55ed6f634c859c4d50e89d8d'),
     ObjectId('55ed6f634c859c4d50e89d8e'),
     ObjectId('55ed6f634c859c4d50e89d8f'),
     ObjectId('55ed6f634c859c4d50e89d90'),
     ObjectId('55ed6f634c859c4d50e89d91'),
     ObjectId('55ed6f634c859c4d50e89d92'),
     ObjectId('55ed6f634c859c4d50e89d93'),
     ObjectId('55ed6f634c859c4d50e89d94'),
     ObjectId('55ed6f634c859c4d50e89d95'),
     ObjectId('55ed6f634c859c4d50e89d96'),
     ObjectId('55ed6f634c859c4d50e89d97'),
     ObjectId('55ed6f634c859c4d50e89d98'),
     ObjectId('55ed6f634c859c4d50e89d99'),
     ObjectId('55ed6f634c859c4d50e89d9a'),
     ObjectId('55ed6f634c859c4d50e89d9b'),
     ObjectId('55ed6f634c859c4d50e89d9c'),
     ObjectId('55ed6f634c859c4d50e89d9d'),
     ObjectId('55ed6f634c859c4d50e89d9e'),
     ObjectId('55ed6f634c859c4d50e89d9f'),
     ObjectId('55ed6f634c859c4d50e89da0'),
     ObjectId('55ed6f634c859c4d50e89da1'),
     ObjectId('55ed6f634c859c4d50e89da2'),
     ObjectId('55ed6f634c859c4d50e89da3'),
     ObjectId('55ed6f634c859c4d50e89da4'),
     ObjectId('55ed6f634c859c4d50e89da5'),
     ObjectId('55ed6f634c859c4d50e89da6'),
     ObjectId('55ed6f634c859c4d50e89da7'),
     ObjectId('55ed6f634c859c4d50e89da8'),
     ObjectId('55ed6f634c859c4d50e89da9'),
     ObjectId('55ed6f634c859c4d50e89daa'),
     ObjectId('55ed6f634c859c4d50e89dab'),
     ObjectId('55ed6f634c859c4d50e89dac'),
     ObjectId('55ed6f634c859c4d50e89dad'),
     ObjectId('55ed6f634c859c4d50e89dae'),
     ObjectId('55ed6f634c859c4d50e89daf'),
     ObjectId('55ed6f634c859c4d50e89db0'),
     ObjectId('55ed6f634c859c4d50e89db1'),
     ObjectId('55ed6f634c859c4d50e89db2'),
     ObjectId('55ed6f634c859c4d50e89db3'),
     ObjectId('55ed6f634c859c4d50e89db4'),
     ObjectId('55ed6f634c859c4d50e89db5'),
     ObjectId('55ed6f634c859c4d50e89db6'),
     ObjectId('55ed6f634c859c4d50e89db7'),
     ObjectId('55ed6f634c859c4d50e89db8'),
     ObjectId('55ed6f634c859c4d50e89db9'),
     ObjectId('55ed6f634c859c4d50e89dba'),
     ObjectId('55ed6f634c859c4d50e89dbb'),
     ObjectId('55ed6f634c859c4d50e89dbc'),
     ObjectId('55ed6f634c859c4d50e89dbd'),
     ObjectId('55ed6f634c859c4d50e89dbe'),
     ObjectId('55ed6f634c859c4d50e89dbf'),
     ObjectId('55ed6f634c859c4d50e89dc0'),
     ObjectId('55ed6f634c859c4d50e89dc1'),
     ObjectId('55ed6f634c859c4d50e89dc2'),
     ObjectId('55ed6f634c859c4d50e89dc3'),
     ObjectId('55ed6f634c859c4d50e89dc4'),
     ObjectId('55ed6f634c859c4d50e89dc5'),
     ObjectId('55ed6f634c859c4d50e89dc6'),
     ObjectId('55ed6f634c859c4d50e89dc7'),
     ObjectId('55ed6f634c859c4d50e89dc8'),
     ObjectId('55ed6f634c859c4d50e89dc9'),
     ObjectId('55ed6f634c859c4d50e89dca'),
     ObjectId('55ed6f634c859c4d50e89dcb'),
     ObjectId('55ed6f634c859c4d50e89dcc'),
     ObjectId('55ed6f634c859c4d50e89dcd'),
     ObjectId('55ed6f634c859c4d50e89dce'),
     ObjectId('55ed6f634c859c4d50e89dcf'),
     ObjectId('55ed6f634c859c4d50e89dd0'),
     ObjectId('55ed6f634c859c4d50e89dd1'),
     ObjectId('55ed6f634c859c4d50e89dd2'),
     ObjectId('55ed6f634c859c4d50e89dd3'),
     ObjectId('55ed6f634c859c4d50e89dd4'),
     ObjectId('55ed6f634c859c4d50e89dd5'),
     ObjectId('55ed6f634c859c4d50e89dd6'),
     ObjectId('55ed6f634c859c4d50e89dd7'),
     ObjectId('55ed6f634c859c4d50e89dd8'),
     ObjectId('55ed6f634c859c4d50e89dd9'),
     ObjectId('55ed6f634c859c4d50e89dda'),
     ObjectId('55ed6f634c859c4d50e89ddb'),
     ObjectId('55ed6f634c859c4d50e89ddc'),
     ObjectId('55ed6f634c859c4d50e89ddd'),
     ObjectId('55ed6f634c859c4d50e89dde'),
     ObjectId('55ed6f634c859c4d50e89ddf'),
     ObjectId('55ed6f634c859c4d50e89de0'),
     ObjectId('55ed6f634c859c4d50e89de1'),
     ObjectId('55ed6f634c859c4d50e89de2'),
     ObjectId('55ed6f634c859c4d50e89de3'),
     ObjectId('55ed6f634c859c4d50e89de4'),
     ObjectId('55ed6f634c859c4d50e89de5'),
     ObjectId('55ed6f634c859c4d50e89de6'),
     ObjectId('55ed6f634c859c4d50e89de7'),
     ObjectId('55ed6f634c859c4d50e89de8'),
     ObjectId('55ed6f634c859c4d50e89de9'),
     ObjectId('55ed6f634c859c4d50e89dea'),
     ObjectId('55ed6f634c859c4d50e89deb'),
     ObjectId('55ed6f634c859c4d50e89dec'),
     ObjectId('55ed6f634c859c4d50e89ded'),
     ObjectId('55ed6f634c859c4d50e89dee'),
     ObjectId('55ed6f634c859c4d50e89def'),
     ObjectId('55ed6f634c859c4d50e89df0'),
     ObjectId('55ed6f634c859c4d50e89df1'),
     ObjectId('55ed6f634c859c4d50e89df2'),
     ObjectId('55ed6f634c859c4d50e89df3'),
     ObjectId('55ed6f634c859c4d50e89df4'),
     ObjectId('55ed6f634c859c4d50e89df5'),
     ObjectId('55ed6f634c859c4d50e89df6'),
     ObjectId('55ed6f634c859c4d50e89df7'),
     ObjectId('55ed6f634c859c4d50e89df8'),
     ObjectId('55ed6f634c859c4d50e89df9'),
     ObjectId('55ed6f634c859c4d50e89dfa'),
     ObjectId('55ed6f634c859c4d50e89dfb'),
     ObjectId('55ed6f634c859c4d50e89dfc'),
     ObjectId('55ed6f634c859c4d50e89dfd'),
     ObjectId('55ed6f634c859c4d50e89dfe'),
     ObjectId('55ed6f634c859c4d50e89dff'),
     ObjectId('55ed6f634c859c4d50e89e00'),
     ObjectId('55ed6f634c859c4d50e89e01'),
     ObjectId('55ed6f634c859c4d50e89e02'),
     ObjectId('55ed6f634c859c4d50e89e03'),
     ObjectId('55ed6f634c859c4d50e89e04'),
     ObjectId('55ed6f634c859c4d50e89e05'),
     ObjectId('55ed6f634c859c4d50e89e06'),
     ObjectId('55ed6f634c859c4d50e89e07'),
     ObjectId('55ed6f634c859c4d50e89e08'),
     ObjectId('55ed6f634c859c4d50e89e09'),
     ObjectId('55ed6f634c859c4d50e89e0a'),
     ObjectId('55ed6f634c859c4d50e89e0b'),
     ObjectId('55ed6f634c859c4d50e89e0c'),
     ObjectId('55ed6f634c859c4d50e89e0d'),
     ObjectId('55ed6f634c859c4d50e89e0e'),
     ObjectId('55ed6f634c859c4d50e89e0f'),
     ObjectId('55ed6f634c859c4d50e89e10'),
     ObjectId('55ed6f634c859c4d50e89e11'),
     ObjectId('55ed6f634c859c4d50e89e12'),
     ObjectId('55ed6f634c859c4d50e89e13'),
     ObjectId('55ed6f634c859c4d50e89e14'),
     ObjectId('55ed6f634c859c4d50e89e15'),
     ObjectId('55ed6f634c859c4d50e89e16'),
     ObjectId('55ed6f634c859c4d50e89e17'),
     ObjectId('55ed6f634c859c4d50e89e18'),
     ObjectId('55ed6f634c859c4d50e89e19'),
     ObjectId('55ed6f634c859c4d50e89e1a'),
     ObjectId('55ed6f634c859c4d50e89e1b'),
     ObjectId('55ed6f634c859c4d50e89e1c'),
     ObjectId('55ed6f634c859c4d50e89e1d'),
     ObjectId('55ed6f634c859c4d50e89e1e'),
     ObjectId('55ed6f634c859c4d50e89e1f'),
     ObjectId('55ed6f634c859c4d50e89e20'),
     ObjectId('55ed6f634c859c4d50e89e21'),
     ObjectId('55ed6f634c859c4d50e89e22'),
     ObjectId('55ed6f634c859c4d50e89e23'),
     ObjectId('55ed6f634c859c4d50e89e24'),
     ObjectId('55ed6f634c859c4d50e89e25'),
     ObjectId('55ed6f634c859c4d50e89e26'),
     ObjectId('55ed6f634c859c4d50e89e27'),
     ObjectId('55ed6f634c859c4d50e89e28'),
     ObjectId('55ed6f634c859c4d50e89e29'),
     ObjectId('55ed6f634c859c4d50e89e2a'),
     ObjectId('55ed6f634c859c4d50e89e2b'),
     ObjectId('55ed6f634c859c4d50e89e2c'),
     ObjectId('55ed6f634c859c4d50e89e2d'),
     ObjectId('55ed6f634c859c4d50e89e2e'),
     ObjectId('55ed6f634c859c4d50e89e2f'),
     ObjectId('55ed6f634c859c4d50e89e30'),
     ObjectId('55ed6f634c859c4d50e89e31'),
     ObjectId('55ed6f634c859c4d50e89e32'),
     ObjectId('55ed6f634c859c4d50e89e33'),
     ObjectId('55ed6f634c859c4d50e89e34'),
     ObjectId('55ed6f634c859c4d50e89e35'),
     ObjectId('55ed6f634c859c4d50e89e36'),
     ObjectId('55ed6f634c859c4d50e89e37'),
     ObjectId('55ed6f634c859c4d50e89e38'),
     ObjectId('55ed6f634c859c4d50e89e39'),
     ObjectId('55ed6f634c859c4d50e89e3a'),
     ObjectId('55ed6f634c859c4d50e89e3b'),
     ObjectId('55ed6f634c859c4d50e89e3c'),
     ObjectId('55ed6f634c859c4d50e89e3d'),
     ObjectId('55ed6f634c859c4d50e89e3e'),
     ObjectId('55ed6f634c859c4d50e89e3f'),
     ObjectId('55ed6f634c859c4d50e89e40'),
     ObjectId('55ed6f634c859c4d50e89e41'),
     ObjectId('55ed6f634c859c4d50e89e42'),
     ObjectId('55ed6f634c859c4d50e89e43'),
     ObjectId('55ed6f634c859c4d50e89e44'),
     ObjectId('55ed6f634c859c4d50e89e45'),
     ObjectId('55ed6f634c859c4d50e89e46'),
     ObjectId('55ed6f634c859c4d50e89e47'),
     ObjectId('55ed6f634c859c4d50e89e48'),
     ObjectId('55ed6f634c859c4d50e89e49'),
     ObjectId('55ed6f634c859c4d50e89e4a'),
     ObjectId('55ed6f634c859c4d50e89e4b'),
     ObjectId('55ed6f634c859c4d50e89e4c'),
     ObjectId('55ed6f634c859c4d50e89e4d'),
     ObjectId('55ed6f634c859c4d50e89e4e'),
     ObjectId('55ed6f634c859c4d50e89e4f'),
     ObjectId('55ed6f634c859c4d50e89e50'),
     ObjectId('55ed6f634c859c4d50e89e51'),
     ObjectId('55ed6f634c859c4d50e89e52'),
     ObjectId('55ed6f634c859c4d50e89e53'),
     ObjectId('55ed6f634c859c4d50e89e54'),
     ObjectId('55ed6f634c859c4d50e89e55'),
     ObjectId('55ed6f634c859c4d50e89e56'),
     ObjectId('55ed6f634c859c4d50e89e57'),
     ObjectId('55ed6f634c859c4d50e89e58'),
     ObjectId('55ed6f634c859c4d50e89e59'),
     ObjectId('55ed6f634c859c4d50e89e5a'),
     ObjectId('55ed6f634c859c4d50e89e5b'),
     ObjectId('55ed6f634c859c4d50e89e5c'),
     ObjectId('55ed6f634c859c4d50e89e5d'),
     ObjectId('55ed6f634c859c4d50e89e5e'),
     ObjectId('55ed6f634c859c4d50e89e5f'),
     ObjectId('55ed6f634c859c4d50e89e60'),
     ObjectId('55ed6f634c859c4d50e89e61'),
     ObjectId('55ed6f634c859c4d50e89e62'),
     ObjectId('55ed6f634c859c4d50e89e63'),
     ObjectId('55ed6f634c859c4d50e89e64'),
     ObjectId('55ed6f634c859c4d50e89e65'),
     ObjectId('55ed6f634c859c4d50e89e66'),
     ObjectId('55ed6f634c859c4d50e89e67'),
     ObjectId('55ed6f634c859c4d50e89e68'),
     ObjectId('55ed6f634c859c4d50e89e69'),
     ObjectId('55ed6f634c859c4d50e89e6a'),
     ObjectId('55ed6f634c859c4d50e89e6b'),
     ObjectId('55ed6f634c859c4d50e89e6c'),
     ObjectId('55ed6f634c859c4d50e89e6d'),
     ObjectId('55ed6f634c859c4d50e89e6e'),
     ObjectId('55ed6f634c859c4d50e89e6f'),
     ObjectId('55ed6f634c859c4d50e89e70'),
     ObjectId('55ed6f634c859c4d50e89e71'),
     ObjectId('55ed6f634c859c4d50e89e72'),
     ObjectId('55ed6f634c859c4d50e89e73'),
     ObjectId('55ed6f634c859c4d50e89e74'),
     ObjectId('55ed6f634c859c4d50e89e75'),
     ObjectId('55ed6f634c859c4d50e89e76'),
     ObjectId('55ed6f634c859c4d50e89e77'),
     ObjectId('55ed6f634c859c4d50e89e78'),
     ObjectId('55ed6f634c859c4d50e89e79'),
     ObjectId('55ed6f634c859c4d50e89e7a'),
     ObjectId('55ed6f634c859c4d50e89e7b'),
     ObjectId('55ed6f634c859c4d50e89e7c'),
     ObjectId('55ed6f634c859c4d50e89e7d'),
     ObjectId('55ed6f634c859c4d50e89e7e'),
     ObjectId('55ed6f634c859c4d50e89e7f'),
     ObjectId('55ed6f634c859c4d50e89e80'),
     ObjectId('55ed6f634c859c4d50e89e81'),
     ObjectId('55ed6f634c859c4d50e89e82'),
     ObjectId('55ed6f634c859c4d50e89e83'),
     ObjectId('55ed6f634c859c4d50e89e84'),
     ObjectId('55ed6f634c859c4d50e89e85'),
     ObjectId('55ed6f634c859c4d50e89e86'),
     ObjectId('55ed6f634c859c4d50e89e87'),
     ObjectId('55ed6f634c859c4d50e89e88'),
     ObjectId('55ed6f634c859c4d50e89e89'),
     ObjectId('55ed6f634c859c4d50e89e8a'),
     ObjectId('55ed6f634c859c4d50e89e8b'),
     ObjectId('55ed6f634c859c4d50e89e8c'),
     ObjectId('55ed6f634c859c4d50e89e8d'),
     ObjectId('55ed6f634c859c4d50e89e8e'),
     ObjectId('55ed6f634c859c4d50e89e8f'),
     ObjectId('55ed6f634c859c4d50e89e90'),
     ObjectId('55ed6f634c859c4d50e89e91'),
     ObjectId('55ed6f634c859c4d50e89e92'),
     ObjectId('55ed6f634c859c4d50e89e93'),
     ObjectId('55ed6f634c859c4d50e89e94'),
     ObjectId('55ed6f634c859c4d50e89e95'),
     ObjectId('55ed6f634c859c4d50e89e96'),
     ObjectId('55ed6f634c859c4d50e89e97'),
     ObjectId('55ed6f634c859c4d50e89e98'),
     ObjectId('55ed6f634c859c4d50e89e99'),
     ObjectId('55ed6f634c859c4d50e89e9a'),
     ObjectId('55ed6f634c859c4d50e89e9b'),
     ObjectId('55ed6f634c859c4d50e89e9c'),
     ObjectId('55ed6f634c859c4d50e89e9d'),
     ObjectId('55ed6f634c859c4d50e89e9e'),
     ObjectId('55ed6f634c859c4d50e89e9f'),
     ObjectId('55ed6f634c859c4d50e89ea0'),
     ObjectId('55ed6f634c859c4d50e89ea1'),
     ObjectId('55ed6f634c859c4d50e89ea2'),
     ObjectId('55ed6f634c859c4d50e89ea3'),
     ObjectId('55ed6f634c859c4d50e89ea4'),
     ObjectId('55ed6f634c859c4d50e89ea5'),
     ObjectId('55ed6f634c859c4d50e89ea6'),
     ObjectId('55ed6f634c859c4d50e89ea7'),
     ObjectId('55ed6f634c859c4d50e89ea8'),
     ObjectId('55ed6f634c859c4d50e89ea9'),
     ObjectId('55ed6f634c859c4d50e89eaa'),
     ObjectId('55ed6f634c859c4d50e89eab'),
     ObjectId('55ed6f634c859c4d50e89eac'),
     ObjectId('55ed6f634c859c4d50e89ead'),
     ObjectId('55ed6f634c859c4d50e89eae'),
     ObjectId('55ed6f634c859c4d50e89eaf'),
     ObjectId('55ed6f634c859c4d50e89eb0'),
     ObjectId('55ed6f634c859c4d50e89eb1'),
     ObjectId('55ed6f634c859c4d50e89eb2'),
     ObjectId('55ed6f634c859c4d50e89eb3'),
     ObjectId('55ed6f634c859c4d50e89eb4'),
     ObjectId('55ed6f634c859c4d50e89eb5'),
     ObjectId('55ed6f634c859c4d50e89eb6'),
     ObjectId('55ed6f634c859c4d50e89eb7'),
     ObjectId('55ed6f634c859c4d50e89eb8'),
     ObjectId('55ed6f634c859c4d50e89eb9'),
     ObjectId('55ed6f634c859c4d50e89eba'),
     ObjectId('55ed6f634c859c4d50e89ebb'),
     ObjectId('55ed6f634c859c4d50e89ebc'),
     ObjectId('55ed6f634c859c4d50e89ebd'),
     ObjectId('55ed6f634c859c4d50e89ebe'),
     ObjectId('55ed6f634c859c4d50e89ebf'),
     ObjectId('55ed6f634c859c4d50e89ec0'),
     ObjectId('55ed6f634c859c4d50e89ec1'),
     ObjectId('55ed6f634c859c4d50e89ec2'),
     ObjectId('55ed6f634c859c4d50e89ec3'),
     ObjectId('55ed6f634c859c4d50e89ec4'),
     ObjectId('55ed6f634c859c4d50e89ec5'),
     ObjectId('55ed6f634c859c4d50e89ec6'),
     ObjectId('55ed6f634c859c4d50e89ec7'),
     ObjectId('55ed6f634c859c4d50e89ec8'),
     ObjectId('55ed6f634c859c4d50e89ec9'),
     ObjectId('55ed6f634c859c4d50e89eca'),
     ObjectId('55ed6f634c859c4d50e89ecb'),
     ObjectId('55ed6f634c859c4d50e89ecc'),
     ObjectId('55ed6f634c859c4d50e89ecd'),
     ObjectId('55ed6f634c859c4d50e89ece'),
     ObjectId('55ed6f634c859c4d50e89ecf'),
     ObjectId('55ed6f634c859c4d50e89ed0'),
     ObjectId('55ed6f634c859c4d50e89ed1'),
     ObjectId('55ed6f634c859c4d50e89ed2'),
     ObjectId('55ed6f634c859c4d50e89ed3'),
     ObjectId('55ed6f634c859c4d50e89ed4'),
     ObjectId('55ed6f634c859c4d50e89ed5'),
     ObjectId('55ed6f634c859c4d50e89ed6'),
     ObjectId('55ed6f634c859c4d50e89ed7'),
     ObjectId('55ed6f634c859c4d50e89ed8'),
     ObjectId('55ed6f634c859c4d50e89ed9'),
     ObjectId('55ed6f634c859c4d50e89eda'),
     ObjectId('55ed6f634c859c4d50e89edb'),
     ObjectId('55ed6f634c859c4d50e89edc'),
     ObjectId('55ed6f634c859c4d50e89edd'),
     ObjectId('55ed6f634c859c4d50e89ede'),
     ObjectId('55ed6f634c859c4d50e89edf'),
     ObjectId('55ed6f634c859c4d50e89ee0'),
     ObjectId('55ed6f634c859c4d50e89ee1'),
     ObjectId('55ed6f634c859c4d50e89ee2'),
     ObjectId('55ed6f634c859c4d50e89ee3'),
     ObjectId('55ed6f634c859c4d50e89ee4'),
     ObjectId('55ed6f634c859c4d50e89ee5'),
     ObjectId('55ed6f634c859c4d50e89ee6'),
     ObjectId('55ed6f634c859c4d50e89ee7'),
     ObjectId('55ed6f634c859c4d50e89ee8'),
     ObjectId('55ed6f634c859c4d50e89ee9'),
     ObjectId('55ed6f634c859c4d50e89eea'),
     ObjectId('55ed6f634c859c4d50e89eeb'),
     ObjectId('55ed6f634c859c4d50e89eec'),
     ObjectId('55ed6f634c859c4d50e89eed'),
     ObjectId('55ed6f634c859c4d50e89eee'),
     ObjectId('55ed6f634c859c4d50e89eef'),
     ObjectId('55ed6f634c859c4d50e89ef0'),
     ObjectId('55ed6f634c859c4d50e89ef1'),
     ObjectId('55ed6f634c859c4d50e89ef2'),
     ObjectId('55ed6f634c859c4d50e89ef3'),
     ObjectId('55ed6f634c859c4d50e89ef4'),
     ObjectId('55ed6f634c859c4d50e89ef5'),
     ObjectId('55ed6f634c859c4d50e89ef6'),
     ObjectId('55ed6f634c859c4d50e89ef7'),
     ObjectId('55ed6f634c859c4d50e89ef8'),
     ObjectId('55ed6f634c859c4d50e89ef9'),
     ObjectId('55ed6f634c859c4d50e89efa'),
     ObjectId('55ed6f634c859c4d50e89efb'),
     ObjectId('55ed6f634c859c4d50e89efc'),
     ObjectId('55ed6f634c859c4d50e89efd'),
     ObjectId('55ed6f634c859c4d50e89efe'),
     ObjectId('55ed6f634c859c4d50e89eff'),
     ObjectId('55ed6f634c859c4d50e89f00'),
     ObjectId('55ed6f634c859c4d50e89f01'),
     ObjectId('55ed6f634c859c4d50e89f02'),
     ObjectId('55ed6f634c859c4d50e89f03'),
     ObjectId('55ed6f634c859c4d50e89f04'),
     ObjectId('55ed6f634c859c4d50e89f05'),
     ObjectId('55ed6f634c859c4d50e89f06'),
     ObjectId('55ed6f634c859c4d50e89f07'),
     ObjectId('55ed6f634c859c4d50e89f08'),
     ObjectId('55ed6f634c859c4d50e89f09'),
     ObjectId('55ed6f634c859c4d50e89f0a'),
     ObjectId('55ed6f634c859c4d50e89f0b'),
     ObjectId('55ed6f634c859c4d50e89f0c'),
     ObjectId('55ed6f634c859c4d50e89f0d'),
     ObjectId('55ed6f634c859c4d50e89f0e'),
     ObjectId('55ed6f634c859c4d50e89f0f'),
     ObjectId('55ed6f634c859c4d50e89f10'),
     ObjectId('55ed6f634c859c4d50e89f11'),
     ObjectId('55ed6f634c859c4d50e89f12'),
     ObjectId('55ed6f634c859c4d50e89f13'),
     ObjectId('55ed6f634c859c4d50e89f14'),
     ObjectId('55ed6f634c859c4d50e89f15'),
     ObjectId('55ed6f634c859c4d50e89f16'),
     ObjectId('55ed6f634c859c4d50e89f17'),
     ObjectId('55ed6f634c859c4d50e89f18'),
     ObjectId('55ed6f634c859c4d50e89f19'),
     ObjectId('55ed6f634c859c4d50e89f1a'),
     ObjectId('55ed6f634c859c4d50e89f1b'),
     ObjectId('55ed6f634c859c4d50e89f1c'),
     ObjectId('55ed6f634c859c4d50e89f1d'),
     ObjectId('55ed6f634c859c4d50e89f1e'),
     ObjectId('55ed6f634c859c4d50e89f1f'),
     ObjectId('55ed6f634c859c4d50e89f20'),
     ObjectId('55ed6f634c859c4d50e89f21'),
     ObjectId('55ed6f634c859c4d50e89f22'),
     ObjectId('55ed6f634c859c4d50e89f23'),
     ObjectId('55ed6f634c859c4d50e89f24'),
     ObjectId('55ed6f634c859c4d50e89f25'),
     ObjectId('55ed6f634c859c4d50e89f26'),
     ObjectId('55ed6f634c859c4d50e89f27'),
     ObjectId('55ed6f634c859c4d50e89f28'),
     ObjectId('55ed6f634c859c4d50e89f29'),
     ObjectId('55ed6f634c859c4d50e89f2a'),
     ObjectId('55ed6f634c859c4d50e89f2b'),
     ObjectId('55ed6f634c859c4d50e89f2c'),
     ObjectId('55ed6f634c859c4d50e89f2d'),
     ObjectId('55ed6f634c859c4d50e89f2e'),
     ObjectId('55ed6f634c859c4d50e89f2f'),
     ObjectId('55ed6f634c859c4d50e89f30'),
     ObjectId('55ed6f634c859c4d50e89f31'),
     ObjectId('55ed6f634c859c4d50e89f32'),
     ObjectId('55ed6f634c859c4d50e89f33'),
     ObjectId('55ed6f634c859c4d50e89f34'),
     ObjectId('55ed6f634c859c4d50e89f35'),
     ObjectId('55ed6f634c859c4d50e89f36'),
     ObjectId('55ed6f634c859c4d50e89f37'),
     ObjectId('55ed6f634c859c4d50e89f38'),
     ObjectId('55ed6f634c859c4d50e89f39'),
     ObjectId('55ed6f634c859c4d50e89f3a'),
     ObjectId('55ed6f634c859c4d50e89f3b'),
     ObjectId('55ed6f634c859c4d50e89f3c'),
     ObjectId('55ed6f634c859c4d50e89f3d'),
     ObjectId('55ed6f634c859c4d50e89f3e'),
     ObjectId('55ed6f634c859c4d50e89f3f'),
     ObjectId('55ed6f634c859c4d50e89f40'),
     ObjectId('55ed6f634c859c4d50e89f41'),
     ObjectId('55ed6f634c859c4d50e89f42'),
     ObjectId('55ed6f634c859c4d50e89f43'),
     ObjectId('55ed6f634c859c4d50e89f44'),
     ObjectId('55ed6f634c859c4d50e89f45'),
     ObjectId('55ed6f634c859c4d50e89f46'),
     ObjectId('55ed6f634c859c4d50e89f47'),
     ObjectId('55ed6f634c859c4d50e89f48'),
     ObjectId('55ed6f634c859c4d50e89f49'),
     ObjectId('55ed6f634c859c4d50e89f4a'),
     ObjectId('55ed6f634c859c4d50e89f4b'),
     ObjectId('55ed6f634c859c4d50e89f4c'),
     ObjectId('55ed6f634c859c4d50e89f4d'),
     ObjectId('55ed6f634c859c4d50e89f4e'),
     ObjectId('55ed6f634c859c4d50e89f4f'),
     ObjectId('55ed6f634c859c4d50e89f50'),
     ObjectId('55ed6f634c859c4d50e89f51'),
     ObjectId('55ed6f634c859c4d50e89f52'),
     ObjectId('55ed6f634c859c4d50e89f53'),
     ObjectId('55ed6f634c859c4d50e89f54'),
     ObjectId('55ed6f634c859c4d50e89f55'),
     ObjectId('55ed6f634c859c4d50e89f56'),
     ObjectId('55ed6f634c859c4d50e89f57'),
     ObjectId('55ed6f634c859c4d50e89f58'),
     ObjectId('55ed6f634c859c4d50e89f59'),
     ObjectId('55ed6f634c859c4d50e89f5a'),
     ObjectId('55ed6f634c859c4d50e89f5b'),
     ObjectId('55ed6f634c859c4d50e89f5c'),
     ObjectId('55ed6f634c859c4d50e89f5d'),
     ObjectId('55ed6f634c859c4d50e89f5e'),
     ObjectId('55ed6f634c859c4d50e89f5f'),
     ObjectId('55ed6f634c859c4d50e89f60'),
     ObjectId('55ed6f634c859c4d50e89f61'),
     ObjectId('55ed6f634c859c4d50e89f62'),
     ObjectId('55ed6f634c859c4d50e89f63'),
     ObjectId('55ed6f634c859c4d50e89f64'),
     ObjectId('55ed6f634c859c4d50e89f65'),
     ObjectId('55ed6f634c859c4d50e89f66'),
     ObjectId('55ed6f634c859c4d50e89f67'),
     ObjectId('55ed6f634c859c4d50e89f68'),
     ObjectId('55ed6f634c859c4d50e89f69'),
     ObjectId('55ed6f634c859c4d50e89f6a'),
     ObjectId('55ed6f634c859c4d50e89f6b'),
     ObjectId('55ed6f634c859c4d50e89f6c'),
     ObjectId('55ed6f634c859c4d50e89f6d'),
     ObjectId('55ed6f634c859c4d50e89f6e'),
     ObjectId('55ed6f634c859c4d50e89f6f'),
     ObjectId('55ed6f634c859c4d50e89f70'),
     ObjectId('55ed6f634c859c4d50e89f71'),
     ObjectId('55ed6f634c859c4d50e89f72'),
     ObjectId('55ed6f634c859c4d50e89f73'),
     ObjectId('55ed6f634c859c4d50e89f74'),
     ObjectId('55ed6f634c859c4d50e89f75'),
     ObjectId('55ed6f634c859c4d50e89f76'),
     ObjectId('55ed6f634c859c4d50e89f77'),
     ObjectId('55ed6f634c859c4d50e89f78'),
     ObjectId('55ed6f634c859c4d50e89f79'),
     ObjectId('55ed6f634c859c4d50e89f7a'),
     ObjectId('55ed6f634c859c4d50e89f7b'),
     ObjectId('55ed6f634c859c4d50e89f7c'),
     ObjectId('55ed6f634c859c4d50e89f7d'),
     ObjectId('55ed6f634c859c4d50e89f7e'),
     ObjectId('55ed6f634c859c4d50e89f7f'),
     ObjectId('55ed6f634c859c4d50e89f80'),
     ObjectId('55ed6f634c859c4d50e89f81'),
     ObjectId('55ed6f634c859c4d50e89f82'),
     ObjectId('55ed6f634c859c4d50e89f83'),
     ObjectId('55ed6f634c859c4d50e89f84'),
     ObjectId('55ed6f634c859c4d50e89f85'),
     ObjectId('55ed6f634c859c4d50e89f86'),
     ObjectId('55ed6f634c859c4d50e89f87'),
     ObjectId('55ed6f634c859c4d50e89f88'),
     ObjectId('55ed6f634c859c4d50e89f89'),
     ObjectId('55ed6f634c859c4d50e89f8a'),
     ObjectId('55ed6f634c859c4d50e89f8b'),
     ObjectId('55ed6f634c859c4d50e89f8c'),
     ObjectId('55ed6f634c859c4d50e89f8d'),
     ObjectId('55ed6f634c859c4d50e89f8e'),
     ObjectId('55ed6f634c859c4d50e89f8f'),
     ObjectId('55ed6f634c859c4d50e89f90'),
     ObjectId('55ed6f634c859c4d50e89f91'),
     ObjectId('55ed6f634c859c4d50e89f92'),
     ObjectId('55ed6f634c859c4d50e89f93'),
     ObjectId('55ed6f634c859c4d50e89f94'),
     ObjectId('55ed6f634c859c4d50e89f95'),
     ObjectId('55ed6f634c859c4d50e89f96'),
     ObjectId('55ed6f634c859c4d50e89f97'),
     ObjectId('55ed6f634c859c4d50e89f98'),
     ObjectId('55ed6f634c859c4d50e89f99'),
     ObjectId('55ed6f634c859c4d50e89f9a'),
     ObjectId('55ed6f634c859c4d50e89f9b'),
     ObjectId('55ed6f634c859c4d50e89f9c'),
     ObjectId('55ed6f634c859c4d50e89f9d'),
     ObjectId('55ed6f634c859c4d50e89f9e'),
     ObjectId('55ed6f634c859c4d50e89f9f'),
     ObjectId('55ed6f634c859c4d50e89fa0'),
     ObjectId('55ed6f634c859c4d50e89fa1'),
     ObjectId('55ed6f634c859c4d50e89fa2'),
     ObjectId('55ed6f634c859c4d50e89fa3'),
     ObjectId('55ed6f634c859c4d50e89fa4'),
     ObjectId('55ed6f634c859c4d50e89fa5'),
     ObjectId('55ed6f634c859c4d50e89fa6'),
     ObjectId('55ed6f634c859c4d50e89fa7'),
     ObjectId('55ed6f634c859c4d50e89fa8'),
     ObjectId('55ed6f634c859c4d50e89fa9'),
     ObjectId('55ed6f634c859c4d50e89faa'),
     ObjectId('55ed6f634c859c4d50e89fab'),
     ObjectId('55ed6f634c859c4d50e89fac'),
     ObjectId('55ed6f634c859c4d50e89fad'),
     ObjectId('55ed6f634c859c4d50e89fae'),
     ObjectId('55ed6f634c859c4d50e89faf'),
     ObjectId('55ed6f634c859c4d50e89fb0'),
     ObjectId('55ed6f634c859c4d50e89fb1'),
     ObjectId('55ed6f634c859c4d50e89fb2'),
     ObjectId('55ed6f634c859c4d50e89fb3'),
     ObjectId('55ed6f634c859c4d50e89fb4'),
     ObjectId('55ed6f634c859c4d50e89fb5'),
     ObjectId('55ed6f634c859c4d50e89fb6'),
     ObjectId('55ed6f634c859c4d50e89fb7'),
     ObjectId('55ed6f634c859c4d50e89fb8'),
     ObjectId('55ed6f634c859c4d50e89fb9'),
     ObjectId('55ed6f634c859c4d50e89fba'),
     ObjectId('55ed6f634c859c4d50e89fbb'),
     ObjectId('55ed6f634c859c4d50e89fbc'),
     ObjectId('55ed6f634c859c4d50e89fbd'),
     ObjectId('55ed6f634c859c4d50e89fbe'),
     ObjectId('55ed6f634c859c4d50e89fbf'),
     ObjectId('55ed6f634c859c4d50e89fc0'),
     ObjectId('55ed6f634c859c4d50e89fc1'),
     ObjectId('55ed6f634c859c4d50e89fc2'),
     ObjectId('55ed6f634c859c4d50e89fc3'),
     ObjectId('55ed6f634c859c4d50e89fc4'),
     ObjectId('55ed6f634c859c4d50e89fc5'),
     ObjectId('55ed6f634c859c4d50e89fc6'),
     ObjectId('55ed6f634c859c4d50e89fc7'),
     ObjectId('55ed6f634c859c4d50e89fc8'),
     ObjectId('55ed6f634c859c4d50e89fc9'),
     ObjectId('55ed6f634c859c4d50e89fca'),
     ObjectId('55ed6f634c859c4d50e89fcb'),
     ObjectId('55ed6f634c859c4d50e89fcc'),
     ObjectId('55ed6f634c859c4d50e89fcd'),
     ObjectId('55ed6f634c859c4d50e89fce'),
     ObjectId('55ed6f634c859c4d50e89fcf'),
     ObjectId('55ed6f634c859c4d50e89fd0'),
     ObjectId('55ed6f634c859c4d50e89fd1'),
     ObjectId('55ed6f634c859c4d50e89fd2'),
     ObjectId('55ed6f634c859c4d50e89fd3'),
     ObjectId('55ed6f634c859c4d50e89fd4'),
     ObjectId('55ed6f634c859c4d50e89fd5'),
     ObjectId('55ed6f634c859c4d50e89fd6'),
     ObjectId('55ed6f634c859c4d50e89fd7'),
     ObjectId('55ed6f634c859c4d50e89fd8'),
     ObjectId('55ed6f634c859c4d50e89fd9'),
     ObjectId('55ed6f634c859c4d50e89fda'),
     ObjectId('55ed6f634c859c4d50e89fdb'),
     ObjectId('55ed6f634c859c4d50e89fdc'),
     ObjectId('55ed6f634c859c4d50e89fdd'),
     ObjectId('55ed6f634c859c4d50e89fde'),
     ObjectId('55ed6f634c859c4d50e89fdf'),
     ObjectId('55ed6f634c859c4d50e89fe0'),
     ObjectId('55ed6f634c859c4d50e89fe1'),
     ObjectId('55ed6f634c859c4d50e89fe2'),
     ObjectId('55ed6f634c859c4d50e89fe3'),
     ObjectId('55ed6f634c859c4d50e89fe4'),
     ObjectId('55ed6f634c859c4d50e89fe5'),
     ObjectId('55ed6f634c859c4d50e89fe6'),
     ObjectId('55ed6f634c859c4d50e89fe7'),
     ObjectId('55ed6f634c859c4d50e89fe8'),
     ObjectId('55ed6f634c859c4d50e89fe9'),
     ObjectId('55ed6f634c859c4d50e89fea'),
     ObjectId('55ed6f634c859c4d50e89feb'),
     ObjectId('55ed6f634c859c4d50e89fec'),
     ObjectId('55ed6f634c859c4d50e89fed'),
     ObjectId('55ed6f634c859c4d50e89fee'),
     ObjectId('55ed6f634c859c4d50e89fef'),
     ObjectId('55ed6f634c859c4d50e89ff0'),
     ObjectId('55ed6f634c859c4d50e89ff1'),
     ObjectId('55ed6f634c859c4d50e89ff2'),
     ObjectId('55ed6f634c859c4d50e89ff3'),
     ObjectId('55ed6f634c859c4d50e89ff4'),
     ObjectId('55ed6f634c859c4d50e89ff5'),
     ObjectId('55ed6f634c859c4d50e89ff6'),
     ObjectId('55ed6f634c859c4d50e89ff7'),
     ObjectId('55ed6f634c859c4d50e89ff8'),
     ObjectId('55ed6f634c859c4d50e89ff9'),
     ObjectId('55ed6f634c859c4d50e89ffa'),
     ObjectId('55ed6f634c859c4d50e89ffb'),
     ObjectId('55ed6f634c859c4d50e89ffc'),
     ObjectId('55ed6f634c859c4d50e89ffd'),
     ObjectId('55ed6f634c859c4d50e89ffe'),
     ObjectId('55ed6f634c859c4d50e89fff'),
     ObjectId('55ed6f634c859c4d50e8a000'),
     ObjectId('55ed6f634c859c4d50e8a001'),
     ObjectId('55ed6f634c859c4d50e8a002'),
     ObjectId('55ed6f634c859c4d50e8a003'),
     ObjectId('55ed6f634c859c4d50e8a004'),
     ObjectId('55ed6f634c859c4d50e8a005'),
     ObjectId('55ed6f634c859c4d50e8a006'),
     ObjectId('55ed6f634c859c4d50e8a007'),
     ObjectId('55ed6f634c859c4d50e8a008'),
     ObjectId('55ed6f634c859c4d50e8a009'),
     ObjectId('55ed6f634c859c4d50e8a00a'),
     ObjectId('55ed6f634c859c4d50e8a00b'),
     ObjectId('55ed6f634c859c4d50e8a00c'),
     ObjectId('55ed6f634c859c4d50e8a00d'),
     ObjectId('55ed6f634c859c4d50e8a00e'),
     ObjectId('55ed6f634c859c4d50e8a00f'),
     ObjectId('55ed6f634c859c4d50e8a010'),
     ObjectId('55ed6f634c859c4d50e8a011'),
     ObjectId('55ed6f634c859c4d50e8a012'),
     ObjectId('55ed6f634c859c4d50e8a013'),
     ObjectId('55ed6f634c859c4d50e8a014'),
     ObjectId('55ed6f634c859c4d50e8a015'),
     ObjectId('55ed6f634c859c4d50e8a016'),
     ObjectId('55ed6f634c859c4d50e8a017'),
     ObjectId('55ed6f634c859c4d50e8a018'),
     ObjectId('55ed6f634c859c4d50e8a019'),
     ObjectId('55ed6f634c859c4d50e8a01a'),
     ObjectId('55ed6f634c859c4d50e8a01b'),
     ObjectId('55ed6f634c859c4d50e8a01c'),
     ObjectId('55ed6f634c859c4d50e8a01d'),
     ObjectId('55ed6f634c859c4d50e8a01e'),
     ObjectId('55ed6f634c859c4d50e8a01f'),
     ObjectId('55ed6f634c859c4d50e8a020'),
     ObjectId('55ed6f634c859c4d50e8a021'),
     ObjectId('55ed6f634c859c4d50e8a022'),
     ObjectId('55ed6f634c859c4d50e8a023'),
     ObjectId('55ed6f634c859c4d50e8a024'),
     ObjectId('55ed6f634c859c4d50e8a025'),
     ObjectId('55ed6f634c859c4d50e8a026'),
     ObjectId('55ed6f634c859c4d50e8a027'),
     ObjectId('55ed6f634c859c4d50e8a028'),
     ObjectId('55ed6f634c859c4d50e8a029'),
     ObjectId('55ed6f634c859c4d50e8a02a'),
     ObjectId('55ed6f634c859c4d50e8a02b'),
     ObjectId('55ed6f634c859c4d50e8a02c'),
     ObjectId('55ed6f634c859c4d50e8a02d'),
     ObjectId('55ed6f634c859c4d50e8a02e'),
     ObjectId('55ed6f634c859c4d50e8a02f'),
     ObjectId('55ed6f634c859c4d50e8a030'),
     ObjectId('55ed6f634c859c4d50e8a031'),
     ObjectId('55ed6f634c859c4d50e8a032'),
     ObjectId('55ed6f634c859c4d50e8a033'),
     ObjectId('55ed6f634c859c4d50e8a034'),
     ObjectId('55ed6f634c859c4d50e8a035'),
     ObjectId('55ed6f634c859c4d50e8a036'),
     ObjectId('55ed6f634c859c4d50e8a037'),
     ObjectId('55ed6f634c859c4d50e8a038'),
     ObjectId('55ed6f634c859c4d50e8a039'),
     ObjectId('55ed6f634c859c4d50e8a03a'),
     ObjectId('55ed6f634c859c4d50e8a03b'),
     ObjectId('55ed6f634c859c4d50e8a03c'),
     ObjectId('55ed6f634c859c4d50e8a03d'),
     ObjectId('55ed6f634c859c4d50e8a03e'),
     ObjectId('55ed6f634c859c4d50e8a03f'),
     ObjectId('55ed6f634c859c4d50e8a040'),
     ObjectId('55ed6f634c859c4d50e8a041'),
     ObjectId('55ed6f634c859c4d50e8a042'),
     ObjectId('55ed6f634c859c4d50e8a043'),
     ObjectId('55ed6f634c859c4d50e8a044'),
     ObjectId('55ed6f634c859c4d50e8a045'),
     ObjectId('55ed6f634c859c4d50e8a046'),
     ObjectId('55ed6f634c859c4d50e8a047'),
     ObjectId('55ed6f634c859c4d50e8a048'),
     ObjectId('55ed6f634c859c4d50e8a049'),
     ObjectId('55ed6f634c859c4d50e8a04a'),
     ObjectId('55ed6f634c859c4d50e8a04b'),
     ObjectId('55ed6f634c859c4d50e8a04c'),
     ObjectId('55ed6f634c859c4d50e8a04d'),
     ObjectId('55ed6f634c859c4d50e8a04e'),
     ObjectId('55ed6f634c859c4d50e8a04f'),
     ObjectId('55ed6f634c859c4d50e8a050'),
     ObjectId('55ed6f634c859c4d50e8a051'),
     ObjectId('55ed6f634c859c4d50e8a052'),
     ObjectId('55ed6f634c859c4d50e8a053'),
     ObjectId('55ed6f634c859c4d50e8a054'),
     ObjectId('55ed6f634c859c4d50e8a055'),
     ObjectId('55ed6f634c859c4d50e8a056'),
     ObjectId('55ed6f634c859c4d50e8a057'),
     ObjectId('55ed6f634c859c4d50e8a058'),
     ObjectId('55ed6f634c859c4d50e8a059'),
     ObjectId('55ed6f634c859c4d50e8a05a'),
     ObjectId('55ed6f634c859c4d50e8a05b'),
     ObjectId('55ed6f634c859c4d50e8a05c'),
     ObjectId('55ed6f634c859c4d50e8a05d'),
     ObjectId('55ed6f634c859c4d50e8a05e'),
     ObjectId('55ed6f634c859c4d50e8a05f'),
     ObjectId('55ed6f634c859c4d50e8a060'),
     ObjectId('55ed6f634c859c4d50e8a061'),
     ObjectId('55ed6f634c859c4d50e8a062'),
     ObjectId('55ed6f634c859c4d50e8a063'),
     ObjectId('55ed6f634c859c4d50e8a064'),
     ObjectId('55ed6f634c859c4d50e8a065'),
     ObjectId('55ed6f634c859c4d50e8a066'),
     ObjectId('55ed6f634c859c4d50e8a067'),
     ObjectId('55ed6f634c859c4d50e8a068'),
     ObjectId('55ed6f634c859c4d50e8a069'),
     ObjectId('55ed6f634c859c4d50e8a06a'),
     ObjectId('55ed6f634c859c4d50e8a06b'),
     ObjectId('55ed6f634c859c4d50e8a06c'),
     ObjectId('55ed6f634c859c4d50e8a06d'),
     ObjectId('55ed6f634c859c4d50e8a06e'),
     ObjectId('55ed6f634c859c4d50e8a06f'),
     ObjectId('55ed6f634c859c4d50e8a070'),
     ObjectId('55ed6f634c859c4d50e8a071'),
     ObjectId('55ed6f634c859c4d50e8a072'),
     ObjectId('55ed6f634c859c4d50e8a073'),
     ObjectId('55ed6f634c859c4d50e8a074'),
     ObjectId('55ed6f634c859c4d50e8a075'),
     ObjectId('55ed6f634c859c4d50e8a076'),
     ObjectId('55ed6f634c859c4d50e8a077'),
     ObjectId('55ed6f634c859c4d50e8a078'),
     ObjectId('55ed6f634c859c4d50e8a079'),
     ObjectId('55ed6f634c859c4d50e8a07a'),
     ObjectId('55ed6f634c859c4d50e8a07b'),
     ObjectId('55ed6f634c859c4d50e8a07c'),
     ObjectId('55ed6f634c859c4d50e8a07d'),
     ObjectId('55ed6f634c859c4d50e8a07e'),
     ObjectId('55ed6f634c859c4d50e8a07f'),
     ObjectId('55ed6f634c859c4d50e8a080'),
     ObjectId('55ed6f634c859c4d50e8a081'),
     ObjectId('55ed6f634c859c4d50e8a082'),
     ObjectId('55ed6f634c859c4d50e8a083'),
     ObjectId('55ed6f634c859c4d50e8a084'),
     ObjectId('55ed6f634c859c4d50e8a085'),
     ObjectId('55ed6f634c859c4d50e8a086'),
     ObjectId('55ed6f634c859c4d50e8a087'),
     ObjectId('55ed6f634c859c4d50e8a088'),
     ObjectId('55ed6f634c859c4d50e8a089'),
     ObjectId('55ed6f634c859c4d50e8a08a'),
     ObjectId('55ed6f634c859c4d50e8a08b'),
     ObjectId('55ed6f634c859c4d50e8a08c'),
     ObjectId('55ed6f634c859c4d50e8a08d'),
     ObjectId('55ed6f634c859c4d50e8a08e'),
     ObjectId('55ed6f634c859c4d50e8a08f'),
     ObjectId('55ed6f634c859c4d50e8a090'),
     ObjectId('55ed6f634c859c4d50e8a091'),
     ObjectId('55ed6f634c859c4d50e8a092'),
     ObjectId('55ed6f634c859c4d50e8a093'),
     ObjectId('55ed6f634c859c4d50e8a094'),
     ObjectId('55ed6f634c859c4d50e8a095'),
     ObjectId('55ed6f634c859c4d50e8a096'),
     ObjectId('55ed6f634c859c4d50e8a097'),
     ObjectId('55ed6f634c859c4d50e8a098'),
     ObjectId('55ed6f634c859c4d50e8a099'),
     ObjectId('55ed6f634c859c4d50e8a09a'),
     ObjectId('55ed6f634c859c4d50e8a09b'),
     ObjectId('55ed6f634c859c4d50e8a09c'),
     ObjectId('55ed6f634c859c4d50e8a09d'),
     ObjectId('55ed6f634c859c4d50e8a09e'),
     ObjectId('55ed6f634c859c4d50e8a09f'),
     ObjectId('55ed6f634c859c4d50e8a0a0'),
     ObjectId('55ed6f634c859c4d50e8a0a1'),
     ...]



####Database structure

File size comparison:

perth_australia.osm: 204 MB (214,742,096 bytes)
perth_australia.osm.json: 320 MB (335,878,944 bytes)

Total number of documents in database:


```python
db.perth.find().count()
```




    2248470



Number of nodes in database:


```python
db.perth.find({'type':'node'}).count()
```




    2000794



Number of ways in database:


```python
db.perth.find({'type':'way'}).count()
```




    247600



Number of cafe's in database:


```python
db.perth.find({'amenity':'cafe'}).count()
```




    516



Number of cinema's in database:


```python
db.perth.find({'amenity':'cinema'}).count()
```




    36



Number of bank's in database:


```python
db.perth.find({'amenity':'bank'}).count()
```




    138




```python
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
```

User with highest post count:


```python
print(list(db.perth.aggregate(pipeline.top_post_user())))
```

    [{u'count': 725322, u'_id': u'SDavies'}]
    

Top three users by post count:


```python
print(list(db.perth.aggregate(pipeline.top_three_post_users())))
```

    [{u'count': 725322, u'_id': u'SDavies'}, {u'count': 300128, u'_id': u'browny_au'}, {u'count': 155564, u'_id': u'sb9576'}]
    

Count of users who have made a single post:


```python
print(list(db.perth.aggregate(pipeline.single_post_users())))
```

    [{u'num_users': 169, u'_id': 2}]
    

Top five amenity by count:


```python
print(list(db.perth.aggregate(pipeline.top_five_amenity())))
```

    [{u'count': 4486, u'_id': u'parking'}, {u'count': 926, u'_id': u'school'}, {u'count': 592, u'_id': u'fast_food'}, {u'count': 586, u'_id': u'bench'}, {u'count': 542, u'_id': u'restaurant'}]
    

Top five fast food by count:


```python
print(list(db.perth.aggregate(pipeline.top_five_fastfood())))
```

    [{u'count': 62, u'_id': None}, {u'count': 48, u'_id': u'Subway'}, {u'count': 42, u'_id': u"McDonald's"}, {u'count': 30, u'_id': u'Red Rooster'}, {u'count': 30, u'_id': u'KFC'}]
    

####Create a sample database


```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
```

perth_australia_sample.osm: 20.7 MB (21,770,717 bytes)

###5.0 Conclusion

Overall, I didnt have too much trouble processing the dataset. There were no 'problemchars' identified as part of the first pass. Based on my memory of Perth, most of the reported amenity counts seem reasonable, however caution should be exercised when interpreting the presented results as the completeness of the data is unknown. Finally, I did not get a chance to exercise MonogDB's geospatial querying, however the original dataset contains a large amount of latitude/longitude data.

###References

* PyMongo Documentation: https://api.mongodb.org/python/current/
* Udacity Data Wrangling with MonogoDB: https://www.udacity.com/course/data-wrangling-with-mongodb--ud032
