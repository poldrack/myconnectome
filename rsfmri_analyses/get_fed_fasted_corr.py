import numpy
import scipy.stats

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0

    return z

def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)

d=numpy.load('/Users/poldrack/Dropbox/data/selftracking/rsfmri/corrdata.npy')
f=open('/Users/poldrack/Dropbox/data/selftracking/rsfmri/subcodes.txt')
subcodes=[i.strip() for i in f.readlines()]
f.close()

tuesdays=[]
thursdays=[]
f=open('/Users/poldrack/Dropbox/code/selftracking/analysis_metadata/trackingdata.txt')
day_of_week={}
header=f.readline()
for l in f.readlines():
    l_s=l.strip().split()
    if l_s[0] in subcodes:
        day_of_week[l_s[0]]=l_s[19]
    if l_s[19]=='2':
        tuesdays.append(l_s[0])
    if l_s[19]=='4':
        thursdays.append(l_s[0])
    
f.close()

daycodes=[]
ctr=0
for s in subcodes:
    try:
        daycodes.append(int(day_of_week[s]))
    except:
        daycodes.append(0)
        print 'problem with',s
daycodes=numpy.array(daycodes)

tuesday_corr=d[daycodes==2,:]
thursday_corr=d[daycodes==4,:]

mean_corr={}
mean_corr['thursday']=z_to_r(numpy.mean(r_to_z(thursday_corr),0))
mean_corr['tuesday']=z_to_r(numpy.mean(r_to_z(tuesday_corr),0))
var={}
var['tuesday']=numpy.var(r_to_z(tuesday_corr),0)
var['thursday']=numpy.var(r_to_z(thursday_corr),0)

numpy.save('/Users/poldrack/Dropbox/data/selftracking/rsfmri/meancorr_tuesday.npy',mean_corr['tuesday'])
numpy.save('/Users/poldrack/Dropbox/data/selftracking/rsfmri/meancorr_thursday.npy',mean_corr['thursday'])

numpy.save('/Users/poldrack/Dropbox/data/selftracking/rsfmri/var_tuesday.npy',var['tuesday'])
numpy.save('/Users/poldrack/Dropbox/data/selftracking/rsfmri/var_thursday.npy',var['thursday'])

tuesday_var_full=numpy.zeros((634,634))
tuesday_var_full[numpy.triu_indices(634,1)]=var['tuesday']
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/tuesday_var_adjmtx.txt',tuesday_var_full)

thursday_var_full=numpy.zeros((634,634))
thursday_var_full[numpy.triu_indices(634,1)]=var['thursday']
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/thursday_var_adjmtx.txt',thursday_var_full)

