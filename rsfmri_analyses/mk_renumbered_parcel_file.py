# renumber parcels so that CARET will treat them properly
# originally called mk_parcelfile.py
import sys

import nibabel.gifti.giftiio
import nibabel,numpy
from run_shell_cmd import run_shell_cmd

stdir='/Users/poldrack/data/selftracking'
basedir=os.path.join(stdir,'parcellation')

communitydtseries=os.path.join(basedir,'parcels_LR_assignments_minsize5_regularized_consensus_powercolors.dtseries.nii')
lhinfomapfile=os.path.join(basedir,'parcel_L_consensus_new.func.gii')
rhinfomapfile=os.path.join(basedir,'parcel_R_consensus_new.func.gii')
if not os.path.exists(lhinfomapfile):
    cmd='/Applications/fmri_progs/workbench/macosx64_apps/wb_command.app/Contents/MacOS/wb_command -cifti-separate  %s COLUMN -metric CORTEX_LEFT %s'%(communitydtseries,lhinfomapfile)
    run_shell_cmd(cmd)
if not os.path.exists(rhinfomapfile):
    cmd='/Applications/fmri_progs/workbench/macosx64_apps/wb_command.app/Contents/MacOS/wb_command -cifti-separate  %s COLUMN -metric CORTEX_RIGHT %s'%(communitydtseries,rhinfomapfile)
    run_shell_cmd(cmd)


#rh=nibabel.load('parcels.R.nii.gz').get_data()
#lh=nibabel.load('parcels.L.nii.gz').get_data()
lhs=nibabel.gifti.giftiio.read('/Users/poldrack/data/selftracking/parcellation/84sub_333_all_startpos50_presmooth_L_threshperc0.45_minparcel20watershedmerge_0.45.func.gii')
rhs=nibabel.gifti.giftiio.read('/Users/poldrack/data/selftracking/parcellation/84sub_333_all_startpos50_presmooth_R_threshperc0.45_minparcel20watershedmerge_0.45.func.gii')
#lhu=numpy.unique(lh)
lhsu=numpy.unique(lhs.darrays[0].data)
rhsu=numpy.unique(rhs.darrays[0].data)


origdata=lhs.darrays[0].data


intent=lhs.darrays[0].intent
datatype=lhs.darrays[0].datatype
for i in range(len(lhs.darrays[0].data)):
    lhs.darrays[0].data[i]=numpy.where(lhsu==origdata[i])[0][0]

nibabel.gifti.giftiio.write(lhs,'/Users/poldrack/data/selftracking/parcellation/all_selected_L_new_parcel_renumbered.func.gii')

origdata=rhs.darrays[0].data

intent=rhs.darrays[0].intent
datatype=rhs.darrays[0].datatype
rh_zeros=numpy.where(rhs.darrays[0].data==0)
for i in range(len(rhs.darrays[0].data)):
    rhs.darrays[0].data[i]=numpy.where(rhsu==origdata[i])[0][0]+ numpy.max(lhs.darrays[0].data)
rhs.darrays[0].data[rh_zeros]=0
nibabel.gifti.giftiio.write(rhs,'/Users/poldrack/data/selftracking/parcellation/all_selected_R_new_parcel_renumbered.func.gii')

cmd='wb_command -set-structure /Users/poldrack/data/selftracking/parcellation/all_selected_L_new_parcel_renumbered.func.gii CORTEX_LEFT'
cmd='wb_command -set-structure /Users/poldrack/data/selftracking/parcellation/all_selected_R_new_parcel_renumbered.func.gii CORTEX_RIGHT'
