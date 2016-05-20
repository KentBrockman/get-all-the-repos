#!/usr/bin/python

import os
import json
import urllib2
import subprocess

print 'Get all repositories'
data = urllib2.urlopen("https://api.github.com/orgs/openaginitiative/repos")
repositories = json.load(data)
repos = {}

for repo in repositories:
     repos[repo["name"]] = False

items = os.listdir('.') 
for item in items:
    if os.path.isdir(item):
        command = "cd {0}".format(item)
        os.chdir(item)
        subprocess.call(["git up"], shell=True)
        os.chdir("..")
        repos[item] = True

if False in repos.values():
    print "You are missing the following repositories:"
    for repo in repos:
        if repos[repo] is False:
            print repo
