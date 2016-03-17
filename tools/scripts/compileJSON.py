#!/usr/bin/python
import sys, os, datetime, time, json

# Script settings (pass in to script as args)
STATE = 'ca'
STATE_EA = STATE.upper()
LANGUAGE = 'en'

# DIRECTORY FOLDER MAPPINGS
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT = os.path.abspath(os.path.join(SCRIPT_ROOT, os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
STATE_ROOT = REPO_ROOT + "/voting-info/states/" + STATE
BUILD_ROOT = REPO_ROOT + "/build/" + STATE
ALL_ELECTIONS_ROOT = STATE_ROOT + "/all-elections/" + LANGUAGE
SINGLE_ELECTION_PATH = '2016-11-08'
SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/single-election/" + SINGLE_ELECTION_PATH + "/" + LANGUAGE
ELECTION_AUTHORITIES_ROOT = STATE_ROOT + "/election-authorities/" # ea name, language

# Load election authorities
def getElectionAuthorities(filePath):
    # http://maplight-api.elasticbeanstalk.com/api/election_authority/getListByState?state=ca&key=test
    # http://maplight-api-qa.us-west-2.elasticbeanstalk.com/api/election_authority/getListByState?state=ca&key=test
    # http://maplight-api.elasticbeanstalk.com/api/election_authority/getAllElectionAuthorities?&key=test
    # http://maplight-api-qa.us-west-2.elasticbeanstalk.com/api/election_authority/getAllElectionAuthorities?&key=test

    with open(filePath) as data_file:    
        data = json.load(data_file)
    # print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return data

# Get info about election authorities (currently, all states)
ea = getElectionAuthorities(PARENT_ROOT  + '/data/election-authorities.json')
state_election_authorities = ea['election_authority_data'][STATE_EA]

# Create list of files.
ca_single_file_list = []

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

def getFile(file):
    # print file['path']
    # Create file, write content, save, close.
    output = ''
    fout=open(file['path'],"r")
    output = fout.read()
    return output

# Load markdown files for all elections, for each voting content section.
all_elections_json = {}
all_elections_file_list = []
for section in votingContentState:
    all_elections_json[section] = []
    for file in [doc for doc in os.listdir(ALL_ELECTIONS_ROOT + '/' + section)
        if doc.endswith(".md")]:
            # print ALL_ELECTIONS_ROOT + '/' + section + '/' + file
            all_elections_file_list.append( {'path': ALL_ELECTIONS_ROOT + '/' + section + '/' + file, 'section': section})

for file_content in all_elections_file_list:
    content = getFile(file_content)
    all_elections_json[file_content['section']].append(content)

state_file = {
    'content' : {
        'stateData': {"votingInfo": all_elections_json},
    }
}

# Build state json file (no election authority info)
state_json_file_name = BUILD_ROOT + '/voting-info.' + STATE + '.' + LANGUAGE + '.json'

if not os.path.exists(state_json_file_name):
    open(state_json_file_name, 'w').close() 
fout=open(state_json_file_name,"w")
fout.seek(0)
fout.write(json.dumps(state_file))
fout.truncate()
fout.close()

# Get Election Authorities specific content
election_authorities_json = {}
election_authorities_file_list = []
election_authorities_groups = []
state_file_merged = {}

# Process each election authority.
for ea in state_election_authorities:
    # Build filename
    ea_file_name = ea['election_authority_id'] + '-' + ea['name'].rstrip().lower().replace(' ', '-')
    ea_file_path = ELECTION_AUTHORITIES_ROOT + '/' + ea_file_name
    election_authorities_file_list = []
    election_authorities_json = {}

    # Process each section
    for section in votingContentState:
        election_authorities_json[section] = []
        
        # If markdown files exist for the state
        if os.path.exists(ea_file_path):
            if os.path.exists(ea_file_path + '/' + section):
                for file in [doc for doc in os.listdir(ea_file_path + '/' + section)
                    if doc.endswith(".md")]:
                        election_authorities_file_list.append( {'path': ALL_ELECTIONS_ROOT + '/' + section + '/' + file, 'section': section})

            for file_content in election_authorities_file_list:
                content = getFile(file_content)
                # print content
                election_authorities_json[file_content['section']].append(content)

            state_file_merged = {
                'content' : {
                    'stateData': {"votingInfo": all_elections_json},
                    'electionAuthorityData': {"votingInfo": election_authorities_json},
                }
            }

            json_file_name = json_path_output + '/voting-info.' + STATE + '.' + LANGUAGE + '-' + ea_file_name + '.json'
            if not os.path.exists(json_file_name):
                open(json_file_name, 'w').close() 
            fout=open(json_file_name,"w")
            fout.seek(0)
            fout.write(json.dumps(state_file_merged))
            fout.truncate()
            fout.close()
        else: 
            json_file_name = BUILD_ROOT + '/voting-info.' + STATE + '.' + LANGUAGE + '-' + ea_file_name + '.json'
            if not os.path.exists(json_file_name):
                open(json_file_name, 'w').close() 
            fout=open(json_file_name,"w")
            fout.seek(0)
            fout.write(json.dumps(state_file))
            fout.truncate()
            fout.close()



print "Done."
sys.exit()
