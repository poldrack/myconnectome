""" 
extract within- and between-module correlation for each module/session
"""

import os,sys
import numpy
import ctypes

basedir=os.environ['MYCONNECTOME_DIR']

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0
    
    return z

def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)

def extract_module_summary():
    f=open(os.path.join(basedir,'parcellation/module_names.txt'))
    
    network_names=[]
    for l in f.readlines():
        l_s=l.strip().split('\t')
        network_names.append(' '.join(l_s))
    f.close()
    network_names=network_names[2:]
    nmods=len(network_names)
    
    datadir=os.path.join(basedir,'combined_data_scrubbed')
    outdir=os.path.join(basedir,'rsfmri')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
        
    outdir_bwmod=os.path.join(outdir,'bwmod_corr_data')
    if not os.path.exists(outdir_bwmod):
        os.makedirs(outdir_bwmod)
    outdir_winmod=os.path.join(outdir,'winmod_corr_data')
    if not os.path.exists(outdir_winmod):
        os.mkdir(outdir_winmod)
    
    
    subcodes=[i.strip() for i in open(os.path.join(basedir,'subcodes.txt')).readlines()]
    
    f=open(os.path.join(basedir,'rsfmri/module_assignments.txt'))
    roinum=[]
    hemis=[]
    parcelnum=[]
    modulenum=[]
    for l in f.readlines():
        l_s=l.strip().split()
        roinum.append(int(l_s[0]))
        hemis.append(l_s[1])
        parcelnum.append(int(l_s[2]))
        modulenum.append(float(l_s[3]))
    f.close()
    modulenum=numpy.array(modulenum)
    modules=numpy.unique(modulenum)
    modules=modules[modules>0]
    
    nparcels=616
    
    #subcodes=[subcodes[0]]
    for subcode in subcodes:
        datafile=os.path.join(datadir,subcode+'.txt')
        print datafile
        assert os.path.exists(datafile)
    
        data=numpy.loadtxt(datafile)
        data=data[:,:nparcels]
        
        modctr=0
        modrois={}
        modmeancorr_within=numpy.zeros(len(modules))
        modmeancorr_between=numpy.zeros((len(modules),len(modules)))
        moddata={}
        moddata_unscrubbed={}
        
        for m in modules:
            modrois[m]=numpy.where(modulenum==m)[0]
            moddata[m]=data[:,modrois[m]]
    
        for m in modules:
            modcorr=numpy.corrcoef(moddata[m].T)
            modutr=numpy.triu_indices(modcorr.shape[0],1)
            modmeancorr_within[modctr]=z_to_r(numpy.mean(r_to_z(modcorr[modutr])))
            mbctr=-1
            for mb in modules:
                mbctr+=1
                if mb==m:
                    continue
                mc=numpy.corrcoef(moddata[m].T,moddata[mb].T)
                mcbw=mc[moddata[m].shape[1]:,:moddata[m].shape[1]]
                modmeancorr_between[modctr,mbctr]=z_to_r(numpy.mean(r_to_z(mcbw)))
                
            modctr+=1
    
    
        mcbw_utr=modmeancorr_between[numpy.triu_indices(nmods,1)]
        numpy.savetxt(os.path.join(outdir_winmod,subcode+'.txt'),modmeancorr_within)
        numpy.savetxt(os.path.join(outdir_bwmod,subcode+'.txt'),mcbw_utr)
    
    f=open(os.path.join(outdir,'bwmod_corr_labels.txt'),'w')
    utr=numpy.triu_indices(nmods,1)
    for i in range(utr[0].shape[0]):
        f.write('%s\t%s\n'%(network_names[utr[0][i]].replace(' ','_'),network_names[utr[1][i]].replace(' ','_')))
    f.close()

if __name__ == "__main__":
    extract_module_summary()