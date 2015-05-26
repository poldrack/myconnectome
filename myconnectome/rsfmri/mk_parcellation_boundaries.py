"""
make file showing boundaries from parcellation
"""


import numpy,nibabel
import nibabel.gifti.giftiio
import os
from myconnectome.utils import set_structure

basedir=os.environ['MYCONNECTOME_DIR']

def mk_parcellation_boundaries():
    lh=os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii')
    rh=os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered.func.gii')
    
    lhimg=nibabel.gifti.giftiio.read(lh)
    rhimg=nibabel.gifti.giftiio.read(rh)
    
    lhboundaries=numpy.zeros(lhimg.darrays[0].data.shape,dtype=numpy.float32)
    lhboundaries[lhimg.darrays[0].data==0]=1
    
    lhimg.darrays[0].data=lhboundaries
    
    lhimg=nibabel.gifti.giftiio.write(lhimg,os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered_boundaries.func.gii'))
    set_structure.set_structure(os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered_boundaries.func.gii'),'CORTEX_LEFT')
    
    rhboundaries=numpy.zeros(rhimg.darrays[0].data.shape,dtype=numpy.float32)
    rhboundaries[rhimg.darrays[0].data==0]=1
    
    rhimg.darrays[0].data=rhboundaries
    
    rhimg=nibabel.gifti.giftiio.write(rhimg,os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered_boundaries.func.gii'))
    set_structure.set_structure(os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered_boundaries.func.gii'),'CORTEX_RIGHT')
if __name__ == "__main__":
    mk_parcellation_boundaries()