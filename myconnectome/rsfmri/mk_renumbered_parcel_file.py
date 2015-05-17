# renumber parcels so that CARET will treat them properly
# originally called mk_parcelfile.py
import sys,os

import nibabel.gifti.giftiio
import nibabel,numpy
from run_shell_cmd import run_shell_cmd
from myconnectome.utils.set_structure import set_structure

def mk_renumbered_parcel_file():
    stdir=os.environ['MYCONNECTOME_DIR']
    workbench_bin=os.environ['WORKBENCH_BIN_DIR']
    
    basedir=os.path.join(stdir,'parcellation')
    
    communitydtseries=os.path.join(basedir,'parcels_LR_assignments_minsize5_regularized_consensus_powercolors.dtseries.nii')
    lhinfomapfile=os.path.join(basedir,'parcel_L_consensus_new.func.gii')
    rhinfomapfile=os.path.join(basedir,'parcel_R_consensus_new.func.gii')
    if not os.path.exists(lhinfomapfile):
        cmd='%s/wb_command -cifti-separate  %s COLUMN -metric CORTEX_LEFT %s'%(workbench_bin,communitydtseries,lhinfomapfile)
        run_shell_cmd(cmd)
    if not os.path.exists(rhinfomapfile):
        cmd='%s/wb_command -cifti-separate  %s COLUMN -metric CORTEX_RIGHT %s'%(workbench_bin,communitydtseries,rhinfomapfile)
        run_shell_cmd(cmd)
    
    
    lhs=nibabel.gifti.giftiio.read(os.path.join(basedir,'84sub_333_all_startpos50_presmooth_L_threshperc0.45_minparcel20watershedmerge_0.45.func.gii'))
    rhs=nibabel.gifti.giftiio.read(os.path.join(basedir,'84sub_333_all_startpos50_presmooth_R_threshperc0.45_minparcel20watershedmerge_0.45.func.gii'))
    lhsu=numpy.unique(lhs.darrays[0].data)
    rhsu=numpy.unique(rhs.darrays[0].data)
    
    
    origdata=lhs.darrays[0].data
    
    
    intent=lhs.darrays[0].intent
    datatype=lhs.darrays[0].datatype
    for i in range(len(lhs.darrays[0].data)):
        lhs.darrays[0].data[i]=numpy.where(lhsu==origdata[i])[0][0]
    
    nibabel.gifti.giftiio.write(lhs,os.path.join(basedir,'all_selected_L_new_parcel_renumbered.func.gii'))
    
    origdata=rhs.darrays[0].data
    
    intent=rhs.darrays[0].intent
    datatype=rhs.darrays[0].datatype
    rh_zeros=numpy.where(rhs.darrays[0].data==0)
    for i in range(len(rhs.darrays[0].data)):
        rhs.darrays[0].data[i]=numpy.where(rhsu==origdata[i])[0][0]+ numpy.max(lhs.darrays[0].data)
    rhs.darrays[0].data[rh_zeros]=0
    nibabel.gifti.giftiio.write(rhs,os.path.join(basedir,'all_selected_R_new_parcel_renumbered.func.gii'))
    
    set_structure('%s/all_selected_L_new_parcel_renumbered.func.gii'%basedir,'CORTEX_LEFT')
    set_structure('%s/all_selected_R_new_parcel_renumbered.func.gii'%basedir,'CORTEX_RIGHT')

if __name__ == "__main__":
    mk_renumbered_parcel_file()