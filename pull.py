# execute git pull on all git repos
# if a pro - do simultaneously, and list off progress for each docker pull style

import os
from glob import glob
import subprocess

directories = glob(f'{os.getcwd()}/*/')

for directory in directories:
    if os.path.exists(f'{directory}/.git'):
        subprocess.Popen('git pull', shell=True, executable='/bin/bash', cwd=directory)
