"""
get location and identity info
for all of the parcels in the
Poldrome parcellation
"""

import os,sys
import nibabel
import nibabel.gifti.giftiio as giftiio
import numpy

basedir='/corral-repl/utexas/poldracklab/data/selftracking/parcellation'
hcpdir='/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k'
tutorialdir='/corral-repl/utexas/poldracklab/data/selftracking/HCP_tutorial'
fsldir='/corral-repl/utexas/poldracklab/software_lonestar/fsl-5.0.6'

lhfile=os.path.join(basedir,'84sub_333_all_startpos50_presmooth_L_threshperc0.45_minparcel20watershedmerge_0.45.func.gii')
rhfile=os.path.join(basedir,'84sub_333_all_startpos50_presmooth_R_threshperc0.45_minparcel20watershedmerge_0.45.func.gii')

lh=giftiio.read(lhfile)
rh=giftiio.read(rhfile)

lhparcvals=numpy.unique(lh.darrays[0].data)[1:]
rhparcvals=numpy.unique(rh.darrays[0].data)[1:]

# open community files
communities_orig=numpy.loadtxt(os.path.join(basedir,'parcel_infomap_assigns_startpos50_neworder_communities.txt'))
communities_orig_idx=numpy.loadtxt(os.path.join(basedir,'parcel_infomap_assigns_startpos50_neworder_consensus_ind.txt'))


#lhinfomapfile=os.path.join(basedir,'parcel_L_consensus.func.gii')
#rhinfomapfile=os.path.join(basedir,'parcel_R_consensus.func.gii')

#lhinfomap=giftiio.read(lhinfomapfile)
#rhinfomap=giftiio.read(rhinfomapfile)


lhsurffile=os.path.join(hcpdir,'sub013.L.midthickness.32k_fs_LR.surf.gii')
lhsurf=giftiio.read(lhsurffile)
rhsurffile=os.path.join(hcpdir,'sub013.R.midthickness.32k_fs_LR.surf.gii')
rhsurf=giftiio.read(rhsurffile)


# get mean XYZ location and central vertex of each parcel
lhcoords=numpy.zeros((len(lhparcvals),3))
lhcentvertex=numpy.zeros(len(lhparcvals))

for i in range(len(lhparcvals)):
    v=lhparcvals[i]
    vertices=numpy.where(lh.darrays[0].data==v)[0]
    lhcoords[i,:]=numpy.mean(lhsurf.darrays[0].data[vertices,:],0)
    vdist=numpy.zeros(len(vertices))
    for j in range(len(vertices)):
        vdist[j]= numpy.linalg.norm(lhsurf.darrays[0].data[j,:] - lhcoords[i,:])
    lhcentvertex[i]=vertices[vdist==numpy.min(vdist)]
    
rhcoords=numpy.zeros((len(rhparcvals),3))
rhcentvertex=numpy.zeros(len(rhparcvals))

for i in range(len(rhparcvals)):
    v=rhparcvals[i]
    vertices=numpy.where(rh.darrays[0].data==v)[0]
    rhcoords[i,:]=numpy.mean(rhsurf.darrays[0].data[vertices,:],0)
    vdist=numpy.zeros(len(vertices))
    for j in range(len(vertices)):
        vdist[j]= numpy.linalg.norm(rhsurf.darrays[0].data[j,:] - rhcoords[i,:])
    rhcentvertex[i]=vertices[vdist==numpy.min(vdist)]
        
# get labels for each parcel

llabelfile=os.path.join(hcpdir,'sub013.L.aparc.32k_fs_LR.label.gii')
rlabelfile=os.path.join(hcpdir,'sub013.R.aparc.32k_fs_LR.label.gii')

lparc=giftiio.read(llabelfile)
rparc=giftiio.read(rlabelfile)


lhparclabels=[]
rhparclabels=[]

for i in range(len(lhcentvertex)):
    l=lparc.darrays[0].data[lhcentvertex[i]]
    lhparclabels.append(lparc.labeltable.labels[l].label)

for i in range(len(rhcentvertex)):
    l=rparc.darrays[0].data[rhcentvertex[i]]
    rhparclabels.append(rparc.labeltable.labels[l].label)


# get RSN labels from HCP tutorial data
l_rsnlabelfile=os.path.join(tutorialdir,'RSN-networks.L.32k_fs_LR.label.gii')
r_rsnlabelfile=os.path.join(tutorialdir,'RSN-networks.R.32k_fs_LR.label.gii')

l_rsn=giftiio.read(l_rsnlabelfile)
r_rsn=giftiio.read(r_rsnlabelfile)

power_network_names={-1:'none',0:'none',1:'Default',2:'Second-Visual',3:'Frontal-Parietal',4.5:'First-Visual-V1+',5:'First-Dorsal-Attention',6:'Second-Dorsal-Attention',7:'Ventral-Attention-Language',8:'Salience',9:'Cingulo-opercular',10:'Somatomotor',11.5:'Frontal-Parietal-Other',15:'Parietal-Episodic-Retrieval',16:'Parieto-Occipital'}

l_rsnlabels=[]
r_rsnlabels=[]
l_rsnlabels_yeo7=[]
r_rsnlabels_yeo7=[]
l_rsnlabels_yeo17=[]
r_rsnlabels_yeo17=[]

for i in range(len(lhcentvertex)):
    l=lhinfomap.darrays[0].data[lhcentvertex[i]]
    l_rsnlabels.append(power_network_names[l[0]])
    l=l_rsn.darrays[0].data[lhcentvertex[i]]
    l_rsnlabels_yeo7.append(l_rsn.labeltable.labels[l].label)
    l=l_rsn.darrays[1].data[lhcentvertex[i]]
    l_rsnlabels_yeo17.append(l_rsn.labeltable.labels[l].label)

for i in range(len(rhcentvertex)):
    l=rhinfomap.darrays[0].data[rhcentvertex[i]]
    r_rsnlabels.append(power_network_names[l[0]])
    l=r_rsn.darrays[0].data[rhcentvertex[i]]
    r_rsnlabels_yeo7.append(r_rsn.labeltable.labels[l].label)
    l=r_rsn.darrays[1].data[rhcentvertex[i]]
    r_rsnlabels_yeo17.append(r_rsn.labeltable.labels[l].label)

# get lobe

atlasfile=os.path.join(fsldir,'data/atlases/MNI/MNI-maxprob-thr0-2mm.nii.gz')

atlas=nibabel.load(atlasfile)
atlasdata=atlas.get_data()
lobenames=['None','Caudate','Cerebellum','Frontal','Insula','Occipital','Parietal','Putamen','Temporal','Thalamus']

def mni2vox(mni,qform):
    tmp=numpy.linalg.inv(qform)*numpy.matrix([mni[0],mni[1],mni[2],1]).T
    return numpy.array(numpy.round(tmp.T[0,0:3]))[0]

l_lobe=[]
r_lobe=[]

for i in range(len(lhcentvertex)):
    vox=mni2vox(lhcoords[i,:],atlas.get_qform())
    lobe=atlasdata[vox[0],vox[1],vox[2]]
    l_lobe.append(lobenames[lobe])
for i in range(len(rhcentvertex)):
    vox=mni2vox(rhcoords[i,:],atlas.get_qform())
    lobe=atlasdata[vox[0],vox[1],vox[2]]
    r_lobe.append(lobenames[lobe])

use_aseg=True

def vox2mni(vox,qform):
    vox=numpy.array([vox[0],vox[1],vox[2],1])
    return qform.dot(vox)[:3]

if use_aseg:
# now get data from APARC
    f=open(os.path.join(basedir,'aseg_fields.txt'))
    asegnames={}
    for l in f.readlines():
        l_s=l.strip().split()
        asegnames[int(l_s[0])]=l_s[1]
        f.close()
    asegkeys=asegnames.keys()
    asegkeys.sort()
    asegimg=nibabel.load(os.path.join(basedir,'aparc+aseg_reg2mni.nii.gz'))
    asegdata=asegimg.get_data()

    meancoords={}
    for k in asegkeys:
        mni=[]
        v=numpy.where(asegdata==k)
        nvox=len(v[0])
        for i in range(nvox):
            mni.append(vox2mni([v[0][i],v[1][i],v[2][i]],asegimg.get_qform()))
        mni=numpy.matrix(mni)
        meancoords[k]=numpy.mean(mni,0)
asdf

f=open(os.path.join(basedir,'parcel_data.txt','w'))
ctr=1
for i in range(len(lhcentvertex)):
    f.write('%d\tL\t%0.2f\t%0.2f\t%0.2f\t%s\t%s\t%s\t%s\t%s\n'%(ctr,lhcoords[i,0],lhcoords[i,1],lhcoords[i,2],l_lobe[i],lhparclabels[i],l_rsnlabels[i],l_rsnlabels_yeo7[i],l_rsnlabels_yeo17[i]))
    ctr+=1

for i in range(len(rhcentvertex)):
    f.write('%d\tR\t%0.2f\t%0.2f\t%0.2f\t%s\t%s\t%s\t%s\t%s\n'%(ctr,rhcoords[i,0],rhcoords[i,1],rhcoords[i,2],r_lobe[i],rhparclabels[i],r_rsnlabels[i],r_rsnlabels_yeo7[i],r_rsnlabels_yeo17[i]))
    ctr+=1


if use_aseg:
  for k in asegkeys:
    if meancoords[k][0,0]<0:
        hemis='L'
    else:
        hemis='R'
    f.write('%d\t%s\t%0.2f\t%0.2f\t%0.2f\t%s\t%s\t%s\t%s\t%s\n'%(ctr,hemis,meancoords[k][0,0],meancoords[k][0,1],meancoords[k][0,2],'subcortical',asegnames[k],'na','na','na'))
    ctr+=1
    
f.close()
