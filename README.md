Voter's Edge Voting info Guide
This is the document folder for the voting info guide for Voter's Edge.
These pages are stored in an online repository and can be synced by an administrator and published to the web.
-----------

Spec: https://docs.google.com/document/d/16rZfuKUD7lHf3IUesz7YzwL6eXwg7L0ttSb4FGlcmb8/edit


### State content folder
This contains all of the default content we provide, for each statewide election. 
* There are default pages, and state-wide override files. 
* The default pages should be written generically.

#### File names are as follows

name-of-url.jade  — This would apply to all states.
name-of-url.ca.jade — This would override the default page and be used on california only.

Example:

These files are present:
where-do-i-vote.jade
where-do-i-vote.ca.jade
where-do-i-vote.ny.jade

In this case, Illinois would use the default page.


### Page strucutre
The files are currently in Jade format. http://jade-lang.com/reference/code/

This includes a header, that speaks to the server, and the content within the section. You do not need to include the header title. That will be handled automatically.

### Development notes
* If Jade is too complicated, we can try using markdown.
* Jade uses abbreviated html syntax. It also accept HTML syntax. 


##### Url or anchor tag
controlled by the filename

##### Title
Is the header name
* Should be written in easy to understand language
* 8th grade reading level
* Max 6 words

##### Published
Controls if a page should be rendered as published or not. 

Values: 
Unpublished
Published

##### Weight
Controls the order of the content
Values
range from -100 to 100
Ex. -10
Values that are lower will appear lower than the other values.

##### Priority
Controls if a piece of content is a section or subsection

Values:
Major
Minor

##### No Override
Controls if content should not override state or default content. Will override by default.

Value:
Yes

###### Section
We have 6 sections. 
Weights for major sections control the sections

Values
Where do I vote?
Register to vote
Voting Basics
How do I vote?
When do I vote?
Other topics

### Files that will be "locked down" (changes reviewed)
* do not change these file names: file names that get linked to (this will be kept to a minimum)
    - my-polling-location-hours
    - my-election-office

### Overriding county specific content
Ex. Register to vote
name file

register-to-vote-county.ca.county_id.jade
- for now use the name of the county in the file, and we will make a lookup tool to get the county id.


### Image style guide

### Administration and publishing workflow
For now, the page templates are all set up, and are in a Dropbox folder which will be synced with a git repository in a private Bitbucket account.

### Spanish translation
Content in the 'es' folder should use the structure of the en folder as a model.
