

import os,glob


basedir='/scratch/01329/poldrack/selftracking/ds031'
nsubs=12 # nsubs per tarball

subdirs_full=glob.glob(os.path.join(basedir,'sub00001/ses*'))
subdirs=['/'.join(i.split('/')[-3:]) for i in subdirs_full]

subdirs.sort()

washu=subdirs[-2]
stanford=subdirs[-1]
subdirs=subdirs[:-2]

ctr=1
f=open('mk_tarfiles.sh','w')

for i in range(0,len(subdirs),nsubs):
    setlist=['%s/{anatomy,functional,diffusion,fieldmap}'%j for j in subdirs[i:(i+nsubs)]]
    flist=' '.join(setlist)
    cmd='tar zcvf ds031_set%02d.tgz %s'%(ctr,flist)
    print cmd
    ctr+=1
    f.write(cmd+'\n')

f.write('tar zcvf ds031_ses105.tgz ds031/sub00001/ses105\n')
f.write('tar zcvf ds031_ses106.tgz ds031/sub00001/ses106\n')
f.close()
