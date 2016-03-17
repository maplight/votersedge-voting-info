### How to build JSON from markdown
This repository contains organized markdown formats with a particular data model. 

The markdown files are then compiled into a lot of json files for every county in each state. This makes it faster to deliver the information. These JSON files are used by the votersedge app and further processed before delivery to voters.

### Git hooks
To run either after push or commit, whenever something is saved on Prose.io (or otherwise committed.)

post-commit -> .git/hooks/post-commit  (runs a python script)
