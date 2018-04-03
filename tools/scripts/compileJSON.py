#!/usr/bin/python
import sys, os, datetime, time, json

exec(open("compileJSON.ca.py").read())
exec(open("compileJSON.ca.es.py").read())
exec(open("compileJSON.ny.py").read())
exec(open("compileJSON.ny.es.py").read())
exec(open("compileJSON.il.py").read())
exec(open("compileJSON.il.es.py").read())

print ("Done all scripts")
sys.exit()
