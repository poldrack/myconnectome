"""
get module descriptions from annotation files
"""

import os,glob

basedir=os.environ['MYCONNECTOME_DIR']
rnaseqdir=os.path.join(basedir,'rna-seq')
wgcnadir=os.path.join(rnaseqdir,'WGCNA')

    
def get_module_descriptions():  
    david_pathfiles=glob.glob(os.path.join(wgcnadir,'DAVID_thr8_prefilt_rin3PCreg_path_set*.txt'))
    david_pathfiles.sort()
    
    module_desc=[]
    for file in david_pathfiles:
        f=open(file)
        lines=f.readlines()
        f.close()
        if len(lines)==0:
            f=open(file.replace('_path_','_GO_'))
            lines=f.readlines()
            f.close()
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