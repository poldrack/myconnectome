

import os,glob


basedir='/scratch/01329/poldrack/selftracking'
nsubs=12 # nsubs per tarball

subdirs_full=glob.glob(os.path.join(basedir,'ds031/sub-01/ses*'))
subdirs=['/'.join(i.split('/')[-3:]) for i in subdirs_full]

infofiles=[i for i in glob.glob('/scratch/01329/poldrack/selftracking/ds031/*')+glob.glob('/scratch/01329/poldrack/selftracking/ds031/sub-01/*') if not os.path.isdir(i)]
           
infofiles=[i.replace('/scratch/01329/poldrack/selftracking/','') for i in infofiles]
subdirs.sort()


washu=subdirs[-2]
stanford=subdirs[-1]
subdirs=subdirs[:-3]

ctr=1
f=open('mk_tarfiles.sh','w')


setlist=['%s/{anat,func,dwi,fmap}'%j for j in subdirs[:11]] + infofiles
flist=' '.join(setlist)
cmd='tar zcvf %s/tarballs/ds031_pilot_set.tgz %s'%(basedir,flist)
print cmd

f.write(cmd+'\n')

for i in range(11,len(subdirs),nsubs):
    setlist=['%s/{anat,func,dwi,fmap}'%j for j in subdirs[i:(i+nsubs)]] + infofiles
    flist=' '.join(setlist)
    cmd='tar zcvf %s/tarballs/ds031_set%02d.tgz %s'%(basedir,ctr,flist)
    print cmd
    ctr+=1
    f.write(cmd+'\n')

f.write('tar zcvf %s/tarballs/ds031_ses105.tgz ds031/sub-01/ses-105\n'%basedir)
f.write('tar zcvf %s/tarballs/ds031_ses106.tgz ds031/sub-01/ses-106\n'%basedir)
f.write('tar zcvf %s/tarballs/ds031_retinotopy.tgz ds031/sub-01/ses-ret\n'%basedir)

f.close()
