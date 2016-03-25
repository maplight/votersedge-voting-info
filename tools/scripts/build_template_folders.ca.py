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

ALL_ELECTIONS_ROOT = STATE_ROOT + "/state-all-elections/"
STATE_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/state-single-election/"
ELECTION_AUTHORITIES_ROOT = STATE_ROOT + "/election-authorities/"

# Only copy single election & election authority.
SINGLE_ELECTION_TEMPLATES = REPO_ROOT + "/_templates/" + STATE + "/state-single-election"
ELECTION_AUTHORITY_TEMPLATES = REPO_ROOT + "/_templates/" + STATE + "/election-authorities"

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
state_elections = elections['election_authorities']['state']

state_election_authorities = getJSON(PARENT_ROOT  + '/data/state-election-authorities.json')
state_election_authority = state_election_authorities[STATE]

# Find non-existing folders, add markdown folder template as new files.
# Build state-specific data for each election.
for election in state_elections[STATE_AREA_NAME]['election']:
    election_date = election['election_date']

    if (election_date):
      if not os.path.exists(STATE_SINGLE_ELECTIONS_ROOT + election_date):
        # Make folder for single election
        os.makedirs(STATE_SINGLE_ELECTIONS_ROOT + election_date)
        copy(SINGLE_ELECTION_TEMPLATES, STATE_SINGLE_ELECTIONS_ROOT + election_date)

# --------------------
# Get & Build Election Authorities folders
# Process each election authority.
for election_authority in election_authorities_in_state:
    # Build filename
    election_authority_file_name = election_authority['election_authority_id'] + '-' + election_authority['name'].rstrip().lower().replace(' ', '-')
    election_authority_file_path = ELECTION_AUTHORITIES_ROOT + '/' + election_authority_file_name
    if not os.path.exists(ELECTION_AUTHORITIES_ROOT + '/' + election_authority_file_name):
      # Make folder for election authority
      os.makedirs(ELECTION_AUTHORITIES_ROOT + '/' + election_authority_file_name)
      copy(ELECTION_AUTHORITY_TEMPLATES, ELECTION_AUTHORITIES_ROOT + '/' + election_authority_file_name)
    
    single_election_folder = ELECTION_AUTHORITIES_ROOT + election_authority_file_name + '/single-election/'
    if os.path.exists(ELECTION_AUTHORITIES_ROOT + election_authority_file_name):
        if (election_authority['area']):
                if (election_authority['area'] in county_elections):
                    for election in county_elections[election_authority['area']]['election']:
                        election_date = election['election_date']
                        if (election_date):
                            if not os.path.exists(single_election_folder + election_date):
                                # shutil.rmtree(single_election_folder + election_date)
                                # Make folder for single election
                                print single_election_folder
                                os.makedirs(single_election_folder + election_date)
                                copy(SINGLE_ELECTION_TEMPLATES, single_election_folder + election_date)

print "Done building new file folders: " + STATE
sys.exit()
