import numpy
import os

basedir=os.environ['MYCONNECTOME_DIR']

    
def get_matching_datasets(d1,d2,s1,s2):
    """
    get_matching_datasets(d1,d2,s1,s2)
    """
    
    joint_subs=set(s1).intersection(s2)
    s1_idx=[i for i in range(len(s1)) if s1[i] in joint_subs]
    s2_idx=[i for i in range(len(s2)) if s2[i] in joint_subs]
    for i in range(len(s1_idx)):
        assert s1[s1_idx[i]]==s2[s2_idx[i]]
    d1_joint=d1[s1_idx,:]
    d2_joint=d2[s2_idx,:]
    return d1_joint, d2_joint,joint_subs

def load_immport_data():
    f=open(os.path.join(basedir,'rna-seq/ImmPort/ImmPort_eigengenes_rinregressed.txt'))
    lines=[]
    gene_names=[]
    for l in f.readlines():
            l_s=l.strip().split()
            gene_names.append(l_s[0])
            lines.append([float(l_s[i]) for i in range(1,len(l_s))])
    f.close()
    data=numpy.array(lines).T
    subcodes=[i.strip() for i in open(os.path.join(basedir,'rna-seq/pathsubs.txt')).readlines()]
    return data,gene_names,subcodes
    
    
def load_rnaseq_data(use_wgcna=True):
    if use_wgcna:
        f=open(os.path.join(basedir,'rna-seq/WGCNA/MEs-thr8-rinreg-48sess.txt'))
        header=[i.replace('"','') for i in f.readline().strip().split()]
        MEs=[int(i.replace('ME','')) for i in header]
        sort_idx=numpy.argsort(MEs)
        gene_names=[MEs[i] for i in sort_idx]
        lines=[]
        for l in f.readlines():
            l_s=l.strip().split()
            lines.append([float(l_s[i]) for i in sort_idx])
        f.close()
        data=numpy.array(lines)
        subcodes=[i.strip() for i in open(os.path.join(basedir,'rna-seq/pathsubs.txt')).readlines()]
    else:  # use full data
        f=open(os.path.join(basedir,'rna-seq/varstab_data_rinregressed.txt'))
        subcodes=[i.replace('"','') for i in f.readline().strip().split(' ')]
        
        lines=[]
        gene_names=[]
        for line in f.readlines():
            l_s=line.strip().split(' ')
            lines.append([float(i) for i in l_s[1:]])
            gene_names.append(l_s[0].replace('"',''))
        f.close()
        data=numpy.array(lines).T
    f=open(os.path.join(basedir,'rna-seq/drawdates.txt'))
    dates=[i for i in f.readline().split('\r')]
    f.close()
    return data,gene_names,dates,subcodes

def load_behav_data(subcodes_limit=None,xvars=None,allsubs=False):
    """
    load behavioral data - pass dates to limit to specific subcodes
    """
    
    if allsubs:
        f=open(os.path.join(basedir,'behavior/trackingdata.txt'))
    else:
        f=open(os.path.join(basedir,'behavior/trackingdata_goodscans.txt'))
    header=[i for i in f.readline().strip().split('\t')]
    variables=header[2:]  # remove 
    lines=[]
    for line in f.readlines():
        l_s=line.strip().split('\t')
        if subcodes_limit:
            if not set(subcodes_limit).intersection([l_s[0]]):
                continue
        lines.append(l_s)

    f.close()
    
    behavdata=numpy.zeros((len(lines),len(variables)))
    dates=[]
    subcodes=[]
    for i in range(len(lines)):
        line=lines[i]
        for v in range(len(variables)):
            try:
                behavdata[i,v]=float(line[v+2])
            except:
                behavdata[i,v]=numpy.nan
        dates.append(line[1])
        subcodes.append(line[0])
    if subcodes_limit:
        try:
            assert len(subcodes)==len(subcodes_limit)
        except:
            print 'there is a problem: subcodes do not match subcodes_limit'
    if xvars:
        xvar_nums=[]
        for name in xvars:
            varnum=[i for i in range(len(variables)) if variables[i]==name.replace('.',':')]
            xvar_nums.append(varnum[0])
        behavdata=behavdata[:,xvar_nums]
        variables=[variables[i] for i in xvar_nums]
    
    return behavdata,variables,dates,subcodes

def load_food_data():
    f=open(os.path.join(basedir,'behavior/food_data.txt'))
    header=f.readline().strip().split()
    lines=[i.strip() for i in f.readlines()]
    subcodes=[]
    data=[]
    for l in lines:
        data.append([int(i) for i in l.split('\t')[1:]])
        subcodes.append(l.split('\t')[0])
    data=numpy.array(data)
    behavdata,behavvars,behavdates,behavsubs=load_behav_data(allsubs=True)
    behav_dict={}
    for i in range(len(behavdates)):
        behav_dict[behavsubs[i]]=behavdates[i]
    food_dates=[behav_dict[i] for i in subcodes]
    return data,header[1:],food_dates,subcodes

def load_metab_data():
    f=open(os.path.join(basedir,'rna-seq/drawdates.txt'))
    dates=[i.strip() for i in f.readlines()]
    f.close()
    subcodes=[i.strip() for i in open(os.path.join(basedir,'rna-seq/pathsubs.txt')).readlines()]
    f=open(os.path.join(basedir,'metabolomics/apclust_eigenconcentrations.txt'))
    header=f.readline()
    lines=f.readlines()
    f.close()
    data=[]
    for l in lines:
        l_s=[float(i) for i in l.strip().split()[1:]]
        data.append(l_s)
    data=numpy.array(data)
    clust_desc=[i.strip() for i in open(os.path.join(basedir,'metabolomics/apclust_descriptions.txt')).readlines()]
    return data,clust_desc,dates,subcodes


def load_wincorr_data():
    wincorr=numpy.loadtxt(os.path.join(basedir,'rsfmri/module_within_corr.txt'))
    netnames=['1_Default','2_Second_Visual','3_Frontal-Parietal','4.5_First_Visual_V1plus',
              '5_Dorsal_Attention','7_Ventral_Attention',
              '8_Salience','9_Cingulo-opercular','10_Somatomotor','11.5_Frontal-Parietal_Other',
              '15_Media_Parietal','16_Parieto-Occipital']
    
    subcodes=[i.strip() for i in open(os.path.join(basedir,'subcodes.txt')).readlines()]
    return wincorr,netnames,subcodes

def load_bwcorr_data():
    wincorr=numpy.loadtxt(os.path.join(basedir,'rsfmri/module_between_corr.txt'))
    labels=[i.strip().replace('\t','-') for i in open(os.path.join(basedir,'rsfmri/bwmod_corr_labels.txt')).readlines()]
    
    subcodes=[i.strip() for i in open(os.path.join(basedir,'subcodes.txt')).readlines()]
    return wincorr,labels,subcodes
    
def load_fullcorr_data():
    fullcorr=numpy.load(os.path.join(basedir,'rsfmri/corrdata.npy'))
    subcodes=[i.strip() for i in open(os.path.join(basedir,'subcodes.txt')).readlines()]

    return fullcorr,subcodes

#def load_partialcorr_data(cross_thresh=False,thresh=0.05):
#    thresh_dict={0.01:0,0.025:1,0.05:2,0.075:3,0.1:4}
#    
#    partialcorr=numpy.load('/Users/poldrack/Dropbox/data/selftracking/rsfmri/huge_adj.npy')
#    subcodes=[i.strip() for i in open('/Users/poldrack/Dropbox/data/selftracking/rsfmri/subcodes.txt').readlines()]
#    if not cross_thresh:
#        pc=partialcorr[:,thresh_dict[thresh],:]
#        pc=pc.squeeze()
#    else:
#        pc=numpy.sum(partialcorr,1)
#    v=numpy.var(pc,0)
#    pc_good=pc[:,v>0]
#    return pc_good,subcodes

#def load_illness_data():
#    f=open('/Users/poldrack/code/selftracking/analysis_metadata/health_and_drawdates.txt')
#    lines=[i.strip().split() for i in f.readlines()]
#    f.close()
#    illness=[]
#    for l in lines:
#        if not l[1]=='none':
#            illness.append(1)
#        else:
#            illness.append(0)
#    illness=numpy.array(illness)
#    return illness
