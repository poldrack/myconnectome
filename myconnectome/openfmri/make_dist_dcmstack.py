"""
create openfmri distro using files from dcmstack
- this is only for UT data

- problem with breahth hold sessions for ses 066, 067, and 068 - named as resting state
"""

import os,glob
import json
import numpy
from flatten_js import flatten_js
import nibabel
import pickle

slicetiming=pickle.load(open('/corral-repl/utexas/poldracklab/data/selftracking/slicetiming.pkl','rb'))

outdir='/scratch/01329/poldrack/selftracking/ds031/sub-01'
indir='/scratch/01329/poldrack/selftracking/dcmstack'
excludes=['Localizer','Scout','TRACEW','SBRef']
task_descriptors=['N-','dot','face','super','easy','Breath','Retino']
task_codes=['nback','dotstop','objects','languagewm','spatialwm','breathhold','retinotopy']

task_details=['N-back task with faces, scenes, and Chinese characters','Dot-motion perception task with an embedded stop signal task','Multi-object localizer task','Sentence/nonword working memory task','Spatial working memory task with varied load','Breath holding task','Retinotopic mapping']

task_cogatlas=['http://www.cognitiveatlas.org/task/id/trm_54e69c642d89b','http://www.cognitiveatlas.org/task/id/trm_558c324478d22','http://www.cognitiveatlas.org/task/id/trm_558c3350c6a9f','http://www.cognitiveatlas.org/task/id/trm_558c33e7714ba','http://www.cognitiveatlas.org/term/id/trm_558c35979a284','http://www.cognitiveatlas.org/task/id/trm_558c36935a0e9','http://www.cognitiveatlas.org/term/id/trm_4c898a680e424','http://www.cognitiveatlas.org/task/id/trm_558c4d3105abf']
task_names=['nback','dot motion stop signal','object localizer','language localizer','spatial working memory','breath holding','retinotopy']

anat_names={'T1w':'T1w','T2w':'T2w','MPRAGE':'T1w','PD-T2':'PDT2','t2':'T2w','t1':'T1w','PDT2':'PDT2'}

def load_json(j):
        l=open(j).readlines()
        try:
            js=json.loads(' '.join([i.strip() for i in l]))
        except:
            js=[]
        return js
    
indirs=glob.glob(os.path.join(indir,'ses*'))
indirs.sort()


if os.path.exists('copy_dcmstack_files.sh'):
	os.remove('copy_dcmstack_files.sh')
	
def writecmd(cmd):
	cmdfile=open('copy_dcmstack_files.sh','a')
	cmdfile.write(cmd+'\n')
	cmdfile.close()

def writejson(outfile,js):
	f=open(outfile,'w')
	f.write(json.dumps(js,indent=4))
	f.close()
	
outfiles=[]

sub_json={}
for i in indirs:
    #if not i.find('014')>-1:
    #	    continue
    taskrun=numpy.ones(len(task_descriptors)+2)
    difrun=1
    anatctr={}
    for k in anat_names.iterkeys():
	    anatctr[k]=1
    sescode_orig=os.path.basename(i)
    sescode=sescode_orig.replace('ses','ses-')
    if not os.path.exists(os.path.join(outdir,sescode)):
        os.mkdir(os.path.join(outdir,sescode))
    jsonfiles=glob.glob(os.path.join(i,'*.json'))
    jsonfiles.sort()
    for j in jsonfiles:
        niifile=j.replace('.json','.nii.gz')
        js=load_json(j)
        if len(js)==0:
            #print 'zero length json:',l
            continue
        
        
        jsflat=flatten_js(js)
	# fix misnamed breaht hold scans
        sd=jsflat['SeriesDescription']
        sn=jsflat['SeriesNumber']
	if len(jsflat['dcmmeta_shape'])==4:
		ntp=jsflat['dcmmeta_shape'][3]
	else:
		ntp=1
	if sd.find('Resting')>-1 and ntp==318:
		sd='Breath Holding'
		jsflat['SeriesDescription']=sd
        exclude=False
        for e in excludes:
            if sd.find(e)>-1:
	        print 'excluding',sn,sd
                exclude=True
        if exclude:
            continue
        print sescode,sn,sd,jsflat['dcmmeta_shape']
        
        # process resting

        if sd.find('Resting')>-1:
            if not os.path.exists('%s/%s/func'%(outdir,sescode)):
                    os.mkdir('%s/%s/func'%(outdir,sescode))
            
            if len(jsflat['dcmmeta_shape'])<4:
                continue
            if jsflat['dcmmeta_shape'][3]<400:
                #print 'skipping ',j
                continue
	    jsflat['SliceTiming']=slicetiming[sescode][sn][0]
	    jsflat['MultibandAccelerationFactor']=slicetiming[sescode][sn][1]
            jsflat['TaskName']='rest - eyes closed'
            jsflat['TaskCogatlasId']=task_cogatlas[0]
	    if jsflat['RepetitionTime']>100:
		    # heuristic to change from ms to secs
		    jsflat['RepetitionTime']=jsflat['RepetitionTime']/1000.0
            cmd='cp %s %s/%s/func//sub-01_%s_task-rest_acq-MB_run-001_bold.nii.gz'%(niifile,
                          outdir,sescode,sescode)
            writecmd(cmd)
	    writejson('%s/%s/func/sub-01_%s_task-rest_acq-MB_run-001_bold.json'%(outdir,sescode,sescode),jsflat)

            # try to copy SBRef if it exists
            niibase=os.path.basename(niifile)
            niidir=os.path.dirname(niifile)
            sbref_file=os.path.join(niidir,niibase.replace('%03d'%sn,'%03d'%int(sn-1)))
            sbref_json=sbref_file.replace('nii.gz','json')
            try:
                sbj=flatten_js(load_json(sbref_json))
            except:
                sbj={'SeriesDescription':''}
            
            if os.path.exists(sbref_file) and sbj['SeriesDescription'].find('SBRef')>-1:
                cmd='cp %s %s/%s/func//sub-01_%s_task-rest_acq-SBref_run-001_bold.nii.gz'%(sbref_file,
                          outdir,sescode,sescode)
                writecmd(cmd)

                
        # process task
        for t in range(len(task_descriptors)):
            tasknum=t+2
            if len(jsflat['dcmmeta_shape'])<4:
                continue
            if jsflat['dcmmeta_shape'][3]<100:
                print 'skipping ',j
                continue
	    sd=sd.replace('N Bac','N-Bac')
            if sd.find(task_descriptors[t])>-1:
                if not os.path.exists('%s/%s/func'%(outdir,sescode)):
                    os.mkdir('%s/%s/func'%(outdir,sescode))
		print jsflat['SeriesDescription'],jsflat['dcmmeta_shape']
		if jsflat['RepetitionTime']>100:
			# heuristic to change from ms to secs
			jsflat['RepetitionTime']=jsflat['RepetitionTime']/1000.0
		jsflat['SliceTiming']=slicetiming[sescode][sn][0]
		jsflat['MultibandAccelerationFactor']=slicetiming[sescode][sn][1]
                jsflat['TaskName']=task_names[t]
                jsflat['TaskCogatlasId']=task_cogatlas[tasknum-1]
                jsflat['TaskDescription']=task_details[t]
                cmd='cp %s %s/%s/func/sub-01_%s_task-%s_acq-MB_run-%03d_bold.nii.gz'%(niifile,
                              outdir,sescode,sescode,task_codes[t],taskrun[t])
                writecmd(cmd)
		writejson('%s/%s/func/sub-01_%s_task-%s_acq-MB_run-%03d_bold.json'%(outdir,sescode,sescode,task_codes[t],taskrun[t]),jsflat)
                niibase=os.path.basename(niifile)
                niidir=os.path.dirname(niifile)

                # try to copy SBRef if it exists
                niibase=os.path.basename(niifile)
                niidir=os.path.dirname(niifile)
                sbref_file=os.path.join(niidir,niibase.replace('%03d'%sn,'%03d'%int(sn-1)))
                sbref_json=sbref_file.replace('nii.gz','json')
                try:
                    sbj=flatten_js(load_json(sbref_json))
                except:
                    sbj={'SeriesDescription':''}
		print sbj['SeriesDescription']

                if os.path.exists(sbref_file) and sbj['SeriesDescription'].find('SBRef')>-1:
                    cmd='cp %s %s/%s/func/sub-01_%s_task-%s_acq-SBref_run-%03d_bold.nii.gz'%(sbref_file,
                              outdir,sescode,sescode,task_codes[t],taskrun[t])
                    writecmd(cmd)

                taskrun[t]+=1

        # process anatomy
        
        for a in anat_names.keys():
            if sd.find(a)>-1:
                if not os.path.exists('%s/%s/anat'%(outdir,sescode)):
                    os.mkdir('%s/%s/anat'%(outdir,sescode))
                type=anat_names[a]
                cmd='cp %s %s/%s/anat/sub-01_%s_run-%03d_%s.nii.gz'%(niifile,
                             outdir,sescode,sescode,anatctr[type],type)
                writecmd(cmd)
               
                cmd='cp %s %s/%s/anat/sub-01_%s_run-%03d_%s.json'%(j,
                             outdir,sescode,sescode,anatctr[type],type)
                writecmd(cmd)
		anatctr[type]+=1
               

        # process field map
        if sd.find('gre_field_mapping')>-1:
                if not os.path.exists('%s/%s/fmap'%(outdir,sescode)):
                    os.mkdir('%s/%s/fmap'%(outdir,sescode))
                try:
                    ntp=jsflat['dcmmeta_shape'][3]
                except:
                    ntp=1
                if ntp>1:
		    magfile=nibabel.load(niifile)
		    magdata=magfile.get_data()
		    magdata1=magdata[:,:,:,0]
		    mf1=nibabel.Nifti1Image(magdata1,magfile.get_affine(),magfile.get_header())
		    mf1.to_filename('%s/%s/fmap/sub-01_%s_magnitude1.nii.gz'%(outdir,sescode,sescode))
		    magdata2=magdata[:,:,:,1]
		    mf2=nibabel.Nifti1Image(magdata2,magfile.get_affine(),magfile.get_header())
		    mf2.to_filename('%s/%s/fmap/sub-01_%s_magnitude2.nii.gz'%(outdir,sescode,sescode))
		    
                    #cmd='cp %s %s/%s/fmap/sub-01_%s_magnitude.nii.gz'%(niifile,
#                             outdir,sescode,sescode)
                    #writecmd(cmd)
		    writejson('%s/%s/fmap/sub-01_%s_phasediff.json'%(outdir,sescode,sescode),jsflat)
                    writecmd(cmd)
                else:
                    cmd='cp %s %s/%s/fmap/sub-01_%s_phasediff.nii.gz'%(niifile,
                             outdir,sescode,sescode)
                    writecmd(cmd)
               
                    
            

        # process diffusion
        
        if sd.find('MDDW')>-1:
                if not os.path.exists('%s/%s/dwi'%(outdir,sescode)):
                    os.mkdir('%s/%s/dwi'%(outdir,sescode))
                if sd.find('R-L')>-1:
                    phase_encode_dir='RL'
                else:
                    phase_encode_dir='LR'
		jsflat['PhaseEncodingDirection']=phase_encode_dir
		jsflat['EffectiveEchoSpacing']=2.6/10000.0
                cmd='cp %s %s/%s/dwi/sub-01_%s_run-%03d_dwi.nii.gz'%(niifile,
                             outdir,sescode,sescode,difrun)
                writecmd(cmd)
                writejson('%s/%s/dwi/sub-01_%s_run-%03d_dwi.json'%(outdir,sescode,sescode,difrun),jsflat)
                
                difrun+=1
                
                
                
        



