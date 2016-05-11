#!/usr/bin/python
import sys, os, datetime, time, json

# Script settings (pass in to script as args)
STATE = 'il'
STATE_EA = STATE.upper()
LANGUAGE = 'es'
STATE_AREA_NAME = "State of Illinois"

# DIRECTORY FOLDER MAPPINGS
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
PARENT_ROOT = os.path.abspath(os.path.join(SCRIPT_ROOT, os.pardir))
REPO_ROOT = os.path.abspath(os.path.join(PARENT_ROOT, os.pardir))
STATE_ROOT = REPO_ROOT + "/voting-info/states/" + STATE

ALL_ELECTIONS_ROOT = STATE_ROOT + "/state-all-elections/" + LANGUAGE
STATE_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/state-single-election/"
ELECTION_AUTHORITIES_ROOT = STATE_ROOT + "/election-authorities/"

#STATE_ROOT = REPO_ROOT + "/voting-info/states/" + STATE
BUILD_ROOT = REPO_ROOT + "/json/" + STATE
#ALL_ELECTIONS_ROOT = STATE_ROOT + "/all-elections/" + LANGUAGE
#STATE_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/single-election/" # election, language
#ELECTION_AUTHORITIES_ROOT = STATE_ROOT + "/election-authorities/" # ea, language
ELECTION_AUTHORITIES_SINGLE_ELECTIONS_ROOT = STATE_ROOT + "/election-authorities/" # ea, election, language

# http://maplight-api.elasticbeanstalk.com/api/election_authority/getListByState?state=ca&key=test
# http://maplight-api-qa.us-west-2.elasticbeanstalk.com/api/election_authority/getListByState?state=ca&key=test
# http://maplight-api.elasticbeanstalk.com/api/election_authority/getAllElectionAuthorities?&key=test
# http://maplight-api-qa.us-west-2.elasticbeanstalk.com/api/election_authority/getAllElectionAuthorities?&key=test

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
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    return data

def getFile(file):
    output = ''
    fout=open(file['path'],"r")
    output = fout.read()
    return output

# Get info about election authorities (currently, all states)
election_authorities = getJSON(PARENT_ROOT  + '/data/election-authorities.json')
election_authorities_in_state = election_authorities['election_authority_data'][STATE_EA]

elections = getJSON(PARENT_ROOT  + '/data/elections.' + STATE + '.json')

county_elections = elections['election_authorities']['is_county']
not_county_elections = elections['election_authorities']['not_county']
state_elections = elections['election_authorities']['state']
election_dates = elections['election_dates']

state_election_authorities = getJSON(PARENT_ROOT  + '/data/state-election-authorities.json')
state_election_authority = state_election_authorities[STATE]

# @TODO update real election data for a state
# @TODO handle "not county" election authorities

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

# Build state-specific data for each election.
state_single_elections_json = {}
for election in election_dates:
    election_date = election['election_date']
    if (election_date):
        state_single_election_json = {}
        state_single_election_file_list = []
        for section in votingContentState:
            state_single_election_json[section] = []
            state_single_election_section = STATE_SINGLE_ELECTIONS_ROOT + election_date + '/' + LANGUAGE + '/' + section
            # Get files in each section, add as a flat hash
            if os.path.exists(state_single_election_section):
                for file in [doc for doc in os.listdir(state_single_election_section)
                    if doc.endswith(".md")]:
                        print file
                        state_single_election_file_list.append( {'path': state_single_election_section + '/' + file, 'section': section})
        # Process the file list for this election.
        for state_single_election_file_content in state_single_election_file_list:
            state_single_election_content = getFile(state_single_election_file_content)
            state_single_election_json[state_single_election_file_content['section']].append(state_single_election_content)
        state_single_elections_json[election_date] = state_single_election_json

# Build state data hash
state_file = {
    'content' : {
        'stateData': {"votingInfo": all_elections_json},
        'stateDataSingleElections': {"votingInfo": state_single_elections_json}
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

# --------------------
# Get & Build Election Authorities specific content
election_authorities_json = {}
election_authorities_file_list = []
election_authorities_groups = []
state_file_merged = {}

# Process each election authority.
for election_authority in election_authorities_in_state:
    # Build filename
    election_authority_file_name = election_authority['election_authority_id'] + '-' + election_authority['name'].rstrip().lower().replace(' ', '-')
    # election_authority_file_path = ELECTION_AUTHORITIES_ROOT + election_authority_file_name
    election_authority_file_path = ELECTION_AUTHORITIES_ROOT + election_authority_file_name + '/all-elections/' + LANGUAGE
    # election_authority_file_root = ELECTION_AUTHORITIES_ROOT + election_authority_file_name
    election_authorities_file_list = []
    election_authorities_json = {}

    # Process each section for the election authority
    for section in votingContentState:
        election_authorities_json[section] = []
        # If markdown files exist for the state
        if os.path.exists(election_authority_file_path):

            if os.path.exists(election_authority_file_path + '/' + section):
                print election_authority_file_path + '/' + section
                for file in [doc for doc in os.listdir(election_authority_file_path + '/' + section)
                    if doc.endswith(".md")]:
                        # print election_authority_file_path + '/' + section + '/' + file
                        election_authorities_file_list.append( {'path': election_authority_file_path + '/' + section + '/' + file, 'section': section})

    for file_content in election_authorities_file_list:
        content = getFile(file_content)
        election_authorities_json[file_content['section']].append(content)

    # Build election-authority-specific data for each election.
    election_authority_single_elections_json = {}
    if (election_authority['area']):
        if (election_authority['area'] in county_elections):
            for election in county_elections[election_authority['area']]['election']:
                election_date = election['election_date']
                if (election_date):
                    election_authority_single_election_json = {}
                    election_authority_single_election_file_list = []
                    for section in votingContentState:
                        election_authority_single_election_json[section] = []
                        election_authority_single_election_section = ELECTION_AUTHORITIES_ROOT + '/single-election/' + election_date + '/' + LANGUAGE + '/' + section
                        # Get files in each section, add as a flat hash
                        if os.path.exists(election_authority_single_election_section):
                            for file in [doc for doc in os.listdir(election_authority_single_election_section)
                                if doc.endswith(".md")]:
                                    # print file
                                    election_authority_single_election_file_list.append( {'path': election_authority_single_election_section + '/' + file, 'section': section})
                    # Process the file list for this election.
                    for election_authority_single_election_file_content in election_authority_single_election_file_list:
                        election_authority_single_election_content = getFile(election_authority_single_election_file_content)
                        election_authority_single_election_json[election_authority_single_election_file_content['section']].append(election_authority_single_election_content)
                    election_authority_single_elections_json[election_date] = election_authority_single_election_json

    # Build election authority file, merging all state data & creating one file for the election authority with all elections
    state_file_merged = {
        'content' : {
            'stateData': {"votingInfo": all_elections_json},
            'stateDataSingleElections': {"votingInfo": state_single_elections_json},
            'electionAuthorityData': {"votingInfo": election_authorities_json},
            'electionAuthorityDataSingleElections': {"votingInfo": election_authority_single_elections_json},
        }
    }
    json_file_name = BUILD_ROOT + '/voting-info.' + STATE + '.' + LANGUAGE + '-' + election_authority_file_name + '.json'
    if not os.path.exists(json_file_name):
        open(json_file_name, 'w').close()
    fout=open(json_file_name,"w")
    fout.seek(0)
    fout.write(json.dumps(state_file_merged))
    fout.truncate()
    fout.close()



    # else:
    #     # ??? what's this?
    #     json_file_name = BUILD_ROOT + '/voting-info.' + STATE + '.' + LANGUAGE + '-' + election_authority_file_name + '.json'
    #     if not os.path.exists(json_file_name):
    #         open(json_file_name, 'w').close()
    #     fout=open(json_file_name,"w")
    #     fout.seek(0)
    #     fout.write(json.dumps(state_file))
    #     fout.truncate()
    #     fout.close()




print "Done: " + STATE
sys.exit()
