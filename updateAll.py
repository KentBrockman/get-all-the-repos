#!/usr/bin/python

import os
import json
import urllib2
import subprocess

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

# Design: the directory name is the organization to pull repositories from
paths = os.getcwd().split(os.path.sep)
orgname = paths[len(paths) - 1]

print 'Get all repositories'
data = json.load(urllib2.urlopen("https://api.github.com/orgs/{0}/repos".format(orgname)))
allRepos = {}

for repo in data:
    allRepos[repo["name"]] = {"remoteUrl": repo["ssh_url"], "pulled": False}

localRepos = listdir_nohidden('.') 
for localRepo in localRepos:
    if os.path.isdir(localRepo):
        print localRepo

        command = "cd {0}".format(localRepo)
        os.chdir(localRepo)
        subprocess.call(["git pull"], shell=True)
        os.chdir("..")

        if allRepos.has_key(localRepo):
           allRepos[localRepo]["pulled"] = True
        else:
            print "Repository doesn't exist on github: {0}".format(localRepo)

if any(not f["pulled"] for f in allRepos.values()):
    print "You are missing the following repositories:"
    for k in allRepos:
        if allRepos[k]["pulled"] is False:
            print "Missing {0}, pulling it now...".format(k)
            subprocess.call(["git clone {0}".format(allRepos[k]["remoteUrl"])], shell=True)
