#!/usr/bin/python

import os
import json
import urllib2
import subprocess

def listdir_nohidden(path):
        for f in os.listdir(path):
                    if not f.startswith('.'):
                                    yield f

print 'Get all repositories'
data = json.load(urllib2.urlopen("https://api.github.com/orgs/openaginitiative/repos"))
remoteRepos = {}

for repo in data:
    remoteRepos[repo["name"]] = {"remoteUrl": repo["ssh_url"], "pulled": False}

items = listdir_nohidden('.') 
for item in items:
    if os.path.isdir(item):
        print item

        command = "cd {0}".format(item)
        os.chdir(item)
        subprocess.call(["git pull"], shell=True)
        os.chdir("..")

        if remoteRepos.has_key(item):
           remoteRepos[item]["pulled"] = True
        else:
            print "Repository doesn't exist on github: {0}".format(item)

if any(not f["pulled"] for f in remoteRepos.values()):
    print "You are missing the following repositories:"
    for k in remoteRepos:
        if remoteRepos[k]["pulled"] is False:
            print "Missing {0}, pulling it now...".format(k)
            subprocess.call(["git clone {0}".format(remoteRepos[k]["remoteUrl"])], shell=True)
