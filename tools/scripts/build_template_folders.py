#!/usr/bin/python
import sys, os, datetime, time, json, shutil

# Script settings (pass in to script as args)
STATE = 'ca'
STATE_EA = STATE.upper()
LANGUAGE = 'en'
STATE_AREA_NAME = 'State of California'

# DIRECTORY FOLDER MAPPINGS
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT = os.path.abspath(os.path.join(SCRIPT_ROOT, os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
STATE_ROOT = REPO_ROOT + "/voting-info-new/states/" + STATE
SRC_ROOT = REPO_ROOT + "/voting-info-new/" + STATE
STATE_TEMPLATES = REPO_ROOT + "/_templates/state-defaults"
ELECTION_AUTHORITY_TEMPLATES = REPO_ROOT + "/_templates/election-authority-defaults"
ALL_ELECTIONS_ROOT = STATE_ROOT + "/all-elections/" + LANGUAGE
STATE_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/single-election/" # election, language
ELECTION_AUTHORITIES_ROOT = STATE_ROOT + "/election-authorities/" # ea, language
ELECTION_AUTHORITIES_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/election-authorities/" # ea, election, language

# Folder structure all sections.
votingContentState = {
  'my-polling-place': {'icon': 'my-polling-place', 'Major': [], 'Minor': []},
  'register-to-vote': {'icon': 'register-to-vote', 'Major': [], 'Minor': []},
  'ways-to-vote': {'icon': 'ways-to-vote', 'Major': [], 'Minor': []},
  'voting-basics': {'icon': 'voting-basics', 'Major': [], 'Minor': []},
  'important-dates-deadlines': {'icon': 'important-dates-deadlines', 'Major': [], 'Minor': []},
  'my-rights-as-a-voter': {'icon': 'my-rights-as-a-voter', 'Major': [], 'Minor': []},
  'more-voting-info': {'icon': 'more-voting-info', 'Major': [], 'Minor': []},
  #'election-office': {'icon': 'election-office', 'Major': [], 'Minor': []},
  'election-office-contact': {'icon': 'election-office-contact', 'Major': [], 'Minor': []},
};

def getJSON(filePath):
    with open(filePath) as data_file:    
        data = json.load(data_file)
    return data

def getFile(file):
    # print file['path']
    # Create file, write content, save, close.
    output = ''
    fout=open(file['path'],"r")
    output = fout.read()
    return output

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def copy(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

# Get info about election authorities (currently, all states)
election_authorities = getJSON(PARENT_ROOT  + '/data/election-authorities.json')
election_authorities_in_state = election_authorities['election_authority_data'][STATE_EA]

elections = getJSON(PARENT_ROOT  + '/data/elections.' + STATE + '.json')
county_elections = elections['election_authorities']['is_county']
not_county_elections = elections['election_authorities']['not_county']

state_election_authorities = getJSON(PARENT_ROOT  + '/data/state-election-authorities.json')
state_election_authority = state_election_authorities[STATE]

# Find non-existing folders, add markdown folder template as new files.
# Build state-specific data for each election.

for election in not_county_elections[STATE_AREA_NAME]['election']:
    election_date = election['election_date']

    if (election_date):
      if not os.path.exists(STATE_SINGLE_ELECTIONS_ROOT + election_date):
        # Make folder for single election
        os.makedirs(STATE_SINGLE_ELECTIONS_ROOT + election_date)
        copy(STATE_TEMPLATES, STATE_SINGLE_ELECTIONS_ROOT + election_date)
        # for section in votingContentState:
        #     state_single_election_section = STATE_SINGLE_ELECTIONS_ROOT + election_date + '/' + LANGUAGE + '/' + section
            
        #     # Get files in each section, add as a flat hash
        #     if not os.path.exists(state_single_election_section):
        #         os.makedirs(state_single_election_section)
        #         # Make new directory
        #         # Add markdown files



# # --------------------
# # Get & Build Election Authorities specific content
# election_authorities_json = {}
# election_authorities_file_list = []
# election_authorities_groups = []
# state_file_merged = {}

# # Process each election authority.
# for election_authority in election_authorities_in_state:
#     # Build filename
#     election_authority_file_name = election_authority['election_authority_id'] + '-' + election_authority['name'].rstrip().lower().replace(' ', '-')
#     election_authority_file_path = ELECTION_AUTHORITIES_ROOT + '/' + election_authority_file_name
#     election_authorities_file_list = []
#     election_authorities_json = {}

#     # Process each section for the election authority
#     for section in votingContentState:
#         election_authorities_json[section] = []
        
#         # If markdown files exist for the state
#         if os.path.exists(election_authority_file_path):
#             if os.path.exists(election_authority_file_path + '/' + section):
#                 for file in [doc for doc in os.listdir(election_authority_file_path + '/' + section)
#                     if doc.endswith(".md")]:
#                         election_authorities_file_list.append( {'path': ALL_ELECTIONS_ROOT + '/' + section + '/' + file, 'section': section})

#             for file_content in election_authorities_file_list:
#                 content = getFile(file_content)
#                 election_authorities_json[file_content['section']].append(content)

#             json_file_name = json_path_output + '/voting-info.' + STATE + '.' + LANGUAGE + '-' + election_authority_file_name + '.json'
#             if not os.path.exists(json_file_name):
#                 open(json_file_name, 'w').close() 
#             fout=open(json_file_name,"w")
#             fout.seek(0)
#             fout.write(json.dumps(state_file_merged))
#             fout.truncate()
#             fout.close()

#             # Build election-authority-specific data for each election.
#             election_authority_single_elections_json = {}

#             for election in county_elections[election_authority]['election']:
#                 election_date = election['election_date']
#                 if (election_date):
#                     election_authority_single_election_json = {}
#                     election_authority_single_election_file_list = []
#                     for section in votingContentState:
#                         election_authority_single_election_json[section] = []
#                         election_authority_single_election_section = ELECTION_AUTHORITIES_SINGLE_ELECTIONS_ROOT + election_date + '/' + LANGUAGE + '/' + section
#                         # Get files in each section, add as a flat hash
#                         if os.path.exists(election_authority_single_election_section):
#                             for file in [doc for doc in os.listdir(election_authority_single_election_section)
#                                 if doc.endswith(".md")]:
#                                     # print file
#                                     election_authority_single_election_file_list.append( {'path': election_authority_single_election_section + '/' + file, 'section': section})
#                     # Process the file list for this election.
#                     for election_authority_single_election_file_content in election_authority_single_election_file_list:
#                         election_authority_single_election_content = getFile(election_authority_single_election_file_content)
#                         election_authority_single_election_json[election_authority_single_election_file_content['section']].append(election_authority_single_election_content)
#                     election_authority_single_elections_json[election_date] = election_authority_single_election_json

#             # Build election authority file, merging all state data & creating one file for the election authority with all elections
#             state_file_merged = {
#                 'content' : {
#                     'stateData': {"votingInfo": all_elections_json},
#                     'stateDataSingleElections': {"votingInfo": state_single_elections_json}
#                     'electionAuthorityData': {"votingInfo": election_authorities_json},
#                     'electionAuthorityDataSingleElections': {"votingInfo": election_authority_single_elections_json},
#                 }
#             }




print "Done building new file folders: " + STATE
sys.exit()
