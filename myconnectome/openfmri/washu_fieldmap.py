import json,glob,os
import dicom

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses105/fieldmap'
washubase='/scratch/01329/poldrack/selftracking/washu'
basedirs=['vc39556','vc39556_2']

fmseries=[[5,10,21],[5,17]]
ctr=1
for i in range(2):
    basedir=os.path.join(washubase,basedirs[i])
    for j in range(len(fmseries[i])):
        seriesnum=fmseries[i][j]
        dcmfile=glob.glob('%s/DICOM/VC*.MR.HEAD_LAUMANN.%04d.*.IMA'%(basedir,seriesnum))[0]
        print dcmfile
        dcmdata=dicom.read_file(dcmfile)
        dcmdict={}
        for k in dcmdata.dir():
            dd=dcmdata.data_element(k)

            try:
                dd.value.decode('ascii')
                dcmdict[dd.name]=dd.value
            except:
                try:
                    dd.value.original_string.decode('ascii')
                    dcmdict[dd.name]=dd.value
                except:
                    pass
        jsonfile='%s/sub00001_ses105_%03d.json'%(outdir,ctr)
        ctr+=1
        f=open(jsonfile,'w')
        f.write(json.dumps(dcmdict,indent=4))
        f.close()

