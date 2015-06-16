"""
extract parcel data from gifti
"""

import os,sys,glob,shutil
from run_shell_cmd import run_shell_cmd
import tempfile
import nibabel.gifti.giftiio
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

def extract_parcel_data(infile):

    surfaces={}
    surfaces['midthickness']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.midthickness.32k_fs_LR.surf.gii'),
        'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.midthickness.32k_fs_LR.surf.gii')}
    surfaces['white']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.white.32k_fs_LR.surf.gii'),
        'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.white.32k_fs_LR.surf.gii')}
    surfaces['pial']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.pial.32k_fs_LR.surf.gii'),
        'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.pial.32k_fs_LR.surf.gii')}

    parcellations={'L':os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii'),
                    'R':os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered.func.gii')}

    parcels={}
    parceldata={}

    for hemis in ['L','R']:
        surfdata=nibabel.gifti.giftiio.read(infile)
        parcels[hemis]=nibabel.gifti.giftiio.read(parcellations[hemis])


        for i in numpy.unique(parcels[hemis].darrays[0].data):
            if i==0:
                continue
            parcelvertices=parcels[hemis].darrays[0].data==i
            parceldata[i]=[]
            for da in range(len(surfdata.darrays)):
                parceldata[i].append(numpy.mean(surfdata.darrays[da].data[parcelvertices[:,0]]))


    nparcs=len(parceldata)
    ntp=len(parceldata[parceldata.keys()[0]])
    parcs=numpy.unique(parceldata.keys())
    parcs.sort()

    parcmtx=numpy.zeros((nparcs,ntp))
    for p in range(len(parcs)):
        parcmtx[p]=parceldata[parcs[p]]


    return parcmtx
