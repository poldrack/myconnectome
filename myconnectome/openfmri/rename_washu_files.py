import os,glob


basedir='/scratch/01329/poldrack/selftracking/washu/ses-105/func'
outdir='/scratch/01329/poldrack/selftracking/ds031/sub-01/ses-105/func'
if not os.path.exists(outdir):
    os.mkdir(outdir)

boldfiles=glob.glob(os.path.join(basedir,'*nii.gz'))
for b in boldfiles:

    outfile=b.replace('washu','ds031/sub-01').replace('sub00001','sub-01').replace('ses105','ses-105').replace('task001','task-rest').replace('task009','task-eyesopen').replace('run','run-').replace('.nii.gz','_bold.nii.gz')
    if 1:
        print 'cp %s %s'%(b,outfile)
        f=open(b.replace('.nii.gz','.json'))
        of=open(outfile.replace('.nii.gz','.json'),'w')
        for l in f.readlines():
            l=l.replace("Patient's","Patients").replace("Physician's","Physicians").replace("Manufacturer's","Manufacturers").replace("Operators'","Operators")
            of.write(l.replace("'",'"'))
        of.close()
    

fmdir='/scratch/01329/poldrack/selftracking/washu/ses-105/fmap'
outdir='/scratch/01329/poldrack/selftracking/ds031/sub-01/ses-105/fmap'

if not os.path.exists(outdir):
    os.mkdir(outdir)

if 1:   
 for i in range(1,6):
    stem=os.path.join(fmdir,'sub00001_ses105_%03d'%i)
    newstem=os.path.join(outdir,'sub-01_ses-105_run-%03d'%i)
    #print stem,newstem
    cmd='fslroi %s %s 0 1'%(stem+'_magnitude.nii.gz',newstem+'_magnitude1.nii.gz')
    print cmd
    cmd='fslroi %s %s 1 1'%(stem+'_magnitude.nii.gz',newstem+'_magnitude2.nii.gz')
    print cmd
#    print 'cp %s.json %s_phasediff.json'%(stem,newstem)

    f=open('%s.json'%stem)
    of=open('%s_phasediff.json'%newstem,'w')
    for l in f.readlines():
        if l.find('UID')>-1:
            continue
        l=l.replace("Patient's","Patients").replace("Physician's","Physicians").replace("Manufacturer's","Manufacturers").replace("Operators'","Operators")
        of.write(l.replace("'",'"'))
    of.close()


    print 'cp %s_phasediff.nii.gz %s_phasediff.nii.gz'%(stem,newstem)
    
