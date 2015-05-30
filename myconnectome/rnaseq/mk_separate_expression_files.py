import numpy
import os

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/'

f=open(os.path.join(basedir,'rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt'))
header=f.readline()
lines=f.readlines()


outdir=os.path.join(basedir,'rna-seq/expression_sep_files')

if not os.path.exists(outdir):
    os.mkdir(outdir)
    
for i in range(len(lines)):
    l_s=lines[i].strip().split(' ')
    outfile=os.path.join(outdir,'expr_snpPCreg_%05d.txt'%int(i+1))
    f=open(outfile,'w')
    for j in l_s[1:]:
        f.write("%s\n"%j)
    f.close()

