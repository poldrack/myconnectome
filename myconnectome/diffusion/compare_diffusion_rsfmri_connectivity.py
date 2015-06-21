"""
compare diffusion and rsmri across thresholds

"""


import os
import numpy
import scipy.stats
import matplotlib.pyplot as plt

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0

    return z

def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)

def pcor_from_precision(P,zero_diagonal=1):
    # given a precision matrix, compute the partial correlation matrix
    # based on wikipedia page: http://en.wikipedia.org/wiki/Partial_correlat
    #Using_matrix_inversion
    pcor=numpy.zeros(P.shape)
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            pcor[i,j]=P[i,j]/numpy.sqrt(P[i,i]*P[j,j])
            if zero_diagonal==1 and i==j:
                pcor[i,j]=0
    return pcor


basedir=os.environ['MYCONNECTOME_DIR']
use_abs_corr=False

dtidata=numpy.loadtxt(os.path.join(basedir,'diffusion/tracksumm_distcorr.txt'),skiprows=1)
dtidata=dtidata[:,1:]
dtidata=dtidata+dtidata.T

rsfmridata=numpy.load(os.path.join(basedir,'rsfmri/corrdata.npy'))

rsfmridata=r_to_z(rsfmridata)
meancorr_z=numpy.mean(rsfmridata,0)
meancorr=z_to_r(meancorr_z)
if use_abs_corr:
    meancorr=numpy.abs(meancorr)

meancorr[numpy.isnan(meancorr)]=0
adjsize=630
utr=numpy.triu_indices(adjsize,1)
meandti=dtidata[utr]

task_connectome=numpy.loadtxt(os.path.join(basedir,'taskfmri/task_connectome.txt'))
taskdata=task_connectome[utr]

l2data=numpy.load(os.path.join(basedir,'rsfmri/l2_utr_data.npy'))
l2mean=z_to_r(numpy.mean(r_to_z(l2data),0))

randshuffle=False


tvals=[0.005,0.01,0.025,0.05,0.075] #numpy.arange(0.001,0.5,0.005)
tstr=['0.005','0.01','0.025','0.05','0.075']
nrand=1000
overlap={'rs-dti':numpy.zeros(len(tvals)),'rs-task':numpy.zeros(len(tvals)),
      'dti-task':numpy.zeros(len(tvals)),'l1-dti':numpy.zeros(len(tvals)),
    'l2-dti':numpy.zeros(len(tvals))}      
overlap_rand={'rs-dti':numpy.zeros((len(tvals),nrand)),'rs-task':numpy.zeros((len(tvals),nrand)),
      'dti-task':numpy.zeros((len(tvals),nrand)),'l1-dti':numpy.zeros((len(tvals),nrand)),
    'l2-dti':numpy.zeros((len(tvals),nrand))}      
rsthresh=numpy.zeros(len(tvals))
dtithresh=numpy.zeros(len(tvals))
taskthresh=numpy.zeros(len(tvals))
l2thresh=numpy.zeros(len(tvals))
l1thresh=numpy.zeros(len(tvals))

meandti_rand=meandti.copy()

for t in range(len(tvals)):        
    dtibin=meandti>0
    thresh=tvals[t]
    l1data=numpy.load(os.path.join(basedir,'rsfmri/quic_utr_data_%s.npy'%tstr[t]))
    l1mean=z_to_r(numpy.mean(r_to_z(l1data),0))
    rsthresh[t]=scipy.stats.scoreatpercentile(meancorr,100-100*thresh)
    dtithresh[t]=scipy.stats.scoreatpercentile(meandti,100-100*thresh)
    taskthresh[t]=scipy.stats.scoreatpercentile(taskdata,100-100*thresh)
    l2thresh[t]=scipy.stats.scoreatpercentile(l2mean,100-100*thresh)
    l1thresh[t]=scipy.stats.scoreatpercentile(l1mean,100-100*thresh)
    overlap['rs-dti'][t]=numpy.mean(dtibin[meancorr>rsthresh[t]])
    overlap['dti-task'][t]=numpy.mean(dtibin[taskdata>taskthresh[t]])
    overlap['l1-dti'][t]=numpy.mean(dtibin[l1mean>l1thresh[t]])
    overlap['l2-dti'][t]=numpy.mean(dtibin[l2mean>l2thresh[t]])
    for randruns in range(nrand):
        meandti_rand=meandti_rand[numpy.random.permutation(len(utr[0])).astype('int')]
        dtibin_rand=meandti_rand>0
        overlap_rand['rs-dti'][t,randruns]=numpy.mean(dtibin_rand[meancorr>rsthresh[t]])
        overlap_rand['dti-task'][t,randruns]=numpy.mean(dtibin_rand[taskdata>taskthresh[t]])
        overlap_rand['l1-dti'][t,randruns]=numpy.mean(dtibin_rand[l1mean>l1thresh[t]])
        overlap_rand['l2-dti'][t,randruns]=numpy.mean(dtibin_rand[l2mean>l2thresh[t]])
        
overlap_cutoff={'rs-dti':numpy.zeros(len(tvals)),'l1-dti':numpy.zeros(len(tvals)),
                'l2-dti':numpy.zeros(len(tvals)),'dti-task':numpy.zeros(len(tvals))}
                
for t in range(len(tvals)):        
    overlap_cutoff['rs-dti'][t]=scipy.stats.scoreatpercentile(overlap_rand['rs-dti'][t,:],95)
    overlap_cutoff['l1-dti'][t]=scipy.stats.scoreatpercentile(overlap_rand['l1-dti'][t,:],95)
    overlap_cutoff['l2-dti'][t]=scipy.stats.scoreatpercentile(overlap_rand['l2-dti'][t,:],95)
    overlap_cutoff['dti-task'][t]=scipy.stats.scoreatpercentile(overlap_rand['dti-task'][t,:],95)

# do honey et al. analysis - look at correlation for connections that have nonzero structural connectivity
nonzero_dti=meandti>0
cc_rs_dti=numpy.corrcoef(meancorr[nonzero_dti],meandti[nonzero_dti])[0,1]
cc_task_dti=numpy.corrcoef(taskdata[nonzero_dti],meandti[nonzero_dti])[0,1]

# get full corrmtx
alldata=numpy.vstack((meancorr,taskdata,l1mean,l2mean,meandti))
print numpy.corrcoef(alldata)

plt.plot(tvals,overlap['rs-dti'],'r',tvals,overlap['l1-dti'],'g',tvals,overlap['l2-dti'],'b',tvals,overlap['dti-task'],'k',
         tvals,overlap_cutoff['rs-dti'],'r--',tvals,overlap_cutoff['l1-dti'],'g--',
        tvals,overlap_cutoff['l2-dti'],'b--',tvals,overlap_cutoff['dti-task'],'k--')
plt.legend(['Full correlation','Partial correlation [L1]','Partial correlation [L2]','Task'])
plt.xlabel('Density threshold',fontsize=16)
plt.ylabel('Proportion of DTI overlap',fontsize=16)
plt.savefig(os.path.join(basedir,'rsfmri/rsfmri_diffusion_overlap.pdf'))
plt.show()
