"""
compare modules between snyderome and myconnectome datasets

"""

import glob,os
import matplotlib.pyplot as plt
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

def load_varstab_data(infile):
    f=open(infile)
    subcodes=[i.replace('"','') for i in f.readline().strip().split(' ')]
    
    data={}
    for line in f.readlines():
        l_s=line.strip().split(' ')
        data[l_s[0].replace('"','')]=numpy.array([float(i) for i in l_s[1:]])
    f.close()
    return data

def compare_snyderome_myconnectome():
    sny_varstab_file=os.path.join(basedir,'rna-seq/snyderome/varstab_data.txt')
    myc_varstab_file=os.path.join(basedir,'rna-seq/varstab_data_prefiltered.txt')
    
    sny_data=load_varstab_data(sny_varstab_file)
    myc_data=load_varstab_data(myc_varstab_file)
    
    matching_genes=list(set(sny_data.keys()).intersection(myc_data.keys()))
    
    means=numpy.zeros((len(matching_genes),2))
    vars=numpy.zeros((len(matching_genes),2))
    for i in range(len(matching_genes)):
        means[i,0]=numpy.mean(myc_data[matching_genes[i]])
        means[i,1]=numpy.mean(sny_data[matching_genes[i]])
        vars[i,0]=numpy.var(myc_data[matching_genes[i]])
        vars[i,1]=numpy.var(sny_data[matching_genes[i]])
    
    meancor=numpy.corrcoef(means.T)[0,1]
    print 'mean correlation:',meancor
    varcor=numpy.corrcoef(vars.T)[0,1]
    diff=means[:,0]-means[:,1]
    
    f=open(os.path.join(basedir,'rna-seq/snyderome_vs_myconnectome.txt'),'w')
    f.write('%d overlapping genes\n'%len(matching_genes))
    f.write('correlation of mean expression: %0.3f\n'%meancor)
    f.close()
    
    idx=numpy.argsort(diff)
    
    print 'myc>sny'
    for i in idx[:20]:
        print matching_genes[i]
    
    print ''
    print 'sny>myc'
    for i in idx[-20:]:
        print matching_genes[i]
    
    
if __name__ == "__main__":
    compare_snyderome_myconnectome()
    