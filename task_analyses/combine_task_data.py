import os,glob
import nibabel
import numpy
from openfmri_utils import *

basedir='/corral-repl/utexas/poldracklab/data/selftracking/'
outdir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/task_data'

try:
    taskfiles
except:
    taskfiles=[i for i in glob.glob(os.path.join(basedir,'sub*/model/model*/task*.feat/stats/zstat*.nii.gz')) if i.find('_333')>0]

try:
    maskfiles
except:
    maskfiles=[i for i in glob.glob(os.path.join(basedir,'sub*/model/model*/task*.feat/mask.nii.gz')) if i.find('_333')>0]

maskdata=numpy.zeros((48,64,48))
for m in maskfiles:
    img=nibabel.load(m)
    d=img.get_data()
    maskdata+=d

maskvox=numpy.where(maskdata==len(maskfiles))
maskdata_img=nibabel.Nifti1Image(maskdata,affine=img.get_affine())
maskdata_img.to_filename(os.path.join(outdir,'maskdata.nii.gz'))

task=[]
cope=[]
subs=[]
copename=[]
data=numpy.zeros((len(taskfiles),79610))
ctr=0
for t in taskfiles:
    #print t
    t_s=t.split('/')
    sn=int(t_s[6].replace('sub',''))
    tn=int(t_s[8].replace('model',''))
    cn=int(t_s[11].split('.')[0].replace('zstat',''))
    
    con=load_fsl_design_con(os.path.join( '/'.join(t_s[:10]),'design.con'))
    if con[cn]=='all' or con[cn].find('junk')>-1 or con[cn].find('_vs_')>-1:
        print 'skipping',con[cn]
        continue
    subs.append(sn)
    task.append(tn)
    cope.append(cn)
    copename.append(con[cn])
    img=nibabel.load(t)
    data[ctr,:]=img.get_data()[maskvox]
    ctr+=1
numpy.save(os.path.join(outdir,'task_contrast_data.npy'),data)
numpy.savetxt(os.path.join(outdir,'tasknum.txt'),task)
numpy.savetxt(os.path.join(outdir,'copenum.txt'),cope)
numpy.savetxt(os.path.join(outdir,'sessnum.txt'),subs)
f=open(os.path.join(outdir,'copename.txt'),'w')
for c in copename:
    f.write(c+'\n')
f.close()
