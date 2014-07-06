# renumber parcels so that CARET will treat them properly
# originally called mk_parcelfile.py
import sys

import nibabel.gifti.giftiio
import nibabel,numpy


#rh=nibabel.load('parcels.R.nii.gz').get_data()
#lh=nibabel.load('parcels.L.nii.gz').get_data()
lhs=nibabel.gifti.giftiio.read('all_selected_L_parcel.func.gii')
rhs=nibabel.gifti.giftiio.read('all_selected_R_parcel.func.gii')
#lhu=numpy.unique(lh)
lhsu=numpy.unique(lhs.darrays[0].data)
rhsu=numpy.unique(rhs.darrays[0].data)


origdata=lhs.darrays[0].data


intent=lhs.darrays[0].intent
datatype=lhs.darrays[0].datatype
for i in range(len(lhs.darrays[0].data)):
    lhs.darrays[0].data[i]=numpy.where(lhsu==origdata[i])[0][0]

nibabel.gifti.giftiio.write(lhs,'all_selected_L_parcel_renumbered.func.gii')

origdata=rhs.darrays[0].data

intent=rhs.darrays[0].intent
datatype=rhs.darrays[0].datatype
rh_zeros=numpy.where(rhs.darrays[0].data==0)
for i in range(len(rhs.darrays[0].data)):
    rhs.darrays[0].data[i]=numpy.where(rhsu==origdata[i])[0][0]+ numpy.max(lhs.darrays[0].data)
rhs.darrays[0].data[rh_zeros]=0
nibabel.gifti.giftiio.write(rhs,'all_selected_R_parcel_renumbered.func.gii')
