import os,glob
import dicom
import json

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses106/functional'

washubase='/scratch/01329/poldrack/selftracking/washu'

basedirs=['vc39556','vc39556_2']
# 20150402_085939RSFC240FramesEO32Slicess025a001_238.nii.gz

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses105/functional'

runctr={'task001':1,'task009':1}

for b in range(len(basedirs)):
    basedir=os.path.join(washubase,basedirs[b])
    rsfiles=glob.glob(os.path.join(basedir,'nifti/*RSFC*001.nii.gz'))
    rsfiles.sort()
    
    for r in rsfiles:

        seriesnum=int(r.split('Slicess')[1].split('a')[0])
        if r.find('EO')>-1:
            eo='task009'
            taskname='rest - eyes open'
            cogat='http://cognitiveatlas.org/task/id/trm_4c8a834779883'
            
        else:
            eo='task001'
            taskname='rest - eyes closed'
            cogat='http://cognitiveatlas.org/task/id/trm_54e69c642d89b'
        #print eo
        outfile='%s/sub00001_ses105_%s_run%03d.nii.gz'%(outdir,eo,runctr[eo])
        cmd='cp %s %s'%(r,outfile)
        if not os.path.exists(outfile):
            print cmd
        # get dicom header
        dcmfile=glob.glob('%s/DICOM/VC*.MR.HEAD_LAUMANN.%04d.0001.2015.04.02.*.IMA'%(basedir,seriesnum))[0]
        #print dcmfile
        dcmdata=dicom.read_file(dcmfile)
        dcmdict={}
        for k in dcmdata.dir():
            dd=dcmdata.data_element(k)

            try:
                dd.value.decode('ascii')
                dcmdict[dd.name.replace(' ','')]=dd.value
            except:
                try:
                    dd.value.original_string.decode('ascii')
                    dcmdict[dd.name.replace(' ','')]=dd.value
                except:
                    pass
        dcmdict['TaskName']=taskname
        dcmdict['TaskCogatlasId']=cogat
        if dcmdict['RepetitionTime']>100:
            dcmdict['RepetitionTime']=dcmdict['RepetitionTime']/1000.0
        jsonfile=outfile.replace('nii.gz','json')
        
        f=open(jsonfile,'w')
        f.write(json.dumps(dcmdict,indent=4))
        f.close()
        runctr[eo]+=1

                                                  
