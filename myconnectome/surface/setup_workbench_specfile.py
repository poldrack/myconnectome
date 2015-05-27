"""
create connectome workbench spec file
including all of the surface results
"""

import os,sys,glob
from myconnectome.utils.run_shell_cmd import run_shell_cmd
import myconnectome.utils.get_data

basedir=os.environ['MYCONNECTOME_DIR']

workbenchdir=os.environ['WORKBENCH_BIN_DIR']

specdir=os.path.join(basedir,'workbench')
if not os.path.exists(specdir):
    os.mkdir(specdir)

parcdir=os.path.join(basedir,'parcellation')
assert os.path.exists(parcdir)

retdir=os.path.join(basedir,'retinotopy')
if not os.path.exists(retdir):
    myconnectome.utils.get_data.get_s3_directory('retinotopy',retdir)
    
overwrite=True
verbose=True
   
specfile=os.path.join(specdir,'myconnectome.32k_fs_LR.wb.spec')
if os.path.exists(specfile) and not overwrite:
    print 'Specfile %s already exists'%specfile
    print 'Please remove before proceeding'
    sys.exit(0)
elif os.path.exists(specfile) and overwrite:
    os.remove(specfile)

fsdir=os.path.join(basedir,'fsaverage_LR32k')

assert os.path.exists(fsdir)

for ftype in ['label','shape','surf','mpr','func','ret']:
    if ftype=='func':
        giftifiles=glob.glob(os.path.join(parcdir,'*%s*ii*'%ftype))
    if ftype=='ret':
        giftifiles=glob.glob(os.path.join(retdir,'*%s*ii*'%ftype))
    else:
        giftifiles=glob.glob(os.path.join(fsdir,'*%s*ii*'%ftype))
    giftifiles.sort()
    
    for g in giftifiles:
        base=os.path.basename(g)
        if base.find('.L.')>-1 or base.find('_L_')>-1:
            hemis='CORTEX_LEFT'
        elif base.find('.R.')>-1 or base.find('_R_')>-1:
            hemis='CORTEX_RIGHT'
        else:
            hemis='INVALID'
            
        cmd='%s/wb_command -add-to-spec-file %s %s %s'%(workbenchdir,specfile,hemis,g)
        if verbose:
            print cmd
        run_shell_cmd(cmd)
        
