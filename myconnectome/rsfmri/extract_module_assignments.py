"""
extract within-module connectivity using isomap parcels
"""

import os,sys
import nibabel.gifti.giftiio
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

def extract_module_assignments():
    parcels={'L':os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii'),
             'R':os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered.func.gii')}
    
    modules={'L':os.path.join(basedir,'parcellation/parcel_L_consensus_new.func.gii'),
             'R':os.path.join(basedir,'parcellation/parcel_R_consensus_new.func.gii')}
    
    modulenums=[ 1. ,   2. ,   3. ,   4.5,   5. ,   7. , 8. ,   9. ,  10. ,  11.5,  15. ,  16. ]
    
    datadir=os.path.join(basedir,'combined_data_scrubbed')
    
    
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
    
    if not os.path.exists(os.path.join(basedir,'rsfmri')):
        os.makedirs(os.path.join(basedir,'rsfmri'))
    f=open(os.path.join(basedir,'rsfmri/module_assignments.txt'),'w')
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

if __name__ == "__main__":
    extract_module_assignments()