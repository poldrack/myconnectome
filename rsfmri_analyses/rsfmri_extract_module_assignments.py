"""
extract within-module connectivity using isomap parcels
"""

import os,sys
import nibabel.gifti.giftiio
import numpy

parcels={'L':'/corral-repl/utexas/poldracklab/data/selftracking/laumann/all_selected_L_parcel.func.gii','R':'/corral-repl/utexas/poldracklab/data/selftracking/laumann/all_selected_R_parcel.func.gii'}

modules={'L':'/corral-repl/utexas/poldracklab/data/selftracking/laumann/parcel_L_consensus.func.gii','R':'/corral-repl/utexas/poldracklab/data/selftracking/laumann/parcel_R_consensus.func.gii'}

modulenums=[ 1. ,   2. ,   3. ,   4.5,   5. ,   6. ,   7. , 8. ,   9. ,  10. ,  11.5,  15. ,  16. ]

datadir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/subdata_scrubbed'

#subcode='sub014'

#datafile=os.path.join(datadir,subcode+'.txt')
#assert os.path.exists(datafile)

#data=numpy.loadtxt(datafile)

parceldata={}
parceldata['L']=nibabel.gifti.giftiio.read(parcels['L']).darrays[0].data
parceldata['R']=nibabel.gifti.giftiio.read(parcels['R']).darrays[0].data
parcelnums={'L':{},'R':{}}
parcelnums['L']=numpy.unique(parceldata['L'])
parcelnums['R']=numpy.unique(parceldata['R'])

moduledata={}
moduledata['L']=nibabel.gifti.giftiio.read(modules['L']).darrays[0].data
moduledata['R']=nibabel.gifti.giftiio.read(modules['R']).darrays[0].data

parcelvox={'L':{},'R':{}}

modulevox={'L':{},'R':{}}

for n in parcelnums['L']:
    parcelvox['L'][n]=numpy.where(parceldata['L']==n)[0]
    mvox=moduledata['L'][parcelvox['L'][n]]
    if len(numpy.unique(mvox))>1:
        print 'problem with LH:',n
    modulevox['L'][n]=mvox[0]
    
for n in parcelnums['R']:
    parcelvox['R'][n]=numpy.where(parceldata['R']==n)[0]
    mvox=moduledata['R'][parcelvox['R'][n]]
    if len(numpy.unique(mvox))>1:
        print 'problem with LH:',n
    modulevox['R'][n]=mvox[0]


f=open('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/module_assignments.txt','w')
ctr=0
for h in ['L','R']:
    parcelkeys=modulevox[h].keys()
    parcelkeys.sort()
    for k in parcelkeys:
        if k==0:
            continue
        f.write('%d\t%s\t%d\t%f\n'%(ctr,h,k,modulevox[h][k]))
        ctr+=1
f.close()
