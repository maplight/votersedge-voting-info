This information is in DRAFT form.  Please update as you learn more about how it works.

The repository is connected to CircleCI.  When new changes are committed, CircleCI will run the compileJSON.py script.  That script converts the markdown files to JSON used by the Voter's Edge frontend.

From there, the content is uploaded to the Amazon S3 storage where our static content is housed.

Here's the original documentation on how to compile the JSON, which may be a little out of date:

# How to compile:
cd tools/scripts
./compileJSON.py
and git commit the changes.
