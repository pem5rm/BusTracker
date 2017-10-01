import requests
import datetime
import logging
import difflib
import operator

url = "https://transloc-api-1-2.p.mashape.com/"

# UVA agency ID = 347

# Data
idToStop = {'4123734': '14th Street NW @ John St', '4123738': '14th Street NW @ Virginia Ave', '4123742': '14th Street NW @ Wertland St (Northbound)', '4123746': '14th Street NW @ Wertland St (Southbound)', '4123750': 'Alderman Rd @ Facilities Mgmt', '4123754': 'Alderman Rd @ Gooch/Dillard', '4123758': 'Alderman Rd @ O-Hill Dining Hall', '4123762': 'Alderman Rd @ Stadium Rd', '4123766': 'Alderman Road @ AFC', '4123770': 'Arlington Blvd @ Massie Rd', '4123774': 'Arlington Blvd @ Barracks Rd Shopping Ctr', '4123778': 'Arlington Blvd @ Arlington Ct', '4123790': 'Copeley Rd @ Massie Rd (Inbound)', '4123794': 'Copeley Rd @ Massie Rd (Outbound)', '4123798': 'Copeley Rd @ Seymour Ct (Inbound)', '4123802': 'Copeley Rd @ Seymour Ct (Outbound)', '4123810': 'Duffy Blvd @ Darden', '4123814': 'Duffy Blvd @ North Grounds Rec', '4123818': 'Emmet St @ Alumni Hall', '4123822': 'Emmet St @ Central Grounds Garage', '4123826': 'Emmet St @ Goodwin Bridge', '4123834': 'Emmet St @ Ruffner Hall', '4123838': 'Emmet St @ Snyder Tennis Courts', '4123842': 'Emmet / Ivy Garage (EIG)', '4123850': 'George Welsh Way @ Bryant Hall (Outbound)', '4123854': 'George Welsh Way @ SAB', '4123858': 'George Welsh Way @ Scott Stadium', '4123862': 'George Welsh Way @ Stadium West Shelf', '4123866': 'Grady Ave @ 16th St', '4123870': 'Grady Ave @ Preston Pl', '4123874': 'Grady Ave @ 10 ½ St NW (Westbound)', '4123878': 'Grady Ave @ 14th St', '4123882': 'Hereford Dr @ Johnson House', '4123886': 'Hereford Dr @ Kellogg Dorm', '4123890': 'Hereford Dr @ Runk Dining Hall', '4123894': 'Ivy Rd @ Emmet / Ivy Garage', '4123902': 'Jefferson Park Ave @ Brandon Ave', '4123906': 'Jefferson Park Ave @ Cabell Hall', '4123910': 'Jefferson Park Ave @ Pinn Hall', '4123914': 'Jefferson Park Ave @ Kent Terrace', '4123918': 'Jefferson Park Ave @ Maury Ave', '4123922': 'Jefferson Park Ave @ Montebello Circle', '4123926': 'Jefferson Park Ave @ Observatory Ave', '4123930': 'Jefferson Park Ave @ Shamrock Rd (Northbound)', '4123934': 'Jefferson Park Ave @ Shamrock Rd (Southbound)', '4123938': 'Jefferson Park Ave @ UVA Hospital', '4123942': 'Jefferson Park Ave @ Valley Rd', '4123946': 'Jefferson Park Ave @ Woodrow St', '4123950': 'Lane Rd @ MR-5', '4123958': 'Madison Ave @ Preston Ave', '4123962': 'Massie Rd @ Copeley Student Housing', '4123966': 'Massie Rd @ Faulkner Housing (Inbound)', '4123970': 'Massie Rd @ Faulkner Housing (Outbound)', '4123978': 'Massie Rd @ Law School', '4123982': 'Massie Rd @ U-Hall East Lot', '4123990': 'McCormick Rd @ McCormick Residence Hall', '4123994': 'McCormick Rd @ O-Hill Dining Hall', '4123998': 'McCormick Rd @ Physics Building', '4124006': 'Mimosa Dr (Inbound)', '4124014': 'Preston Ave @ Washington Park', '4124018': 'Rugby Rd @ 203 Rugby Rd', '4124022': 'Rugby Rd @ Beta Bridge (Outbound)', '4124026': 'Seymour Ct (Inbound)', '4124030': 'Seymour Ct (Outbound)', '4124034': 'Seymour Ct @ Copeley Hill Housing', '4124038': 'Stadium Rd @ Appletree Rd', '4124042': 'Stadium Rd @ Runk Dining Hall', '4124050': 'U-Hall @ Cage Lot', '4124054': 'U-Hall @ Copeley Rd', '4124058': 'U-Hall @ Massie Rd', '4124062': 'U-Hall @ West Entrance', '4124074': 'University Ave @ Jefferson Park Ave', '4124078': 'Whitehead Rd @ Engineering School (Inbound)', '4124082': 'Whitehead Rd @ Engineering School (Outbound)', '4128262': 'Madison Ave @ Grady Ave', '4137602': 'Massie Rd @ John Paul Jones Arena', '4148110': 'Emmet St @ Lambeth Housing', '4178518': 'George Welsh Way @ Bryant Hall (Inbound)', '4178522': 'McCormick Rd @ Gilmer Hall', '4178524': 'McCormick Rd @ Thornton Hall', '4188128': 'Mimosa Dr (Outbound)', '4202642': 'Stadium Rd @ Stadium Garage', '4209040': 'Colonnade Dr @ Ivy Rd', '4209042': 'Colonnade Dr @ University Heights', '4209044': 'Ivy Rd @ Foods of All Nations', '4209046': 'McCormick Rd @ Brown College (NIGHT STOP)', '4209048': 'McCormick Rd @ Clark Hall (NIGHT STOP)', '4209050': 'McCormick Rd @ Garrett Hall', '4209052': 'McCormick Rd @ Monroe Hall', '4209054': 'McCormick Rd @ UVA Chapel', '4209056': 'University Ave @ Snyder Tennis Courts', '4209058': "University Ave @ Carr's Hill Field", '4209060': 'McCormick Rd @ Alderman Library', '4209062': 'Massie Rd @ North Grounds Rec (Inbound)', '4209064': 'Massie Rd @ North Grounds Rec (Outbound)', '4209066': 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', '4211480': 'Lee St @ UVA Hospital'}
stopToId = {'14th Street NW @ John St': '4123734', '14th Street NW @ Virginia Ave': '4123738', '14th Street NW @ Wertland St (Northbound)': '4123742', '14th Street NW @ Wertland St (Southbound)': '4123746', 'Alderman Rd @ Facilities Mgmt': '4123750', 'Alderman Rd @ Gooch/Dillard': '4123754', 'Alderman Rd @ O-Hill Dining Hall': '4123758', 'Alderman Rd @ Stadium Rd': '4123762', 'Alderman Road @ AFC': '4123766', 'Arlington Blvd @ Massie Rd': '4123770', 'Arlington Blvd @ Barracks Rd Shopping Ctr': '4123774', 'Arlington Blvd @ Arlington Ct': '4123778', 'Copeley Rd @ Massie Rd (Inbound)': '4123790', 'Copeley Rd @ Massie Rd (Outbound)': '4123794', 'Copeley Rd @ Seymour Ct (Inbound)': '4123798', 'Copeley Rd @ Seymour Ct (Outbound)': '4123802', 'Duffy Blvd @ Darden': '4123810', 'Duffy Blvd @ North Grounds Rec': '4123814', 'Emmet St @ Alumni Hall': '4123818', 'Emmet St @ Central Grounds Garage': '4123822', 'Emmet St @ Goodwin Bridge': '4123826', 'Emmet St @ Ruffner Hall': '4123834', 'Emmet St @ Snyder Tennis Courts': '4123838', 'Emmet / Ivy Garage (EIG)': '4123842', 'George Welsh Way @ Bryant Hall (Outbound)': '4123850', 'George Welsh Way @ SAB': '4123854', 'George Welsh Way @ Scott Stadium': '4123858', 'George Welsh Way @ Stadium West Shelf': '4123862', 'Grady Ave @ 16th St': '4123866', 'Grady Ave @ Preston Pl': '4123870', 'Grady Ave @ 10 ½ St NW (Westbound)': '4123874', 'Grady Ave @ 14th St': '4123878', 'Hereford Dr @ Johnson House': '4123882', 'Hereford Dr @ Kellogg Dorm': '4123886', 'Hereford Dr @ Runk Dining Hall': '4123890', 'Ivy Rd @ Emmet / Ivy Garage': '4123894', 'Jefferson Park Ave @ Brandon Ave': '4123902', 'Jefferson Park Ave @ Cabell Hall': '4123906', 'Jefferson Park Ave @ Pinn Hall': '4123910', 'Jefferson Park Ave @ Kent Terrace': '4123914', 'Jefferson Park Ave @ Maury Ave': '4123918', 'Jefferson Park Ave @ Montebello Circle': '4123922', 'Jefferson Park Ave @ Observatory Ave': '4123926', 'Jefferson Park Ave @ Shamrock Rd (Northbound)': '4123930', 'Jefferson Park Ave @ Shamrock Rd (Southbound)': '4123934', 'Jefferson Park Ave @ UVA Hospital': '4123938', 'Jefferson Park Ave @ Valley Rd': '4123942', 'Jefferson Park Ave @ Woodrow St': '4123946', 'Lane Rd @ MR-5': '4123950', 'Madison Ave @ Preston Ave': '4123958', 'Massie Rd @ Copeley Student Housing': '4123962', 'Massie Rd @ Faulkner Housing (Inbound)': '4123966', 'Massie Rd @ Faulkner Housing (Outbound)': '4123970', 'Massie Rd @ Law School': '4123978', 'Massie Rd @ U-Hall East Lot': '4123982', 'McCormick Rd @ McCormick Residence Hall': '4123990', 'McCormick Rd @ O-Hill Dining Hall': '4123994', 'McCormick Rd @ Physics Building': '4123998', 'Mimosa Dr (Inbound)': '4124006', 'Preston Ave @ Washington Park': '4124014', 'Rugby Rd @ 203 Rugby Rd': '4124018', 'Rugby Rd @ Beta Bridge (Outbound)': '4124022', 'Seymour Ct (Inbound)': '4124026', 'Seymour Ct (Outbound)': '4124030', 'Seymour Ct @ Copeley Hill Housing': '4124034', 'Stadium Rd @ Appletree Rd': '4124038', 'Stadium Rd @ Runk Dining Hall': '4124042', 'U-Hall @ Cage Lot': '4124050', 'U-Hall @ Copeley Rd': '4124054', 'U-Hall @ Massie Rd': '4124058', 'U-Hall @ West Entrance': '4124062', 'University Ave @ Jefferson Park Ave': '4124074', 'Whitehead Rd @ Engineering School (Inbound)': '4124078', 'Whitehead Rd @ Engineering School (Outbound)': '4124082', 'Madison Ave @ Grady Ave': '4128262', 'Massie Rd @ John Paul Jones Arena': '4137602', 'Emmet St @ Lambeth Housing': '4148110', 'George Welsh Way @ Bryant Hall (Inbound)': '4178518', 'McCormick Rd @ Gilmer Hall': '4178522', 'McCormick Rd @ Thornton Hall': '4178524', 'Mimosa Dr (Outbound)': '4188128', 'Stadium Rd @ Stadium Garage': '4202642', 'Colonnade Dr @ Ivy Rd': '4209040', 'Colonnade Dr @ University Heights': '4209042', 'Ivy Rd @ Foods of All Nations': '4209044', 'McCormick Rd @ Brown College (NIGHT STOP)': '4209046', 'McCormick Rd @ Clark Hall (NIGHT STOP)': '4209048', 'McCormick Rd @ Garrett Hall': '4209050', 'McCormick Rd @ Monroe Hall': '4209052', 'McCormick Rd @ UVA Chapel': '4209054', 'University Ave @ Snyder Tennis Courts': '4209056', "University Ave @ Carr's Hill Field": '4209058', 'McCormick Rd @ Alderman Library': '4209060', 'Massie Rd @ North Grounds Rec (Inbound)': '4209062', 'Massie Rd @ North Grounds Rec (Outbound)': '4209064', 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)': '4209066', 'Lee St @ UVA Hospital': '4211480'}

stops  = ['14th Street NW @ John St', '14th Street NW @ Virginia Ave', '14th Street NW @ Wertland St (Northbound)', '14th Street NW @ Wertland St (Southbound)', 'Alderman Rd @ Facilities Mgmt', 'Alderman Rd @ Gooch/Dillard', 'Alderman Rd @ O-Hill Dining Hall', 'Alderman Rd @ Stadium Rd', 'Alderman Road @ AFC', 'Arlington Blvd @ Massie Rd', 'Arlington Blvd @ Barracks Rd Shopping Ctr', 'Arlington Blvd @ Arlington Ct', 'Copeley Rd @ Massie Rd (Inbound)', 'Copeley Rd @ Massie Rd (Outbound)', 'Copeley Rd @ Seymour Ct (Inbound)', 'Copeley Rd @ Seymour Ct (Outbound)', 'Duffy Blvd @ Darden', 'Duffy Blvd @ North Grounds Rec', 'Emmet St @ Alumni Hall', 'Emmet St @ Central Grounds Garage', 'Emmet St @ Goodwin Bridge', 'Emmet St @ Ruffner Hall', 'Emmet St @ Snyder Tennis Courts', 'Emmet / Ivy Garage (EIG)', 'George Welsh Way @ Bryant Hall (Outbound)', 'George Welsh Way @ SAB', 'George Welsh Way @ Scott Stadium', 'George Welsh Way @ Stadium West Shelf', 'Grady Ave @ 16th St', 'Grady Ave @ Preston Pl', 'Grady Ave @ 10 ½ St NW (Westbound)', 'Grady Ave @ 14th St', 'Hereford Dr @ Johnson House', 'Hereford Dr @ Kellogg Dorm', 'Hereford Dr @ Runk Dining Hall', 'Ivy Rd @ Emmet / Ivy Garage', 'Jefferson Park Ave @ Brandon Ave', 'Jefferson Park Ave @ Cabell Hall', 'Jefferson Park Ave @ Pinn Hall', 'Jefferson Park Ave @ Kent Terrace', 'Jefferson Park Ave @ Maury Ave', 'Jefferson Park Ave @ Montebello Circle', 'Jefferson Park Ave @ Observatory Ave', 'Jefferson Park Ave @ Shamrock Rd (Northbound)', 'Jefferson Park Ave @ Shamrock Rd (Southbound)', 'Jefferson Park Ave @ UVA Hospital', 'Jefferson Park Ave @ Valley Rd', 'Jefferson Park Ave @ Woodrow St', 'Lane Rd @ MR-5', 'Madison Ave @ Preston Ave', 'Massie Rd @ Copeley Student Housing', 'Massie Rd @ Faulkner Housing (Inbound)', 'Massie Rd @ Faulkner Housing (Outbound)', 'Massie Rd @ Law School', 'Massie Rd @ U-Hall East Lot', 'McCormick Rd @ McCormick Residence Hall', 'McCormick Rd @ O-Hill Dining Hall', 'McCormick Rd @ Physics Building', 'Mimosa Dr (Inbound)', 'Preston Ave @ Washington Park', 'Rugby Rd @ 203 Rugby Rd', 'Rugby Rd @ Beta Bridge (Outbound)', 'Seymour Ct (Inbound)', 'Seymour Ct (Outbound)', 'Seymour Ct @ Copeley Hill Housing', 'Stadium Rd @ Appletree Rd', 'Stadium Rd @ Runk Dining Hall', 'U-Hall @ Cage Lot', 'U-Hall @ Copeley Rd', 'U-Hall @ Massie Rd', 'U-Hall @ West Entrance', 'University Ave @ Jefferson Park Ave', 'Whitehead Rd @ Engineering School (Inbound)', 'Whitehead Rd @ Engineering School (Outbound)', 'Madison Ave @ Grady Ave', 'Massie Rd @ John Paul Jones Arena', 'Emmet St @ Lambeth Housing', 'George Welsh Way @ Bryant Hall (Inbound)', 'McCormick Rd @ Gilmer Hall', 'McCormick Rd @ Thornton Hall', 'Mimosa Dr (Outbound)', 'Stadium Rd @ Stadium Garage', 'Colonnade Dr @ Ivy Rd', 'Colonnade Dr @ University Heights', 'Ivy Rd @ Foods of All Nations', 'McCormick Rd @ Brown College (NIGHT STOP)', 'McCormick Rd @ Clark Hall (NIGHT STOP)', 'McCormick Rd @ Garrett Hall', 'McCormick Rd @ Monroe Hall', 'McCormick Rd @ UVA Chapel', 'University Ave @ Snyder Tennis Courts', "University Ave @ Carr's Hill Field", 'McCormick Rd @ Alderman Library', 'Massie Rd @ North Grounds Rec (Inbound)', 'Massie Rd @ North Grounds Rec (Outbound)', 'Massie Rd @ John Paul Jones Arena (NIGHT STOP)', 'Lee St @ UVA Hospital']

idToRoute = {'4003482': 'Special Route', '4003286': 'Northline', '4003290': 'Inner U-Loop', '4003294': 'Outer U-Loop', '4003298': 'Stadium / Hospital Shuttle', '4003302': 'Green Route', '4003306': 'Central Grounds Shuttle', '4003310': 'Hereford / IRC Express', '4003314': 'Colonnade Shuttle', '4003478': 'Nursing / Clinical Shuttle'}
routeToId = {'Special Route': '4003482', 'Northline': '4003286', 'Inner U-Loop': '4003290', 'Outer U-Loop': '4003294', 'Stadium / Hospital Shuttle': '4003298', 'Green Route': '4003302', 'Central Grounds Shuttle': '4003306', 'Hereford / IRC Express': '4003310', 'Colonnade Shuttle': '4003314', 'Nursing / Clinical Shuttle': '4003478'}

routes = ['Special Route', 'Northline', 'Inner U-Loop', 'Outer U-Loop', 'Stadium / Hospital Shuttle', 'Green Route', 'Central Grounds Shuttle', 'Hereford / IRC Express', 'Colonnade Shuttle', 'Nursing / Clinical Shuttle']


routeInfo = {'347': [{'description': '', 'short_name': '', 'route_id': '4003482', 'url': '', 'segments': [], 'is_active': False, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Special Route', 'stops': [], 'is_hidden': False, 'type': 'bus', 'color': 'ef00f7'}, {'description': '', 'short_name': '', 'route_id': '4003286', 'url': '', 'segments': [['4047699', 'backward'], ['4047703', 'forward'], ['4047863', 'backward'], ['4047871', 'backward'], ['4047907', 'forward'], ['4048279', 'forward'], ['4048303', 'backward'], ['4067319', 'forward'], ['4072239', 'backward'], ['4072239', 'forward'], ['4072271', 'backward'], ['4072271', 'forward'], ['4072275', 'backward'], ['4072275', 'forward'], ['4072331', 'forward'], ['4072339', 'forward'], ['4073443', 'backward'], ['4073443', 'forward'], ['4106959', 'forward'], ['4106979', 'backward'], ['4106979', 'forward'], ['4140169', 'backward'], ['4140171', 'backward'], ['4140557', 'backward'], ['4140557', 'forward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'backward'], ['4145831', 'forward'], ['4155663', 'backward'], ['4155667', 'backward'], ['4155669', 'backward'], ['4157073', 'backward'], ['4157073', 'forward'], ['4157075', 'backward'], ['4157075', 'forward'], ['4157077', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Northline', 'stops': ['4209054', '4209058', '4148110', '4137602', '4124058', '4123970', '4123810', '4123814', '4123962', '4123778', '4123774', '4123770', '4123978', '4123966', '4123982', '4123826', '4123842', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4123754', '4124042', '4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209048', '4209050', '4209066', '4209064', '4209062'], 'is_hidden': False, 'type': 'bus', 'color': '232b9e'}, {'description': '', 'short_name': '', 'route_id': '4003290', 'url': '', 'segments': [['4048519', 'forward'], ['4048535', 'forward'], ['4048539', 'backward'], ['4067275', 'forward'], ['4067339', 'forward'], ['4067359', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4072283', 'backward'], ['4072331', 'backward'], ['4072339', 'backward'], ['4074287', 'forward'], ['4074295', 'backward'], ['4074359', 'forward'], ['4076007', 'forward'], ['4082187', 'forward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106979', 'backward'], ['4106983', 'backward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'backward'], ['4145827', 'forward'], ['4145829', 'forward'], ['4145831', 'backward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Inner U-Loop', 'stops': ['4209054', '4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4178518', '4124078', '4123766', '4178522', '4178524', '4209048', '4209050'], 'is_hidden': False, 'type': 'bus', 'color': 'faca3c'}, {'description': '', 'short_name': '', 'route_id': '4003294', 'url': '', 'segments': [['4048515', 'forward'], ['4048531', 'backward'], ['4067275', 'backward'], ['4067339', 'backward'], ['4067359', 'backward'], ['4072159', 'backward'], ['4072163', 'backward'], ['4072271', 'forward'], ['4072275', 'forward'], ['4072283', 'forward'], ['4072335', 'forward'], ['4072339', 'forward'], ['4074311', 'backward'], ['4074359', 'backward'], ['4076007', 'backward'], ['4082187', 'backward'], ['4082191', 'backward'], ['4106963', 'backward'], ['4106979', 'forward'], ['4106983', 'forward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'forward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Outer U-Loop', 'stops': ['4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123910', '4123742', '4123734', '4128262', '4123958', '4124014', '4123874', '4123878', '4123870', '4124018', '4209060', '4209052', '4209046', '4123998', '4123990', '4123758', '4124082', '4123850', '4188128'], 'is_hidden': False, 'type': 'bus', 'color': 'fa880f'}, {'description': '', 'short_name': '', 'route_id': '4003298', 'url': '', 'segments': [['4048115', 'backward'], ['4048115', 'forward'], ['4048475', 'forward'], ['4067275', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072315', 'forward'], ['4072339', 'forward'], ['4074291', 'backward'], ['4074291', 'forward'], ['4074295', 'backward'], ['4074295', 'forward'], ['4076007', 'backward'], ['4082191', 'backward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106983', 'forward'], ['4107287', 'backward'], ['4107287', 'forward'], ['4146145', 'backward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Stadium / Hospital Shuttle', 'stops': ['4202642', '4123862', '4123858', '4123754', '4123926', '4123930', '4123914', '4123942', '4123902', '4123950', '4123938', '4123906', '4211480'], 'is_hidden': False, 'type': 'bus', 'color': 'ef83f2'}, {'description': '', 'short_name': '', 'route_id': '4003302', 'url': '', 'segments': [['4047703', 'backward'], ['4047703', 'forward'], ['4047743', 'forward'], ['4047863', 'backward'], ['4048303', 'backward'], ['4048411', 'forward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072319', 'backward'], ['4072319', 'forward'], ['4074291', 'backward'], ['4074291', 'forward'], ['4074295', 'backward'], ['4074295', 'forward'], ['4082191', 'backward'], ['4082191', 'forward'], ['4085703', 'backward'], ['4085703', 'forward'], ['4085963', 'forward'], ['4106963', 'forward'], ['4137001', 'backward'], ['4137003', 'forward'], ['4140557', 'backward'], ['4146145', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Green Route', 'stops': ['4124062', '4124058', '4123982', '4123826', '4123842', '4123818', '4123834', '4123902', '4123950', '4211480', '4123938', '4123906', '4123822', '4123838', '4123894', '4124050'], 'is_hidden': False, 'type': 'bus', 'color': '5bad18'}, {'description': '', 'short_name': '', 'route_id': '4003306', 'url': '', 'segments': [['4047703', 'backward'], ['4047743', 'forward'], ['4047863', 'backward'], ['4048199', 'backward'], ['4048303', 'backward'], ['4048323', 'forward'], ['4048411', 'forward'], ['4048431', 'forward'], ['4054475', 'backward'], ['4054475', 'forward'], ['4072203', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4073443', 'backward'], ['4073451', 'backward'], ['4073451', 'forward'], ['4085799', 'backward'], ['4085963', 'forward'], ['4106979', 'backward'], ['4140557', 'backward'], ['4145831', 'backward'], ['4157075', 'forward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Central Grounds Shuttle', 'stops': ['4124034', '4124026', '4123798', '4123790', '4124054', '4124058', '4123982', '4123826', '4123842', '4123894', '4123750', '4178522', '4178524', '4209046', '4209050', '4209054', '4209058', '4123794', '4123802', '4124030'], 'is_hidden': False, 'type': 'bus', 'color': 'f2f20a'}, {'description': '', 'short_name': '', 'route_id': '4003310', 'url': '', 'segments': [['4067319', 'forward'], ['4072271', 'backward'], ['4072275', 'backward'], ['4072319', 'backward'], ['4072331', 'forward'], ['4072339', 'forward'], ['4073443', 'backward'], ['4082131', 'forward'], ['4106979', 'backward'], ['4140169', 'backward'], ['4140171', 'backward'], ['4145827', 'backward'], ['4145829', 'backward'], ['4145831', 'backward'], ['4145831', 'forward']], 'is_active': False, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Hereford / IRC Express', 'stops': ['4123890', '4123882', '4123886', '4123994', '4178522', '4178524', '4209050', '4209054', '4209058', '4123818', '4123834', '4123998', '4123990', '4123758', '4123754', '4124042'], 'is_hidden': False, 'type': 'bus', 'color': 'f81110'}, {'description': '', 'short_name': '', 'route_id': '4003314', 'url': '', 'segments': [['4047699', 'forward'], ['4047863', 'backward'], ['4047907', 'forward'], ['4048199', 'forward'], ['4048291', 'backward'], ['4048291', 'forward'], ['4048431', 'forward'], ['4072203', 'backward'], ['4072271', 'forward'], ['4072275', 'forward'], ['4073443', 'forward'], ['4085963', 'forward'], ['4106971', 'forward'], ['4106975', 'backward'], ['4106979', 'forward'], ['4140557', 'backward'], ['4145831', 'forward'], ['4155663', 'backward'], ['4155667', 'backward'], ['4155669', 'backward'], ['4157073', 'backward'], ['4157073', 'forward'], ['4157075', 'backward'], ['4157077', 'forward']], 'is_active': True, 'agency_id': 347, 'text_color': '000000', 'long_name': 'Colonnade Shuttle', 'stops': ['4209042', '4209040', '4123970', '4123810', '4123966', '4123982', '4123826', '4209056', '4209060', '4209052', '4209046', '4123998', '4123990', '4209044'], 'is_hidden': False, 'type': 'bus', 'color': '966b0e'}, {'description': '', 'short_name': '', 'route_id': '4003478', 'url': '', 'segments': [['4048515', 'forward'], ['4048535', 'forward'], ['4048539', 'backward'], ['4067275', 'forward'], ['4067339', 'forward'], ['4067359', 'backward'], ['4072159', 'forward'], ['4072163', 'forward'], ['4072331', 'backward'], ['4072339', 'backward'], ['4074287', 'forward'], ['4074295', 'backward'], ['4074359', 'forward'], ['4076007', 'forward'], ['4082187', 'forward'], ['4082191', 'forward'], ['4106963', 'forward'], ['4106983', 'backward'], ['4106987', 'forward'], ['4106991', 'forward'], ['4106995', 'backward'], ['4145829', 'forward']], 'is_active': False, 'agency_id': 347, 'text_color': 'FFFFFF', 'long_name': 'Nursing / Clinical Shuttle', 'stops': ['4124022', '4123866', '4128262', '4123958', '4124014', '4123874', '4123878', '4123738', '4123746', '4124074', '4123938', '4123906', '4123946', '4123922', '4123934', '4123918', '4124006', '4124038', '4123762', '4123854', '4123850', '4124078', '4123766'], 'is_hidden': False, 'type': 'bus', 'color': '937dc9'}]}






# gets arrival estimate fow various queries with up to three phrases each for route and stop
# the selected route & stop, if any, is the one which has the most in common with the provded search terms
def get_estimate(routeName, stopName, direction="forward"):
    data = {"error" : None}
    routeResults = {}
    for route in routes:
        for word in routeName.split():
            if (len(difflib.get_close_matches(word, set(route.split()))) > 0):
                if(route not in routeResults):
                    routeResults[route] = 0
                else:
                    routeResults[route] += 1


    stopResults = {}
    for stop in stops:
        for word in stopName.split():
            if (len(difflib.get_close_matches(word, set(stop.split()))) > 0):
                if(stop not in stopResults):
                    stopResults[stop] = 0
                else:
                    stopResults[stop] += 1

    print(stopResults)
    print(routeResults)
    if (len(stopResults.keys())) > 0 and (len(routeResults.keys())) > 0:

        bestRoutes = []
        maxMatches = routeResults[max(routeResults, key=lambda k: routeResults[k])]
        for route in routeResults:
            if routeResults[route] == maxMatches:
                bestRoutes.append(route)

        bestStops = []
        maxMatches = stopResults[max(stopResults, key=lambda k: stopResults[k])]
        for stop in stopResults:
            if stopResults[stop] == maxMatches:
                bestStops.append(stop)

        print(len(bestRoutes))
        print(len(bestStops))
        print("test1")
        if (len(bestStops) > 1) and (len(bestRoutes) > 1):
            print("test2")

            data["error"] = "Did you mean " + ", ".join(bestStops[0:-1]) + ", or " + bestStops[-1] + ". Also, did you mean " + ", ".join(bestRoutes[0:-1]) + ", or " + bestRoutes[-1] + "."
            data["error"] = data["error"].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ", " street ")
            return data
        elif (len(bestStops) > 1):
            print("test3")
            data["error"] = "Did you mean " + ", ".join(bestStops[0:-1]) + ", or " + bestStops[-1] + "."
            data["error"] = data["error"].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ", " street ")
            return data
        elif (len(bestRoutes) > 1):
            print("test4")
            data["error"] = "Did you mean " + ", ".join(bestRoutes[0:-1]) + ", or " + bestRoutes[-1] + "."
            data["error"] = data["error"].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ", " street ")
            return data

        else:
            bestStop = stopToId[bestStops[0]]
            bestRoute = routeToId[bestRoutes[0]]
    elif len(stopResults) > 0:
        data["error"] = "Sorry, I couldn't find that route."
        return data
    elif len(routeResults) > 0:
        data["error"] = "Sorry, I couldn't find that stop."
        return data
    else:
        data["error"] = "Sorry, I couldn't find that route or that stop."
        return data

    # just taking first result for now, will improve search later
    arrivalEstimates_url = url + "arrival-estimates.json?agencies=347&callback=call&stops=" + bestStop + "&routes=" + bestRoute
    arrivalEstimatesResponse = requests.get(arrivalEstimates_url, headers={"X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()
    # print(arrivalEstimatesResponse)
    arrivalEstimates = []
    for result in arrivalEstimatesResponse["data"]:
        for arrival in result["arrivals"]:
            formatted_arrival = arrival["arrival_at"].replace("-04:00", "").replace("T", " ")
            # print(formatted_arrival)
            wait_time = datetime.datetime.strptime(formatted_arrival, "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()
            arrivalEstimates.append(wait_time.seconds // 60)
    data.update({"arrivalEstimates" : arrivalEstimates, "route" : idToRoute[bestRoute], "stop" : idToStop[bestStop].replace(" Dr ", " drive ").replace("NW", "northwest").replace(" St ", " street ")
})
    return data



# def get_agency():
#     agencies_url = url + "agencies.json?agencies=347&callback=call"
#     agencies_response = requests.get(agencies_url, headers={"X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()
#     return agencies_response



def get_routes():
    routes_url = url + "routes.json?agencies=347&callback=call"
    routes_response = requests.get(routes_url, headers={"X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()
    return routes_response



def get_stops():
    stop_url = url + "stops.json?agencies=347&callback=call"
    stop_response = requests.get(stop_url, headers={"X-Mashape-Key": "7zef4m39KxmshI8Z2wZHynIctO7ap1YpFbmjsnL1PAIUpeybSu"}).json()
    return stop_response

# get_agency()
# get_routes()

# Create Stops Dictionary
# stopsResults = get_stops()
# stopDict = {}
# stop_list = []
# for stop in stopsResults["data"]:
#     stopDict[stop["name"]] = stop["stop_id"]
#     stop_list.append(stop["name"])
#     # print(stop["name"] + " : " + stop["stop_id"])
# print(stopDict)
# stop_list_phrases = []
# for stop in stop_list:
#     for word in stop.split():
#         if word not in stop_list_phrases:
#             stop_list_phrases.append(word.replace("(", "").replace(")", ""))
# # print(stop_list_phrases)
# stop_list_phrases2 = []
# for s in stop_list_phrases:
#     if s not in stop_list_phrases2:
#         stop_list_phrases2.append(s)
# stop_list_phrases = sorted(stop_list_phrases2)
# for s in stop_list_phrases:
#     print(s)



# Create Route Dictionary
# routeResults = get_routes()
# print(routeResults)
# routeDict = {}
# route_list = []
# for route in routeResults["data"]["347"]:
#     routeDict[route["long_name"]] = route["route_id"]
#     route_list.append(route["long_name"])
#     # print(stop["name"] + " : " + stop["stop_id"])
# print(routeDict)
# # print(route_list)
# route_list2 = []
# for s in route_list:
#     for word in s.split():
#         if word not in route_list2:
#             route_list2.append(word)
# route_list2 = sorted(route_list2)
#
# for r in route_list2:
#     print(r)
# print(get_estimate("Northline", "Runk"))