"""
create openfmri distro using files from dcmstack
"""

import os,glob
import json
import numpy
from flatten_js import flatten_js

    

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001'
indir='/scratch/01329/poldrack/selftracking/dcmstack'
excludes=['Localizer','Scout','TRACEW','SBRef']
task_descriptors=['N-','dot','face','super','easy','Breath','Retino']
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
    #if not i.find('104')>-1:
    #	    continue
    taskrun=numpy.ones(len(task_descriptors)+2)
    difrun=1
    anatctr={}
    for k in anat_names.iterkeys():
	    anatctr[k]=1
    sescode=os.path.basename(i)
    if not os.path.exists(os.path.join(outdir,sescode)):
        os.mkdir(os.path.join(outdir,sescode))
    jsonfiles=glob.glob(os.path.join(i,'*.json'))
    for j in jsonfiles:
        niifile=j.replace('.json','.nii.gz')
        js=load_json(j)
        if len(js)==0:
            #print 'zero length json:',l
            continue
        

        jsflat=flatten_js(js)
        sd=jsflat['SeriesDescription']
        sn=jsflat['SeriesNumber']
        exclude=False
        for e in excludes:
            if sd.find(e)>-1:
                exclude=True
        if exclude:
            continue
        print sescode,sn,sd
        
        # process resting

        if sd.find('Resting')>-1:
            if not os.path.exists('%s/%s/functional'%(outdir,sescode)):
                    os.mkdir('%s/%s/functional'%(outdir,sescode))
            
            if len(jsflat['dcmmeta_shape'])<4:
                continue
            if jsflat['dcmmeta_shape'][3]<400:
                #print 'skipping ',j
                continue
            jsflat['TaskName']='rest - eyes closed'
            jsflat['TaskCogatlasId']=task_cogatlas[0]
	    if jsflat['RepetitionTime']>100:
		    # heuristic to change from ms to secs
		    jsflat['RepetitionTime']=jsflat['RepetitionTime']/1000.0
            cmd='cp %s %s/%s/functional/sub00001_%s_task001_run001_bold.nii.gz'%(niifile,
                          outdir,sescode,sescode)
            writecmd(cmd)
	    writejson('%s/%s/functional/sub00001_%s_task001_run001_bold.json'%(outdir,sescode,sescode),jsflat)

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
                cmd='cp %s %s/%s/functional/sub00001_%s_task001_run001_sbref.nii.gz'%(sbref_file,
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
            if sd.find(task_descriptors[t])>-1:
                if not os.path.exists('%s/%s/functional'%(outdir,sescode)):
                    os.mkdir('%s/%s/functional'%(outdir,sescode))
		print jsflat['SeriesDescription'],jsflat['dcmmeta_shape']
		if jsflat['RepetitionTime']>100:
			# heuristic to change from ms to secs
			jsflat['RepetitionTime']=jsflat['RepetitionTime']/1000.0
                jsflat['TaskName']=task_names[t]
                jsflat['TaskCogatlasId']=task_cogatlas[tasknum-1]
                jsflat['TaskDescription']=task_details[t]
                cmd='cp %s %s/%s/functional/sub00001_%s_task%03d_run%03d_bold.nii.gz'%(niifile,
                              outdir,sescode,sescode,tasknum,taskrun[t])
                writecmd(cmd)
		writejson('%s/%s/functional/sub00001_%s_task%03d_run%03d_bold.json'%(outdir,sescode,sescode,tasknum,taskrun[t]),jsflat)
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
                    cmd='cp %s %s/%s/functional/sub00001_%s_task%03d_run%03d_sbref.nii.gz'%(sbref_file,
                              outdir,sescode,sescode,tasknum,taskrun[t])
                    writecmd(cmd)

                taskrun[t]+=1

        # process anatomy
        
        for a in anat_names.keys():
            if sd.find(a)>-1:
                if not os.path.exists('%s/%s/anatomy'%(outdir,sescode)):
                    os.mkdir('%s/%s/anatomy'%(outdir,sescode))
                type=anat_names[a]
                cmd='cp %s %s/%s/anatomy/sub00001_%s_%s_%03d.nii.gz'%(niifile,
                             outdir,sescode,sescode,type,anatctr[type])
                writecmd(cmd)
               
                cmd='cp %s %s/%s/anatomy/sub00001_%s_%s_%03d.json'%(j,
                             outdir,sescode,sescode,type,anatctr[type])
                writecmd(cmd)
		anatctr[type]+=1
               

        # process field map
        if sd.find('gre_field_mapping')>-1:
                if not os.path.exists('%s/%s/fieldmap'%(outdir,sescode)):
                    os.mkdir('%s/%s/fieldmap'%(outdir,sescode))
                try:
                    ntp=jsflat['dcmmeta_shape'][3]
                except:
                    ntp=1
                if ntp>1:
                    cmd='cp %s %s/%s/fieldmap/sub00001_%s_fieldmap_001_magnitude.nii.gz'%(niifile,
                             outdir,sescode,sescode)
                    writecmd(cmd)
               
                    cmd='cp %s %s/%s/fieldmap/sub00001_%s_fieldmap_scan.json'%(j,
                             outdir,sescode,sescode)
                    writecmd(cmd)
                else:
                    cmd='cp %s %s/%s/fieldmap/sub00001_%s_fieldmap_001_phasediff.nii.gz'%(niifile,
                             outdir,sescode,sescode)
                    writecmd(cmd)
               
                    
            

        # process diffusion
        
        if sd.find('MDDW')>-1:
                if not os.path.exists('%s/%s/diffusion'%(outdir,sescode)):
                    os.mkdir('%s/%s/diffusion'%(outdir,sescode))
                if sd.find('R-L')>-1:
                    phase_encode_dir='RL'
                else:
                    phase_encode_dir='LR'
		jsflat['PhaseEncodingDirection']=phase_encode_dir
                cmd='cp %s %s/%s/diffusion/sub00001_%s_dwi_%03d.nii.gz'%(niifile,
                             outdir,sescode,sescode,difrun)
                writecmd(cmd)
                writejson('%s/%s/diffusion/sub00001_%s_dwi_%03d.json'%(outdir,sescode,sescode,difrun),jsflat)
                
                difrun+=1
                
                
                
        



