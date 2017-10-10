import requests
import datetime
import difflib
import os, time, sys


url = "https://transloc-api-1-2.p.mashape.com/"

# To improve voice recognition, add common mishearings as alias


# UVA agency ID = 347

# Dictionaries to convert between stop and ID
idToStop = {'4123734': '14th Street NW @ John St', '4123738': '14th Street NW @ Virginia Ave', '4123742': '14th Street NW @ Wertland St (Northbound)', '4123746': '14th Street NW @ Wertland St (Southbound)', '4123750': 'Alderman Rd @ Facilities Mgmt', '4123754': 'Alderman Rd @ Gooch/Dillard', '4123758': 'Alderman Rd @ O-Hill Dining Hall', '4123762': 'Alderman Rd @ Stadium Rd', '4123766': 'Alderman Road @ AFC', '4123770': 'Arlington Blvd @ Massie Rd', '4123774': 'Arlington Blvd @ Barracks Rd Shopping Ctr', '4123778': 'Arlington Blvd @ Arlington Ct', '4123790': 'Copeley Rd @ Massie Rd (Inbound)', '4123794': 'Copeley Rd @ Massie Rd (Outbound)', '4123798': 'Copeley Rd @ Seymour Ct (Inbound)', '4123802': 'Copeley Rd @ Seymour Ct (Outbound)', '4123810': 'Duffy Blvd @ Darden', '4123814': 'Duffy Blvd @ North Grounds Rec', '4123818': 'Emmet St @ Alumni Hall', '4123822': 'Emmet St @ Central Grounds Garage', '4123826': 'Emmet St @ Goodwin Bridge', '4123834': 'Emmet St @ Ruffner Hall', '4123838': 'Emmet St @ Snyder Tennis Courts', '4123842': 'Emmet / Ivy Garage (EIG)', '4123850': 'George Welsh Way @ Bryant Hall (Outbound)', '4123854': 'George Welsh Way @ SAB', '4123858': 'George Welsh Way @ Scott Stadium', '4123862': 'George Welsh Way @ Stadium West Shelf', '4123866': 'Grady Ave @ 16th St', '4123870': 'Grady Ave @ Preston Pl', '4123874': 'Grady Ave @ 10 ½ St NW (Westbound)', '4123878': 'Grady Ave @ 14th St', '4123882': 'Hereford Dr @ Johnson House', '4123886': 'Hereford Dr @ Kellogg Dorm', '4123890': 'Hereford Dr @ Runk Dining Hall', '4123894': 'Ivy Rd @ Emmet / Ivy Garage', '4123902': 'Jefferson Park Ave @ Brandon Ave', '4123906': 'Jefferson Park Ave @ Cabell Hall', '4123910': 'Jefferson Park Ave @ Pinn Hall', '4123914': 'Jefferson Park Ave @ Kent Terrace', '4123918': 'Jefferson Park Ave @ Maury Ave', '4123922': 'Jefferson Park Ave @ Montebello Circle', '4123926': 'Jefferson Park Ave @ Observatory Ave', '4123930': 'Jefferson Park Ave @ Shamrock Rd (Northbound)', '4123934': 'Jefferson Park Ave @ Shamrock Rd (Southbound)', '4123938': 'Jefferson Park Ave @ UVA Hospital', '4123942': 'Jefferson Park Ave @ Valley Rd', '4123946': 'Jefferson Park Ave @ Woodrow St', '4123950': 'Lane Rd @ MR-5', '4123958': 'Madison Ave @ Preston Ave', '4123962': 'Massie Rd @ Copeley Student Housing', '4123966': 'Massie Rd @ Faulkner Housing (Inbound)', '4123970': 'Massie Rd @ Faulkner Housing (Outbound)', '4123978': 'Massie Rd @ Law School', '4123982': 'Massie Rd @ U-Hall East Lot', '4123990': 'McCormick Rd @ McCormick Residence Hall', '4123994': 'McCormick Rd @ O-Hill Dining Hall', '4123998': 'McCormick Rd @ Physics Building', '4124006': 'Mimosa Dr (Inbound)', '4124014': 'Preston Ave @ Washington Park', '4124018': 'Rugby Rd @ 203 Rugby Rd', '4124022': 'Rugby Rd @ Beta Bridge (Outbound)', '4124026': 'Seymour Ct (Inbound)', '4124030': 'Seymour Ct (Outbound)', '4124034': 'Seymour Ct @ Copeley Hill Housing', '4124038': 'Stadium Rd @ Appletree Rd', '4124042': 'Stadium Rd @ Runk Dining Hall', '4124050': 'U-Hall @ Cage Lot', '4124054': 'U-Hall @ Copeley Rd', '4124058': 'U-Hall @ Massie Rd', '4124062': 'U-Hall @ West Entrance', '4124074': 'University Ave @ Jefferson Park Ave', '4124078': 'Whitehead Rd @ Engineering School (Inbound)', '4124082': 'Whitehead Rd @ Engineering School (Outbound)', '4128262': 'Madison Ave @ Grady Ave', '4137602': 'Massie Rd @ John Paul Jones Arena', '4148110': 'Emmet St @ Lambeth Housing', '4178518': 'George Welsh Way @ Bryant Hall (Inbound)', '4178522': 'McCormick Rd @ Gilmer Hall', '4178524': 'McCormick Rd @ Thornton Hall', '4188128': 'Mimosa Dr (Outbound)', '4202642': 'Stadium Rd @ Stadium Garage', '4209040': 'Colonnade Dr @ Ivy Rd', '4209042': 'Colonnade Dr @ University Heights', '4209044': 'Ivy Rd @ Foods of All Nations', '4209046': 'McCormick Rd @ Brown College (NIGHT STOP)', '4209048': 'McCormick Rd @ Clark Hall (NIGHT STOP)', '4209050': 'McCormick Rd @ Garrett Hall', '4209052': 'McCormick Rd @ Monroe Hall', '4209054': 'McCormick Rd @ UVA Chapel', '4209056': 'University Ave @ Snyder Tennis Courts', '4209058': "University Ave @ Carr's Hill Field", '4209060': 'McCormick Rd @ Alderman Library', '4209062': 'Massie Rd @ North Grounds Rec (Inbound)', '4209064': 'Massie Rd @ North Grounds Rec (Outbound)', '4209066': 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', '4211480': 'Lee St @ UVA Hospital'}
stopToId = {'14th Street NW @ John St': '4123734', '14th Street NW @ Virginia Ave': '4123738', '14th Street NW @ Wertland St (Northbound)': '4123742', '14th Street NW @ Wertland St (Southbound)': '4123746', 'Alderman Rd @ Facilities Mgmt': '4123750', 'Alderman Rd @ Gooch/Dillard': '4123754', 'Alderman Rd @ O-Hill Dining Hall': '4123758', 'Alderman Rd @ Stadium Rd': '4123762', 'Alderman Road @ AFC': '4123766', 'Arlington Blvd @ Massie Rd': '4123770', 'Arlington Blvd @ Barracks Rd Shopping Ctr': '4123774', 'Arlington Blvd @ Arlington Ct': '4123778', 'Copeley Rd @ Massie Rd (Inbound)': '4123790', 'Copeley Rd @ Massie Rd (Outbound)': '4123794', 'Copeley Rd @ Seymour Ct (Inbound)': '4123798', 'Copeley Rd @ Seymour Ct (Outbound)': '4123802', 'Duffy Blvd @ Darden': '4123810', 'Duffy Blvd @ North Grounds Rec': '4123814', 'Emmet St @ Alumni Hall': '4123818', 'Emmet St @ Central Grounds Garage': '4123822', 'Emmet St @ Goodwin Bridge': '4123826', 'Emmet St @ Ruffner Hall': '4123834', 'Emmet St @ Snyder Tennis Courts': '4123838', 'Emmet / Ivy Garage (EIG)': '4123842', 'George Welsh Way @ Bryant Hall (Outbound)': '4123850', 'George Welsh Way @ SAB': '4123854', 'George Welsh Way @ Scott Stadium': '4123858', 'George Welsh Way @ Stadium West Shelf': '4123862', 'Grady Ave @ 16th St': '4123866', 'Grady Ave @ Preston Pl': '4123870', 'Grady Ave @ 10 ½ St NW (Westbound)': '4123874', 'Grady Ave @ 14th St': '4123878', 'Hereford Dr @ Johnson House': '4123882', 'Hereford Dr @ Kellogg Dorm': '4123886', 'Hereford Dr @ Runk Dining Hall': '4123890', 'Ivy Rd @ Emmet / Ivy Garage': '4123894', 'Jefferson Park Ave @ Brandon Ave': '4123902', 'Jefferson Park Ave @ Cabell Hall': '4123906', 'Jefferson Park Ave @ Pinn Hall': '4123910', 'Jefferson Park Ave @ Kent Terrace': '4123914', 'Jefferson Park Ave @ Maury Ave': '4123918', 'Jefferson Park Ave @ Montebello Circle': '4123922', 'Jefferson Park Ave @ Observatory Ave': '4123926', 'Jefferson Park Ave @ Shamrock Rd (Northbound)': '4123930', 'Jefferson Park Ave @ Shamrock Rd (Southbound)': '4123934', 'Jefferson Park Ave @ UVA Hospital': '4123938', 'Jefferson Park Ave @ Valley Rd': '4123942', 'Jefferson Park Ave @ Woodrow St': '4123946', 'Lane Rd @ MR-5': '4123950', 'Madison Ave @ Preston Ave': '4123958', 'Massie Rd @ Copeley Student Housing': '4123962', 'Massie Rd @ Faulkner Housing (Inbound)': '4123966', 'Massie Rd @ Faulkner Housing (Outbound)': '4123970', 'Massie Rd @ Law School': '4123978', 'Massie Rd @ U-Hall East Lot': '4123982', 'McCormick Rd @ McCormick Residence Hall': '4123990', 'McCormick Rd @ O-Hill Dining Hall': '4123994', 'McCormick Rd @ Physics Building': '4123998', 'Mimosa Dr (Inbound)': '4124006', 'Preston Ave @ Washington Park': '4124014', 'Rugby Rd @ 203 Rugby Rd': '4124018', 'Rugby Rd @ Beta Bridge (Outbound)': '4124022', 'Seymour Ct (Inbound)': '4124026', 'Seymour Ct (Outbound)': '4124030', 'Seymour Ct @ Copeley Hill Housing': '4124034', 'Stadium Rd @ Appletree Rd': '4124038', 'Stadium Rd @ Runk Dining Hall': '4124042', 'U-Hall @ Cage Lot': '4124050', 'U-Hall @ Copeley Rd': '4124054', 'U-Hall @ Massie Rd': '4124058', 'U-Hall @ West Entrance': '4124062', 'University Ave @ Jefferson Park Ave': '4124074', 'Whitehead Rd @ Engineering School (Inbound)': '4124078', 'Whitehead Rd @ Engineering School (Outbound)': '4124082', 'Madison Ave @ Grady Ave': '4128262', 'Massie Rd @ John Paul Jones Arena': '4137602', 'Emmet St @ Lambeth Housing': '4148110', 'George Welsh Way @ Bryant Hall (Inbound)': '4178518', 'McCormick Rd @ Gilmer Hall': '4178522', 'McCormick Rd @ Thornton Hall': '4178524', 'Mimosa Dr (Outbound)': '4188128', 'Stadium Rd @ Stadium Garage': '4202642', 'Colonnade Dr @ Ivy Rd': '4209040', 'Colonnade Dr @ University Heights': '4209042', 'Ivy Rd @ Foods of All Nations': '4209044', 'McCormick Rd @ Brown College (NIGHT STOP)': '4209046', 'McCormick Rd @ Clark Hall (NIGHT STOP)': '4209048', 'McCormick Rd @ Garrett Hall': '4209050', 'McCormick Rd @ Monroe Hall': '4209052', 'McCormick Rd @ UVA Chapel': '4209054', 'University Ave @ Snyder Tennis Courts': '4209056', "University Ave @ Carr's Hill Field": '4209058', 'McCormick Rd @ Alderman Library': '4209060', 'Massie Rd @ North Grounds Rec (Inbound)': '4209062', 'Massie Rd @ North Grounds Rec (Outbound)': '4209064', 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)': '4209066', 'Lee St @ UVA Hospital': '4211480'}

# A list of all UVA stops
stops  = ['14th Street NW @ John St', '14th Street NW @ Virginia Ave', '14th Street NW @ Wertland St (Northbound)', '14th Street NW @ Wertland St (Southbound)', 'Alderman Rd @ Facilities Mgmt', 'Alderman Rd @ Gooch/Dillard', 'Alderman Rd @ O-Hill Dining Hall', 'Alderman Rd @ Stadium Rd', 'Alderman Road @ AFC', 'Arlington Blvd @ Massie Rd', 'Arlington Blvd @ Barracks Rd Shopping Ctr', 'Arlington Blvd @ Arlington Ct', 'Copeley Rd @ Massie Rd (Inbound)', 'Copeley Rd @ Massie Rd (Outbound)', 'Copeley Rd @ Seymour Ct (Inbound)', 'Copeley Rd @ Seymour Ct (Outbound)', 'Duffy Blvd @ Darden', 'Duffy Blvd @ North Grounds Rec', 'Emmet St @ Alumni Hall', 'Emmet St @ Central Grounds Garage', 'Emmet St @ Goodwin Bridge', 'Emmet St @ Ruffner Hall', 'Emmet St @ Snyder Tennis Courts', 'Emmet / Ivy Garage (EIG)', 'George Welsh Way @ Bryant Hall (Outbound)', 'George Welsh Way @ SAB', 'George Welsh Way @ Scott Stadium', 'George Welsh Way @ Stadium West Shelf', 'Grady Ave @ 16th St', 'Grady Ave @ Preston Pl', 'Grady Ave @ 10 ½ St NW (Westbound)', 'Grady Ave @ 14th St', 'Hereford Dr @ Johnson House', 'Hereford Dr @ Kellogg Dorm', 'Hereford Dr @ Runk Dining Hall', 'Ivy Rd @ Emmet / Ivy Garage', 'Jefferson Park Ave @ Brandon Ave', 'Jefferson Park Ave @ Cabell Hall', 'Jefferson Park Ave @ Pinn Hall', 'Jefferson Park Ave @ Kent Terrace', 'Jefferson Park Ave @ Maury Ave', 'Jefferson Park Ave @ Montebello Circle', 'Jefferson Park Ave @ Observatory Ave', 'Jefferson Park Ave @ Shamrock Rd (Northbound)', 'Jefferson Park Ave @ Shamrock Rd (Southbound)', 'Jefferson Park Ave @ UVA Hospital', 'Jefferson Park Ave @ Valley Rd', 'Jefferson Park Ave @ Woodrow St', 'Lane Rd @ MR-5', 'Madison Ave @ Preston Ave', 'Massie Rd @ Copeley Student Housing', 'Massie Rd @ Faulkner Housing (Inbound)', 'Massie Rd @ Faulkner Housing (Outbound)', 'Massie Rd @ Law School', 'Massie Rd @ U-Hall East Lot', 'McCormick Rd @ McCormick Residence Hall', 'McCormick Rd @ O-Hill Dining Hall', 'McCormick Rd @ Physics Building', 'Mimosa Dr (Inbound)', 'Preston Ave @ Washington Park', 'Rugby Rd @ 203 Rugby Rd', 'Rugby Rd @ Beta Bridge (Outbound)', 'Seymour Ct (Inbound)', 'Seymour Ct (Outbound)', 'Seymour Ct @ Copeley Hill Housing', 'Stadium Rd @ Appletree Rd', 'Stadium Rd @ Runk Dining Hall', 'U-Hall @ Cage Lot', 'U-Hall @ Copeley Rd', 'U-Hall @ Massie Rd', 'U-Hall @ West Entrance', 'University Ave @ Jefferson Park Ave', 'Whitehead Rd @ Engineering School (Inbound)', 'Whitehead Rd @ Engineering School (Outbound)', 'Madison Ave @ Grady Ave', 'Massie Rd @ John Paul Jones Arena', 'Emmet St @ Lambeth Housing', 'George Welsh Way @ Bryant Hall (Inbound)', 'McCormick Rd @ Gilmer Hall', 'McCormick Rd @ Thornton Hall', 'Mimosa Dr (Outbound)', 'Stadium Rd @ Stadium Garage', 'Colonnade Dr @ Ivy Rd', 'Colonnade Dr @ University Heights', 'Ivy Rd @ Foods of All Nations', 'McCormick Rd @ Brown College (NIGHT STOP)', 'McCormick Rd @ Clark Hall (NIGHT STOP)', 'McCormick Rd @ Garrett Hall', 'McCormick Rd @ Monroe Hall', 'McCormick Rd @ UVA Chapel', 'University Ave @ Snyder Tennis Courts', "University Ave @ Carr's Hill Field", 'McCormick Rd @ Alderman Library', 'Massie Rd @ North Grounds Rec (Inbound)', 'Massie Rd @ North Grounds Rec (Outbound)', 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', 'Lee St @ UVA Hospital']

stop_alias = {'14th Street NW @ John St' : '14th Street NW @ John St',
'14th Street NW @ Virginia Ave' : '14th Street NW @ Virginia Ave',
'14th Street NW @ Wertland St (Northbound)' : '14th Street NW @ Wertland St (Northbound)',
'14th Street NW @ Wertland St (Southbound)' : '14th Street NW @ Wertland St (Southbound)',
'Alderman Rd @ Facilities Mgmt' : 'Alderman Rd @ Facilities Mgmt', 'read that alderman read at facilities me' : 'Alderman Rd @ Facilities Mgmt', 'alderman minute at facilities management' : 'Alderman Rd @ Facilities Mgmt', 'be a alderman rodent facilities management' : 'Alderman Rd @ Facilities Mgmt',
'Alderman Rd @ Gooch/Dillard' : 'Alderman Rd @ Gooch/Dillard',
'Alderman Rd @ O-Hill Dining Hall' : 'Alderman Rd @ O-Hill Dining Hall',
'Alderman Rd @ Stadium Rd' : 'Alderman Rd @ Stadium Rd', 'alderman road at stadium' :  'Alderman Rd @ Stadium Rd', 'alderman rooted stadium' : 'Alderman Rd @ Stadium Rd', 'alderman rodents tdm' : 'Alderman Rd @ Stadium Rd', 'minute at stadium' : 'Alderman Rd @ Stadium Rd',
'Arlington Blvd @ Massie Rd' : 'Arlington Blvd @ Massie Rd',
'Arlington Blvd @ Barracks Rd Shopping Ctr' : 'Arlington Blvd @ Barracks Rd Shopping Ctr',
'Arlington Blvd @ Arlington Ct' : 'Arlington Blvd @ Arlington Ct', 'Arlington boulevard in Arlington quote' : 'Arlington Blvd @ Arlington Ct',
'Copeley Rd @ Massie Rd (Inbound)' : 'Copeley Rd @ Massie Rd (Inbound)',
'Copeley Rd @ Massie Rd (Outbound)' : 'Copeley Rd @ Massie Rd (Outbound)',
'Copeley Rd @ Seymour Ct (Inbound)' : 'Copeley Rd @ Seymour Ct (Inbound)',
'Copeley Rd @ Seymour Ct (Outbound)' : 'Copeley Rd @ Seymour Ct (Outbound)',
'Duffy Blvd @ Darden' : 'Duffy Blvd @ Darden',
'Duffy Blvd @ North Grounds Rec' : 'Duffy Blvd @ North Grounds Rec',
'Emmet St @ Alumni Hall' : 'Emmet St @ Alumni Hall',
'Emmet St @ Central Grounds Garage' : 'Emmet St @ Central Grounds Garage',
'Emmet St @ Goodwin Bridge' : 'Emmet St @ Goodwin Bridge',
'Emmet St @ Ruffner Hall' : 'Emmet St @ Ruffner Hall',
'Emmet St @ Snyder Tennis Courts' : 'Emmet St @ Snyder Tennis Courts',
'Emmet / Ivy Garage (EIG)' : 'Emmet / Ivy Garage (EIG)', 'm. and ivy garage E I g.' : 'Emmet / Ivy Garage (EIG)',
'George Welsh Way @ Bryant Hall (Outbound)' : 'George Welsh Way @ Bryant Hall (Outbound)',
'George Welsh Way @ SAB' : 'George Welsh Way @ SAB',
'George Welsh Way @ Scott Stadium' : 'George Welsh Way @ Scott Stadium',
'George Welsh Way @ Stadium West Shelf' : 'George Welsh Way @ Stadium West Shelf',
'Grady Ave @ 16th St' : 'Grady Ave @ 16th St',
'Grady Ave @ Preston Pl' : 'Grady Ave @ Preston Pl',
'Grady Ave @ 10 ½ St NW (Westbound)' : 'Grady Ave @ 10 ½ St NW (Westbound)',
'Grady Ave @ 14th St' : 'Grady Ave @ 14th St',
'Hereford Dr @ Johnson House' : 'Hereford Dr @ Johnson House', 'here for drive and Johnson' : 'Hereford Dr @ Johnson House',
'Hereford Dr @ Kellogg Dorm' : 'Hereford Dr @ Kellogg Dorm',
'Hereford Dr @ Runk Dining Hall' : 'Hereford Dr @ Runk Dining Hall',
'Ivy Rd @ Emmet / Ivy Garage' : 'Ivy Rd @ Emmet / Ivy Garage',
'Jefferson Park Ave @ Brandon Ave' : 'Jefferson Park Ave @ Brandon Ave',
'Jefferson Park Ave @ Cabell Hall' : 'Jefferson Park Ave @ Cabell Hall',
'Jefferson Park Ave @ Pinn Hall' : 'Jefferson Park Ave @ Pinn Hall',
'Jefferson Park Ave @ Kent Terrace' : 'Jefferson Park Ave @ Kent Terrace',
'Jefferson Park Ave @ Maury Ave' : 'Jefferson Park Ave @ Maury Ave',
'Jefferson Park Ave @ Montebello Circle' : 'Jefferson Park Ave @ Montebello Circle',
'Jefferson Park Ave @ Observatory Ave' : 'Jefferson Park Ave @ Observatory Ave',
'Jefferson Park Ave @ Shamrock Rd (Northbound)' : 'Jefferson Park Ave @ Shamrock Rd (Northbound)',
'Jefferson Park Ave @ Shamrock Rd (Southbound)' : 'Jefferson Park Ave @ Shamrock Rd (Southbound)',
'Jefferson Park Ave @ UVA Hospital' : 'Jefferson Park Ave @ UVA Hospital',
'Jefferson Park Ave @ Valley Rd' : 'Jefferson Park Ave @ Valley Rd',
'Jefferson Park Ave @ Woodrow St' : 'Jefferson Park Ave @ Woodrow St',
'Lane Rd @ MR-5' : 'Lane Rd @ MR-5',
'Madison Ave @ Preston Ave' : 'Madison Ave @ Preston Ave',
'Massie Rd @ Copeley Student Housing' : 'Massie Rd @ Copeley Student Housing',
'Massie Rd @ Faulkner Housing (Inbound)' : 'Massie Rd @ Faulkner Housing (Inbound)',
'Massie Rd @ Faulkner Housing (Outbound)' : 'Massie Rd @ Faulkner Housing (Outbound)',
'Massie Rd @ Law School' : 'Massie Rd @ Law School',
'Massie Rd @ U-Hall East Lot' : 'Massie Rd @ U-Hall East Lot',
'McCormick Rd @ McCormick Residence Hall' : 'McCormick Rd @ McCormick Residence Hall',
'McCormick Rd @ O-Hill Dining Hall' : 'McCormick Rd @ O-Hill Dining Hall',
'McCormick Rd @ Physics Building' : 'McCormick Rd @ Physics Building',
'Mimosa Dr (Inbound)' : 'Mimosa Dr (Inbound)',
'Preston Ave @ Washington Park' : 'Preston Ave @ Washington Park',
'Rugby Rd @ 203 Rugby Rd' : 'Rugby Rd @ 203 Rugby Rd',
'Rugby Rd @ Beta Bridge (Outbound)' : 'Rugby Rd @ Beta Bridge (Outbound)',
'Seymour Ct (Inbound)' : 'Seymour Ct (Inbound)',
'Seymour Ct (Outbound)' : 'Seymour Ct (Outbound)',
'Seymour Ct @ Copeley Hill Housing' : 'Seymour Ct @ Copeley Hill Housing', 'simard court at compli hussy' : 'Seymour Ct @ Copeley Hill Housing',
'Stadium Rd @ Appletree Rd' : 'Stadium Rd @ Appletree Rd',
'Stadium Rd @ Runk Dining Hall' : 'Stadium Rd @ Runk Dining Hall',
'U-Hall @ Cage Lot' : 'U-Hall @ Cage Lot',
'U-Hall @ Copeley Rd' : 'U-Hall @ Copeley Rd',
'U-Hall @ Massie Rd' : 'U-Hall @ Massie Rd',
'U-Hall @ West Entrance' : 'U-Hall @ West Entrance',
'University Ave @ Jefferson Park Ave' : 'University Ave @ Jefferson Park Ave',
'Whitehead Rd @ Engineering School (Inbound)' : 'Whitehead Rd @ Engineering School (Inbound)',
'Whitehead Rd @ Engineering School (Outbound)' : 'Whitehead Rd @ Engineering School (Outbound)',
'Madison Ave @ Grady Ave' : 'Madison Ave @ Grady Ave',
'Massie Rd @ John Paul Jones Arena' : 'Massie Rd @ John Paul Jones Arena',
'Emmet St @ Lambeth Housing' : 'Emmet St @ Lambeth Housing',
'George Welsh Way @ Bryant Hall (Inbound)' : 'George Welsh Way @ Bryant Hall (Inbound)',
'McCormick Rd @ Gilmer Hall' : 'McCormick Rd @ Gilmer Hall',
'McCormick Rd @ Thornton Hall' : 'McCormick Rd @ Thornton Hall',
'Mimosa Dr (Outbound)' : 'Mimosa Dr (Outbound)',
'Stadium Rd @ Stadium Garage' : 'Stadium Rd @ Stadium Garage',
'Colonnade Dr @ Ivy Rd' : 'Colonnade Dr @ Ivy Rd',
'Colonnade Dr @ University Heights' : 'Colonnade Dr @ University Heights',
'Ivy Rd @ Foods of All Nations' : 'Ivy Rd @ Foods of All Nations',
'McCormick Rd @ Brown College (NIGHT STOP)' : 'McCormick Rd @ Brown College (NIGHT STOP)',
'McCormick Rd @ Clark Hall (NIGHT STOP)' : 'McCormick Rd @ Clark Hall (NIGHT STOP)',
'McCormick Rd @ Garrett Hall' : 'McCormick Rd @ Garrett Hall',
'McCormick Rd @ Monroe Hall' : 'McCormick Rd @ Monroe Hall',
'McCormick Rd @ UVA Chapel' : 'McCormick Rd @ UVA Chapel',
'University Ave @ Snyder Tennis Courts' : 'University Ave @ Snyder Tennis Courts',
"University Ave @ Carr's Hill Field" : "University Ave @ Carr's Hill Field",
'McCormick Rd @ Alderman Library' : 'McCormick Rd @ Alderman Library',
'Massie Rd @ North Grounds Rec (Inbound)' : 'Massie Rd @ North Grounds Rec (Inbound)',
'Massie Rd @ North Grounds Rec (Outbound)' : 'Massie Rd @ North Grounds Rec (Outbound)',
'Massie Rd @ John Paul Jones Arena (NIGHT STOP)' : 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)',
'Lee St @ UVA Hospital' : 'Lee St @ UVA Hospital',



# training data 1
              '14th street northwest that John street' : '14th Street NW @ John St', '14th street northwest app Virginia avenue' : '14th Street NW @ Virginia Ave','14th street NW at wertland st. northbound' : '14th Street NW @ Wertland St (Northbound)', '14th street northwest at wirthlin street song' : '14th Street NW @ Wertland St (Southbound)','alderman rotech couch slash Dillard' : 'Alderman Rd @ Gooch/Dillard',    'Arlington boulevard at Massey red' : 'Arlington Blvd @ Massie Rd', 'Arlington boulevard at Arlington court' : 'Arlington Blvd @ Arlington Ct', 'coakley road at Massey road in bound' : 'Copeley Rd @ Massie Rd (Inbound)', 'road at Massey read out bound' : 'Copeley Rd @ Massie Rd (Outbound)', 'Grady avenue at 10 and half street northwest west bend' : 'Grady Ave @ 10 ½ St NW (Westbound)', 'her for drive at Johnson' : 'Hereford Dr @ Johnson House', 'Hereford try that door' : 'Hereford Dr @ Kellogg Dorm', 'for drive it up dining hall' : 'Hereford Dr @ Runk Dining Hall', 'Jefferson park avenue on family room' : 'Jefferson Park Ave @ Valley Rd', 'McCormick credit physics mode' : 'McCormick Rd @ Physics Building', 'Wrigley road at 203 about be rich' : 'Rugby Rd @ 203 Rugby Rd', 'Seymour port in inbound' : 'Seymour Ct (Inbound)', 'stadium road at apple tree' : 'Stadium Rd @ Appletree Rd', 'U hall at copeley rd' : 'U-Hall @ Copeley Rd', 'colonnade dry that idea' : 'Colonnade Dr @ Ivy Rd', 'I the road it fits of all nations' : 'Ivy Rd @ Foods of All Nations', '14th street northwest a chance ster' : '14th Street NW @ John St',

#training data 2
              '14th street northwest a chauncey' : '14th Street NW @ John St', '14 street northwest art ridge Enya' : '14th Street NW @ Virginia Ave', '14th street northwest I want in street earthbound' : '14th Street NW @ Wertland St (Northbound)','ortmann street south' : '14th Street NW @ Wertland St (Southbound)', 'ride that alderman road up facilities manageme' : 'Alderman Rd @ Facilities Mgmt', 'alderman run a couch dealer' : 'Alderman Rd @ Gooch/Dillard', 'alderman rd at O. hill dining hall' : 'Alderman Rd @ O-Hill Dining Hall', 'alderman rd at stadium rd' : 'Alderman Rd @ Stadium Rd', 'alderman road at afc' : 'Alderman Road @ AFC', 'Arlington boulevard at Massey great' : 'Arlington Blvd @ Massie Rd', 'Arlington boulevard at barracks rd shopping ctr' : 'Arlington Blvd @ Barracks Rd Shopping Ctr', 'Emmett st. at Snyder tennis courts' : 'Emmet St @ Snyder Tennis Courts', 'Emmett slash ivy garage EIG' : 'Emmet / Ivy Garage (EIG)', 'George welsh way at Bryant hall outbound' : 'George Welsh Way @ Bryant Hall (Outbound)', 'George welsh way at SAB' : 'George Welsh Way @ SAB', 'George welsh way at Scott stadium' : 'George Welsh Way @ Scott Stadium', 'George welsh way at stadium west shelf' : 'George Welsh Way @ Stadium West Shelf', 'Grady ave at 16th st.' : 'Grady Ave @ 16th St', 'Grady ave at Preston pl' : 'Grady Ave @ Preston Pl', '10 have street northwest wessman' : 'Grady Ave @ 10 ½ St NW (Westbound)', 'Grady ave at 14th st.' : 'Grady Ave @ 14th St', 'Hereford Dr. at Johnson house' : 'Hereford Dr @ Johnson House', 'Hereford Dr. at Kellogg dorm' : 'Hereford Dr @ Kellogg Dorm', 'Hereford Dr. at runk dining hall' : 'Hereford Dr @ Runk Dining Hall','a theater to Emmett Abigail' : 'Ivy Rd @ Emmet / Ivy Garage', 'shamrock read south' : 'Jefferson Park Ave @ Shamrock Rd (Southbound)', 'Jefferson park avenue ige awesome' : 'Jefferson Park Ave @ UVA Hospital', 'Jefferson park ave at Woodrow st.' : 'Jefferson Park Ave @ Woodrow St', 'Massey rd at copeley student housing' : 'Massie Rd @ Copeley Student Housing', 'Massey rd at Faulkner housing outbound' : 'Massie Rd @ Faulkner Housing (Outbound)', 'Preston ave at Washington park' : 'Preston Ave @ Washington Park', 'rugby go to 23 red' : 'Rugby Rd @ 203 Rugby Rd', 'rugby rd at beta bridge outbound' : 'Rugby Rd @ Beta Bridge (Outbound)', 'Seymour ct inbound' : 'Seymour Ct (Inbound)', 'Seymour ct outbound' : 'Seymour Ct (Outbound)', 'Seymour ct at copeley hill housing' : 'Seymour Ct @ Copeley Hill Housing', 'stadium rd at apple tree rd' : 'Stadium Rd @ Appletree Rd', 'stadium rd at runk dining hall' : 'Stadium Rd @ Runk Dining Hall', 'U hall at cage lot' : 'U-Hall @ Cage Lot', 'U haul at coakley Libra' : 'U-Hall @ Copeley Rd','U hall at Massey rd' : 'U-Hall @ Massie Rd', 'U hall at west entrance' : 'U-Hall @ West Entrance', 'university ave at Jefferson park ave' : 'University Ave @ Jefferson Park Ave', 'whitehead rd at engineering school inbound' : 'Whitehead Rd @ Engineering School (Inbound)', 'whitehead rd at engineering school outbound' : 'Whitehead Rd @ Engineering School (Outbound)', 'Madison ave at Grady ave' : 'Madison Ave @ Grady Ave', 'Massey rd at John Paul Jones arena' : 'Massie Rd @ John Paul Jones Arena', 'Emmett st. at Lambeth housing' : 'Emmet St @ Lambeth Housing', 'George welsh way at Bryant hall inbound' : 'George Welsh Way @ Bryant Hall (Inbound)', 'McCormick rd at gilmer hall' : 'McCormick Rd @ Gilmer Hall', 'McCormick rd at Thornton hall' : 'McCormick Rd @ Thornton Hall', 'mimosa Dr. outbound' : 'Mimosa Dr (Outbound)', 'stadium rd at stadium garage' : 'Stadium Rd @ Stadium Garage', 'colonie try that I be rich' : 'Colonnade Dr @ Ivy Rd', 'colonnade Dr. at university heights' : 'Colonnade Dr @ University Heights', 'ivy rd at foods of all nations' : 'Ivy Rd @ Foods of All Nations', 'Massey rd at north grounds rec inbound' : 'Massie Rd @ North Grounds Rec (Inbound)', 'Massey rd at John Paul Jones arena night stop' : 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', '14th street northwest at Johnston' : '14th Street NW @ John St',


# part 3
'14th street northwest up Johnson' : '14th Street NW @ John St', 'Virginia avenue' : '14th Street NW @ Virginia Ave', '14 street northwest ortolan street north bound' : '14th Street NW @ Wertland St (Northbound)', '14th street northwest that wittlin streets of' : '14th Street NW @ Wertland St (Southbound)','alderman rd at facilities Mgmt' : 'Alderman Rd @ Facilities Mgmt', 'alderman rodent couch tiller' : 'Alderman Rd @ Gooch/Dillard', 'alderman roto dining hall' : 'Alderman Rd @ O-Hill Dining Hall', 'alderman rodent stadium' : 'Alderman Rd @ Stadium Rd', 'alderman Rhoda afc' : 'Alderman Road @ AFC', 'Arlington boulevard of mass' : 'Arlington Blvd @ Massie Rd', 'Arlington boulevard of ferrets read shopping scene' : 'Arlington Blvd @ Barracks Rd Shopping Ctr', 'Arlington boulevard at Arlington ct' : 'Arlington Blvd @ Arlington Ct', 'copeley rd at Massey rd inbound' : 'Copeley Rd @ Massie Rd (Inbound)', 'copeley rd at Massey rd outbound' : 'Copeley Rd @ Massie Rd (Outbound)', 'copeley rd at Seymour ct inbound' : 'Copeley Rd @ Seymour Ct (Inbound)', 'copeley rd at Seymour ct outbound' : 'Copeley Rd @ Seymour Ct (Outbound)', 'Duffy boulevard at darden' : 'Duffy Blvd @ Darden', 'Duffy boulevard at north grounds rec' : 'Duffy Blvd @ North Grounds Rec', 'Emmett st. at alumni hall' : 'Emmet St @ Alumni Hall', 'Emmett st. at central grounds garage' : 'Emmet St @ Central Grounds Garage', 'Emmett st. at Goodwin bridge' : 'Emmet St @ Goodwin Bridge', 'Emmett st. at ruffner hall' : 'Emmet St @ Ruffner Hall',



'emit street it Snyder tennis courts' : 'Emmet St @ Snyder Tennis Courts','ib garage EIG' : 'Emmet / Ivy Garage (EIG)', 'George wash way at Brian hall out pound' : 'George Welsh Way @ Bryant Hall (Outbound)', 'George wash way at SAP' : 'George Welsh Way @ SAB', 'George wash wait at Scott stadium' : 'George Welsh Way @ Scott Stadium', 'stadium west shelf' : 'George Welsh Way @ Stadium West Shelf','Grady avenue at 16th street' : 'Grady Ave @ 16th St', 'rady avenue at Preston please' : 'Grady Ave @ Preston Pl', '10 and have street northwest west and' : 'Grady Ave @ 10 ½ St NW (Westbound)', 'grand avenue on 14th street' : 'Grady Ave @ 14th St', 'Hereford drive and Johnson' : 'Hereford Dr @ Johnson House',


'her for drive a calendar' : 'Hereford Dr @ Kellogg Dorm','her for try that wrong tiny hall' : 'Hereford Dr @ Runk Dining Hall', 'ivy rd at Emmett slash ivy garage' : 'Ivy Rd @ Emmet / Ivy Garage', 'Jefferson park ave at Brandon ave' : 'Jefferson Park Ave @ Brandon Ave', 'Jefferson park ave at Cabell hall' : 'Jefferson Park Ave @ Cabell Hall', 'Jefferson park ave at pinn hall' : 'Jefferson Park Ave @ Pinn Hall', 'Jefferson park ave at Kent terrace' : 'Jefferson Park Ave @ Kent Terrace', 'Jefferson park ave at Maury ave' : 'Jefferson Park Ave @ Maury Ave', 'Jefferson park ave at Montebello circle' : 'Jefferson Park Ave @ Montebello Circle', 'Jefferson park ave at observatory ave' : 'Jefferson Park Ave @ Observatory Ave', 'Jefferson park ave at shamrock rd northbound' : 'Jefferson Park Ave @ Shamrock Rd (Northbound)', 'Jefferson park ave at shamrock rd southbound' : 'Jefferson Park Ave @ Shamrock Rd (Southbound)', 'Jefferson park ave at UVA hospital' : 'Jefferson Park Ave @ UVA Hospital', 'Jefferson park ave at valley rd' : 'Jefferson Park Ave @ Valley Rd', 'MR5' : 'Lane Rd @ MR-5', 'Madison ave at Preston ave' : 'Madison Ave @ Preston Ave', 'coakley student housing' : 'Massie Rd @ Copeley Student Housing', 'Massey rd at Faulkner housing inbound' : 'Massie Rd @ Faulkner Housing (Inbound)', 'write that Massey root of Faulkner housing out down' : 'Massie Rd @ Faulkner Housing (Outbound)',


'Massey rd at law school' : 'Massie Rd @ Law School', 'Massey rd at U hall east lot' : 'Massie Rd @ U-Hall East Lot', 'McCormick rd at McCormick residence hall' : 'McCormick Rd @ McCormick Residence Hall', 'McCormick rd at O. hill dining hall' : 'McCormick Rd @ O-Hill Dining Hall', 'McCormick rd at physics building' : 'McCormick Rd @ Physics Building', 'mimosa Dr. inbound' : 'Mimosa Dr (Inbound)',

# part 4

'McCormick rodent McCormick residential' : 'Preston Ave @ Washington Park', 'rugby related to have 3' : 'Rugby Rd @ 203 Rugby Rd', 'rugby road update a bridge up pound' : 'Rugby Rd @ Beta Bridge (Outbound)', 'Seymour court in band' : 'Seymour Ct (Inbound)','cinemark work out pound' : 'Seymour Ct (Outbound)', 'sea marquart ecobee hillhouse in' : 'Seymour Ct @ Copeley Hill Housing', 'stadium Rida apple tree road' : 'Stadium Rd @ Appletree Rd', 'stadium road ranked dining hall' : 'Stadium Rd @ Runk Dining Hall', 'you hello kitchen light' : 'U-Hall @ Cage Lot', 'U haul a coakley road' : 'U-Hall @ Copeley Rd','you hall at west entrance' : 'U-Hall @ West Entrance', 'university avenue at Jefferson park avenue' : 'University Ave @ Jefferson Park Ave', 'whitehead motet engineering school in down' : 'Whitehead Rd @ Engineering School (Inbound)', 'whitehead motet engineering school out pound' : 'Whitehead Rd @ Engineering School (Outbound)', 'Madison avenue of radio avenue' : 'Madison Ave @ Grady Ave', 'Massey go to John Paul Jones you now' : 'Massie Rd @ John Paul Jones Arena', 'Emmett streetlamp of housing' : 'Emmet St @ Lambeth Housing', 'George wash where Brian hole in down' : 'George Welsh Way @ Bryant Hall (Inbound)', 'McCormick rodent Kilmer hall' : 'McCormick Rd @ Gilmer Hall', 'McCormick read it for now' : 'McCormick Rd @ Thornton Hall','stadium stadium garage' : 'Stadium Rd @ Stadium Garage', 'colony drive at ivy wrote' : 'Colonnade Dr @ Ivy Rd', 'colonie I drive at university heights' : 'Colonnade Dr @ University Heights', 'I be rodent hits of all nations' : 'Ivy Rd @ Foods of All Nations',

'McCormick rd at brown college night stop' : 'McCormick Rd @ Brown College (NIGHT STOP)', 'McCormick rd at Clark hall night stop' : 'McCormick Rd @ Clark Hall (NIGHT STOP)', 'McCormick rd at Garrett hall' : 'McCormick Rd @ Garrett Hall', 'McCormick rd at Monroe hall' : 'McCormick Rd @ Monroe Hall', 'McCormick rd at UVA chapel' : 'McCormick Rd @ UVA Chapel', 'university ave at Snyder tennis courts' : 'University Ave @ Snyder Tennis Courts', "university ave at Carr's hill field" : "University Ave @ Carr's Hill Field", 'McCormick rd at alderman library' : 'McCormick Rd @ Alderman Library', 'Massey related north Brunswick invalid' : 'Massie Rd @ North Grounds Rec (Inbound)', 'Massey rd at north grounds rec outbound' : 'Massie Rd @ North Grounds Rec (Outbound)', 'Massey voted John Paul Jones arena night stop' : 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', 'lee st. at UVA hospital' : 'Lee St @ UVA Hospital','14th street northwest of Virginia avenue' : '14th Street NW @ Virginia Ave', '14 street northwest at woodland street north bound' : '14th Street NW @ Wertland St (Northbound)', '14th street northwest art and street south southbound' : '14th Street NW @ Wertland St (Southbound)', 'alderman at facilities management' : 'Alderman Rd @ Facilities Mgmt', 'root of couch Dillard' : 'Alderman Rd @ Gooch/Dillard','alderman road at ohel dining hall' : 'Alderman Rd @ O-Hill Dining Hall', 'alderman road at stadium red' : 'Alderman Rd @ Stadium Rd', 'alderman road HC' : 'Alderman Road @ AFC', 'Arlington boulevard of massive no' : 'Arlington Blvd @ Massie Rd', 'Arlington boulevard of barracks read shopping center' : 'Arlington Blvd @ Barracks Rd Shopping Ctr',
              }


# Dictionaries to convert between route and ID
idToRoute = {'4003482': 'Special Route', '4003286': 'Northline', '4003290': 'Inner U-Loop', '4003294': 'Outer U-Loop', '4003298': 'Stadium / Hospital Shuttle', '4003302': 'Green Route', '4003306': 'Central Grounds Shuttle', '4003310': 'Hereford / IRC Express', '4003314': 'Colonnade Shuttle', '4003478': 'Nursing / Clinical Shuttle'}
routeToId = {'Special Route': '4003482', 'Northline': '4003286', 'Inner U-Loop': '4003290', 'Outer U-Loop': '4003294', 'Stadium / Hospital Shuttle': '4003298', 'Green Route': '4003302', 'Central Grounds Shuttle': '4003306', 'Hereford / IRC Express': '4003310', 'Colonnade Shuttle': '4003314', 'Nursing / Clinical Shuttle': '4003478'}

# A list of all UVA routes
routes = [
    'Special Route',
    'Northline',
    'Inner U-Loop',
    'Outer U-Loop',
    'Stadium / Hospital Shuttle',
    'Green Route',
    'Central Grounds Shuttle',
    'Hereford / IRC Express',
    'Colonnade Shuttle',
    'Nursing / Clinical Shuttle']

route_alias = {
    'Special Route' : 'Special Route',
    'Northline' : 'Northline', "north I'm" : 'Northline', 'north' : 'Northline', 'most 9' : 'Northline', 'north 1' : 'Northline', 'north side read that' : 'Northline', 'no sign' : 'Northline', 'north on' : 'Northline',
    'Inner U-Loop' : 'Inner U-Loop', 'N are you' : 'Inner U-Loop', 'N are' : 'Inner U-Loop', 'in you Uber' : 'Inner U-Loop', 'in are you lyft' :  'Inner U-Loop', 'enter you loop' : 'Inner U-Loop', 'in are you live' : 'Inner U-Loop', 'inner you Lutheran' : 'Inner U-Loop',
    'Outer U-Loop' : 'Outer U-Loop',
    'Stadium / Hospital Shuttle' : 'Stadium / Hospital Shuttle',
    'Green Route' : 'Green Route', 'green row ride' : 'Green Route',
    'Central Grounds Shuttle' : 'Central Grounds Shuttle', 'metro ground shut' : 'Central Grounds Shuttle', 'country ground should I' : 'Central Grounds Shuttle', 'metro train schedule' : 'Central Grounds Shuttle', 'metro grand shuttle' : 'Central Grounds Shuttle',
    'Hereford / IRC Express' : 'Hereford / IRC Express',
    'Colonnade Shuttle' : 'Colonnade Shuttle',
    'Nursing / Clinical Shuttle' : 'Nursing / Clinical Shuttle',

# training data 2 (inner)
     'N are you whip' : 'Inner U-Loop',  'any look and' : 'Inner U-Loop', 'N are you live' : 'Inner U-Loop', 'N I U look' : 'Inner U-Loop', 'NHLIT can I' : 'Inner U-Loop', 'new you look' : 'Inner U-Loop', 'new you look into' : 'Inner U-Loop', 'interlude can' : 'Inner U-Loop', 'N are you look' : 'Inner U-Loop', 'energy is' : 'Inner U-Loop', 'N are you loop' : 'Inner U-Loop',

# part 3
    'do you loop' : 'Outer U-Loop', 'how do you live' : 'Outer U-Loop', 'how do you loop' : 'Outer U-Loop', 'are you look' : 'Outer U-Loop',  'outer you live' : 'Outer U-Loop', 'outer you loop' : 'Outer U-Loop',


"stadium hospital shut I'm" : 'Stadium / Hospital Shuttle', 'stadium hospital shut' : 'Stadium / Hospital Shuttle',

'green rap' : 'Green Route', 'crane route' : 'Green Route', 'green red' : 'Green Route', 'green room' : 'Green Route', 'green route' : 'Green Route', 'green you' : 'Green Route',


# part 4
'hannaford I see expressed' : 'Hereford / IRC Express', 'half read iron chef express' : 'Hereford / IRC Express', 'half Ed Irish the express' : 'Hereford / IRC Express', 'half read I have' : 'Hereford / IRC Express', 'Hereford icx see' : 'Hereford / IRC Express', 'half for iron C express' : 'Hereford / IRC Express', 'Hereford piracy express' : 'Hereford / IRC Express', 'Hanford I see express' : 'Hereford / IRC Express', 'half food iris express' : 'Hereford / IRC Express', 'Hereford I see express' : 'Hereford / IRC Express', 'Hereford Irish express' : 'Hereford / IRC Express', 'Hereford iris express' : 'Hereford / IRC Express',

 'nursing clinical shut up' : 'Nursing / Clinical Shuttle', 'next thing clinical shuttle' : 'Nursing / Clinical Shuttle', 'nursing clinical shuttle' : 'Nursing / Clinical Shuttle',

}

#Info about each route (not currently used)
routeInfo = {'347': [{'description': '', 'short_name': '', 'route_id': '4003482', 'url': '', 'segments': [], 'is_active': False, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Special Route', 'stops': [], 'is_hidden': False, 'type': 'bus', 'color': 'ef00f7'}, {'description': '', 'short_name': '', 'route_id': '4003286', 'url': '', 'segments': [['4047699', 'backward'], ['4047703', 'forward'], ['4047863', 'backward'], ['4047871', 'backward'], ['4047907', 'forward'], ['4048279', 'forward'], ['4048303', 'backward'], ['4067319', 'forward'], ['4072239', 'backward'], ['4072239', 'forward'], ['4072271', 'backward'], ['4072271', 'forward'], ['4072275', 'backward'], ['4072275', 'forward'], ['4072331', 'forward'], ['4072339', 'forward'], ['4073443', 'backward'], ['4073443', 'forward'], ['4106959', 'forward'], ['4106979', 'backward'], ['4106979', 'forward'], ['4140169', 'backward'], ['4140171', 'backward'], ['4140557', 'backward'], ['4140557', 'forward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'backward'], ['4145831', 'forward'], ['4155663', 'backward'], ['4155667', 'backward'], ['4155669', 'backward'], ['4157073', 'backward'], ['4157073', 'forward'], ['4157075', 'backward'], ['4157075', 'forward'], ['4157077', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Northline', 'stops': ['4209054', '4209058', '4148110', '4137602', '4124058', '4123970', '4123810', '4123814', '4123962', '4123778', '4123774', '4123770', '4123978', '4123966', '4123982', '4123826', '4123842', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4123754', '4124042', '4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209048', '4209050', '4209066', '4209064', '4209062'], 'is_hidden': False, 'type': 'bus', 'color': '232b9e'}, {'description': '', 'short_name': '', 'route_id': '4003290', 'url': '', 'segments': [['4048519', 'forward'], ['4048535', 'forward'], ['4048539', 'backward'], ['4067275', 'forward'], ['4067339', 'forward'], ['4067359', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4072283', 'backward'], ['4072331', 'backward'], ['4072339', 'backward'], ['4074287', 'forward'], ['4074295', 'backward'], ['4074359', 'forward'], ['4076007', 'forward'], ['4082187', 'forward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106979', 'backward'], ['4106983', 'backward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'backward'], ['4145827', 'forward'], ['4145829', 'forward'], ['4145831', 'backward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Inner U-Loop', 'stops': ['4209054', '4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4178518', '4124078', '4123766', '4178522', '4178524', '4209048', '4209050'], 'is_hidden': False, 'type': 'bus', 'color': 'faca3c'}, {'description': '', 'short_name': '', 'route_id': '4003294', 'url': '', 'segments': [['4048515', 'forward'], ['4048531', 'backward'], ['4067275', 'backward'], ['4067339', 'backward'], ['4067359', 'backward'], ['4072159', 'backward'], ['4072163', 'backward'], ['4072271', 'forward'], ['4072275', 'forward'], ['4072283', 'forward'], ['4072335', 'forward'], ['4072339', 'forward'], ['4074311', 'backward'], ['4074359', 'backward'], ['4076007', 'backward'], ['4082187', 'backward'], ['4082191', 'backward'], ['4106963', 'backward'], ['4106979', 'forward'], ['4106983', 'forward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'forward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Outer U-Loop', 'stops': ['4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123910', '4123742', '4123734', '4128262', '4123958', '4124014', '4123874', '4123878', '4123870', '4124018', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4124082', '4123850', '4188128'], 'is_hidden': False, 'type': 'bus', 'color': 'fa880f'}, {'description': '', 'short_name': '', 'route_id': '4003298', 'url': '', 'segments': [['4048115', 'backward'], ['4048115', 'forward'], ['4048475', 'forward'], ['4067275', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072315', 'forward'], ['4072339', 'forward'], ['4074291', 'backward'], ['4074291', 'forward'], ['4074295', 'backward'], ['4074295', 'forward'], ['4076007', 'backward'], ['4082191', 'backward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106983', 'forward'], ['4107287', 'backward'], ['4107287', 'forward'], ['4146145', 'backward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Stadium / Hospital Shuttle', 'stops': ['4202642', '4123862', '4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123950', '4123938', '4123906', '4211480'], 'is_hidden': False, 'type': 'bus', 'color': 'ef83f2'}, {'description': '', 'short_name': '', 'route_id': '4003302', 'url': '', 'segments': [['4047703', 'backward'], ['4047703', 'forward'], ['4047743', 'forward'], ['4047863', 'backward'], ['4048303', 'backward'], ['4048411', 'forward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072319', 'backward'], ['4072319', 'forward'], ['4074291', 'backward'], ['4074291', 'forward'], ['4074295', 'backward'], ['4074295', 'forward'], ['4082191', 'backward'], ['4082191', 'forward'], ['4085703', 'backward'], ['4085703', 'forward'], ['4085963', 'forward'], ['4106963', 'forward'], ['4137001', 'backward'], ['4137003', 'forward'], ['4140557', 'backward'], ['4146145', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Green Route', 'stops': ['4124062', '4124058', '4123982', '4123826', '4123842', '4123818', '4123834', '4123902', '4123950', '4211480', '4123938', '4123906', '4123822', '4123838', '4123894', '4124050'], 'is_hidden': False, 'type': 'bus', 'color': '5bad18'}, {'description': '', 'short_name': '', 'route_id': '4003306', 'url': '', 'segments': [['4047703', 'backward'], ['4047743', 'forward'], ['4047863', 'backward'], ['4048199', 'backward'], ['4048303', 'backward'], ['4048323', 'forward'], ['4048411', 'forward'], ['4048431', 'forward'], ['4054475', 'backward'], ['4054475', 'forward'], ['4072203', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4073443', 'backward'], ['4073451', 'backward'], ['4073451', 'forward'], ['4085799', 'backward'], ['4085963', 'forward'], ['4106979', 'backward'], ['4140557', 'backward'], ['4145831', 'backward'], ['4157075', 'forward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Central Grounds Shuttle', 'stops': ['4124034', '4124026', '4123798', '4123790', '4124054', '4124058', '4123982', '4123826', '4123842', '4123894', '4123750', '4178522', '4178524', '4209046', '4209050', '4209054', '4209058', '4123794', '4123802', '4124030'], 'is_hidden': False, 'type': 'bus', 'color': 'f2f20a'}, {'description': '', 'short_name': '', 'route_id': '4003310', 'url': '', 'segments': [['4067319', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4072319', 'backward'], ['4072331', 'forward'], ['4072339', 'forward'], ['4073443', 'backward'], ['4082131', 'forward'], ['4106979', 'backward'], ['4140169', 'backward'], ['4140171', 'backward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'backward'], ['4145831', 'forward']], 'is_active': False, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Hereford / IRC Express', 'stops': ['4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209050', '4209054', '4209058', '4123818', '4123834', '4123998', '4123990', '4123758', '4123754', '4124042'], 'is_hidden': False, 'type': 'bus', 'color': 'f81110'}, {'description': '', 'short_name': '', 'route_id': '4003314', 'url': '', 'segments': [['4047699', 'forward'], ['4047863', 'backward'], ['4047907', 'forward'], ['4048199', 'forward'], ['4048291', 'backward'], ['4048291', 'forward'], ['4048431', 'forward'], ['4072203', 'backward'], ['4072271', 'forward'], ['4072275', 'forward'], ['4073443', 'forward'], ['4085963', 'forward'], ['4106971', 'forward'], ['4106975', 'backward'], ['4106979', 'forward'], ['4140557', 'backward'], ['4145831', 'forward'], ['4155663', 'backward'], ['4155667', 'backward'], ['4155669', 'backward'], ['4157073', 'backward'], ['4157073', 'forward'], ['4157075', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Colonnade Shuttle', 'stops': ['4209042', '4209040', '4123970', '4123810', '4123966', '4123982', '4123826', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4209044'], 'is_hidden': False, 'type': 'bus', 'color': '966b0e'}, {'description': '', 'short_name': '', 'route_id': '4003478', 'url': '', 'segments': [['4048515', 'forward'], ['4048535', 'forward'], ['4048539', 'backward'], ['4067275', 'forward'], ['4067339', 'forward'], ['4067359', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072331', 'backward'], ['4072339', 'backward'], ['4074287', 'forward'], ['4074295', 'backward'], ['4074359', 'forward'], ['4076007', 'forward'], ['4082187', 'forward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106983', 'backward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'backward'], ['4145829', 'forward']], 'is_active': False, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Nursing / Clinical Shuttle', 'stops': ['4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4123850', '4124078', '4123766'], 'is_hidden': False, 'type': 'bus', 'color': '937dc9'}]}

routeStops = {'Special Route': [], 'Northline': ['4209054', '4209058', '4148110', '4137602', '4209066', '4123970', '4123810', '4123814', '4123962', '4123778', '4123774', '4123770', '4123978', '4123966', '4124058', '4123982', '4123826', '4123842', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4123754', '4124042', '4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209048', '4209050', '4209064', '4209062'], 'Inner U-Loop': ['4209054', '4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4178518', '4124078', '4123766', '4178522', '4178524', '4209048', '4209050'], 'Outer U-Loop': ['4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123910', '4123742', '4123734', '4128262', '4123958', '4124014', '4123874', '4123878', '4123870', '4124018', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4124082', '4123850', '4188128'], 'Stadium / Hospital Shuttle': ['4202642', '4123862', '4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123950', '4123938', '4123906', '4211480'], 'Green Route': ['4124062', '4124058', '4123982', '4123826', '4123842', '4123818', '4123834', '4123902', '4123950', '4211480', '4123938', '4123906', '4123822', '4123838', '4123894', '4124050'], 'Central Grounds Shuttle': ['4124034', '4124026', '4123798', '4123790', '4124054', '4124058', '4123982', '4123826', '4123842', '4123894', '4123750', '4178522', '4178524', '4209046', '4209050', '4209054', '4209058', '4123794', '4123802', '4124030'], 'Hereford / IRC Express': ['4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209050', '4209054', '4209058', '4123818', '4123834', '4123998', '4123990', '4123758', '4123754', '4124042'], 'Colonnade Shuttle': ['4209042', '4209040', '4123970', '4123810', '4123966', '4123982', '4123826', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4209044'], 'Nursing / Clinical Shuttle': ['4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4123850', '4124078', '4123766']}

# Gets arrival estimate fow various queries each for route and stop at UVA
# The selected route & stop, if any, is the one which has the most in common with the provided search terms
# global routePhrase, stopPhrase, testRoute, testStop
def get_estimate(routeName, stopName, direction="forward", train=False):
    # global routePhrase, stopPhrase, testRoute, testStop

    data = {"error" : None, "train" : None}



    try:
        try:

            # print(routeName)


            bestRoute = routeToId[route_alias[(difflib.get_close_matches(routeName, route_alias, cutoff=0.5))[0]]]

            # print((difflib.get_close_matches(routeName, route_alias, cutoff=0.00))[0:3])
            # print(bestRoute)
            # experimental: ignores stop if it isnt on bestRoute
            # stopAliasList = (difflib.get_close_matches(stopName, stop_alias, cutoff=0.05))
            # print(stopAliasList)
            # for s in stopAliasList:
            #     if stopToId[stop_alias[s]] in routeStops[idToRoute[bestRoute]]:
            #         bestStop = stopToId[stop_alias[s]]
            #         break
            # print(stopName)

            # i = 0
            # bestStop = ""
            # while bestStop not in routeStops[idToRoute[bestRoute]]:
            #     bestStop = stopToId[stop_alias[(difflib.get_close_matches(stopName, stop_alias, cutoff=0.00))[i]]]
            #     i += 1

            bestStop = stopToId[stop_alias[(difflib.get_close_matches(stopName, stop_alias, cutoff=0.5))[0]]]

            # print((difflib.get_close_matches(stopName, stop_alias, cutoff=0.00))[0:3])
            # print(bestStop)
            # print(difflib.get_close_matches(stopName, stop_alias, cutoff=0.05))
            # for word in difflib.get_close_matches(stopName, stop_alias, cutoff=0.05):
            #     print(difflib.SequenceMatcher(None, stopName, word).ratio(), word, stopName)

            if(train):
                route_file = open('route_output.txt', "a")
                stop_file = open('stop_output.txt', "a")
                print(routeName)
                route_file.write("'" + routeName + "' : '")
                print(stopName)
                stop_file.write("'" + stopName + "' : '")
                route_file.close()
                stop_file.close()
                data["train"] = str(idToRoute[bestRoute] + " ; " + idToStop[bestStop])
                return data

            # print(difflib.get_close_matches(routeName, route_alias, cutoff=0.05))
            # for word in difflib.get_close_matches(routeName, route_alias, cutoff=0.05):
            #     print(difflib.SequenceMatcher(None, routeName, word).ratio(), word, routeName)

        except:
            data["error"] = "Hmm, I didn't quite get that. "
            return data

        # This section sends a GET request to the TransLoc Open API to get the arrival estimates
        arrivalEstimates_url = url + "arrival-estimates.json?agencies=347&callback=call&stops=" + bestStop + "&routes=" + bestRoute
        arrivalEstimatesResponse = requests.get(arrivalEstimates_url, headers={"X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()
        arrivalEstimates = []
        for result in arrivalEstimatesResponse["data"]:
            for arrival in result["arrivals"]:
                formatted_arrival = arrival["arrival_at"].replace("-04:00", "").replace("T", " ")
                wait_time = datetime.datetime.strptime(formatted_arrival, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
                arrivalEstimates.append(str(wait_time.seconds // 60 - 60))
        data.update({"arrivalEstimates" : arrivalEstimates, "route" : idToRoute[bestRoute], "stop" : idToStop[bestStop].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ", " street ")
    })




        return data

    # Returns an error message if something goes wrong
    except:
        data["error"] = "Hmm, I didn't quite get that. "
        return data


# print(get_estimate("northl  lion", 'simard court at compli hussy'))

# for r in stops:
#     print(r)

# stopName = "look brother gradient no 10 and have street northwest west bend"
# bestStop = stopToId[stop_alias[(difflib.get_close_matches(stopName, stop_alias, cutoff=0.00))[0]]]
# print((difflib.get_close_matches(stopName, stop_alias, cutoff=0.00))[0:3])
# print(bestStop)

# Check for bad keys
# for r in stop_alias:
#     if stop_alias[r] not in stops:
#         print(r)