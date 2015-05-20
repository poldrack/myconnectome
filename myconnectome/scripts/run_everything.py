"""
main script to run all analyses for MyConnectome paper
"""

import os,sys

try:
    import myconnectome
except:
    print 'you first need to install the myconnectome python package'
    sys.exit(0)

from myconnectome.utils import run_shell_cmd

good_to_go=True
# check for environment variables

## 1 for required, 0 for recommended
envvars={'MYCONNECTOME_DIR':1,'WORKBENCH_BIN_DIR':1,'DAVID_EMAIL':0}

messages=[]
for v in envvars.keys():
    try:
        os.environ[v]
    except:
        if envvars[v]:
            good_to_go=False
            messages.append('environment variable %s must be specified'%v)
        else:
            print 'environment variable %s recommended but not required'%v
if good_to_go:
    print 'all environment variables present'


# check for suitable version of R
whichR=run_shell_cmd.run_shell_cmd('which R 2> /dev/null')
if len(whichR)==0:
    good_to_go=False
    messages.append('you need to install R, version 3.0 or newer')
else:
    rver=run_shell_cmd.run_shell_cmd('R --version 2> /dev/null')
    rversion=rver[0].split(' ')[2]
    print 'Found R version',rversion
    if int(rversion.split('.')[0]) <3:
        good_to_go=False
        messages.append('you need to install R, version 3.0 or newer')

whichmatlab=run_shell_cmd.run_shell_cmd('which matlab 2> /dev/null')
if len(whichmatlab)==0:
    print 'MATLAB was not detected - precomputed results will be downloaded'


if not good_to_go:
    print 'Problems detected'
    for m in messages:
        print m

    sys.exit(0)

# otherwise, run all of the scripts
filepath=os.path.dirname(os.path.abspath(__file__))
basepath=os.path.dirname(filepath)


execfile('%s/scripts/rsfmri_analysis.py'%basepath)

execfile('%s/scripts/rnaseq_analysis.py'%basepath)

execfile('%s/scripts/metabolomic_analysis.py'%basepath)

execfile('%s/scripts/timeseries_analysis.py'%basepath)
