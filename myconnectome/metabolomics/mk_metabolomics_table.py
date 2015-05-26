"""
load data from clustering and impala annotation
and create table
"""

import glob

infiles=glob.glob('/Users/poldrack/Dropbox/data/selftracking/proteomics/impala_mod*.csv')

outfile=open('metab_table.txt','w')

for i in infiles:
    c=int(i.split('mod')[1].replace('.csv',''))
    f=open('/Users/poldrack/Dropbox/data/selftracking/proteomics/apclust_scaled_mod%02d_names.txt'%c)
    compounds=[l.strip().replace('_',' ').replace(' NIST','') for l in f.readlines()]
    f.close()
    f=open(i)
    header=f.readline()
    lines=f.readlines()
    f.close()
    
    for i in range(3):
            if i==0:
                outfile.write('%d\t%s\t'%(c,', '.join(compounds)))
            else:
                outfile.write('\t\t')
            l_s=lines[i].strip().split(',')
            metab='%s (%s)'%(l_s[0],l_s[1])
            fdr=float(l_s[6])
            if fdr<0.101:
                outfile.write('%s\t%0.3f\n'%(metab,fdr))
            elif i==0:
                outfile.write('no enrichment\n')
            else:
                outfile.write('\t\n')
    outfile.write('\n')
outfile.close()