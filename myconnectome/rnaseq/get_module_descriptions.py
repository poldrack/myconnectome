"""
get module descriptions from annotation files
"""

import os,glob
import numpy

basedir=os.environ['MYCONNECTOME_DIR']
rnaseqdir=os.path.join(basedir,'rna-seq')
wgcnadir=os.path.join(rnaseqdir,'WGCNA')

    
def get_module_descriptions():  
    modlines=open(os.path.join(wgcnadir,'hubgenes_thr8_prefilt_rinPCreg.txt')).readlines()
    modules=[int(i.split()[0]) for i in modlines]
    david_pathfiles=[os.path.join(wgcnadir,'DAVID_thr8_prefilt_rin3PCreg_path_set%03d.txt'%i) for i in modules]

    module_desc=[]
    
    for file in david_pathfiles:
        lines=[]
        try:
            f=open(file)
            lines=f.readlines()
            f.close()
        except:
            pass
        # if there is a pathway, use it - otherwise use GO terms
        if len(lines)==0:
            try:
                f=open(file.replace('_path_','_GO_'))
                lines=f.readlines()
                f.close()
            except:
                pass
        if len(lines)==0:
            module_desc.append('no enrichment')
        else:
            desc=lines[0].strip().split('\t')[2]
            desc=desc.replace('GO:','GO_').replace(':','^').replace('~','^')
            desc=desc.split('^')[1].split(',')[0]
            module_desc.append(desc)
            
    f=open(os.path.join(wgcnadir,'module_descriptions.txt'),'w')
    for i in range(len(module_desc)):
        f.write('%d\t%s\n'%(i+1,module_desc[i]))
    f.close()
    
if __name__ == "__main__":
    get_module_descriptions()