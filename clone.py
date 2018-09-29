from getpass import getpass
import json
import multiprocessing
import os
import subprocess
import sys
import urllib3

def pull_repo(name):
    subprocess.run(f'git clone {name}', shell=True)

# get directory of script, check for certs
certs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'certs.pem')
if os.path.isfile(certs_path):
    # using https://certifi.io/ for example
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certs_path)
else:
    http = urllib3.PoolManager()

USERNAME = input('Username: ')
PASSWORD = getpass('Password: ')
ONE_TIME_PASSWORD = input('Enter 2FA code (enter if not using 2FA): ')
ORGANIZATION_NAME = os.path.split(os.getcwd())[-1]

headers = urllib3.util.make_headers(basic_auth=f'{USERNAME}:{PASSWORD}')
if ONE_TIME_PASSWORD:
    headers['X-Github-OTP'] = ONE_TIME_PASSWORD
headers['User-Agent'] = 'python3.urllib3'
resp = http.request('GET', f'https://api.github.com/orgs/{ORGANIZATION_NAME}/repos?per_page=1000', headers=headers) 

if resp.status != 200:
    print(f'Failed to get repos: {resp.data}')
    sys.exit(1)
else:
    repos = json.loads(resp.data)
    print(f'Cloning {len(repos)} repos')
    for repo in repos:
        p = multiprocessing.Process(target=pull_repo, args=(repo['ssh_url'],))
        p.start()
