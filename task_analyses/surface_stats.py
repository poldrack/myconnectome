"""
load surface cope/varcope data and run fixed effects mode
"""

import os,sys,glob
import nibabel.gifti.giftiio
import numpy
import run_shell_cmd
import statsmodels.api as sm

#task=1
#copenum=32



try:
    task=int(sys.argv[1])
    copenum=int(sys.argv[2])
except:
    task=2
    copenum=2

basedir='/corral-repl/utexas/poldracklab/data/selftracking/'

for hemis in ['L','R']:
    copefiles=glob.glob(os.path.join(basedir,'sub*/model/model%03d/task%03d_run*_333.feat/stats_pipeline/cope%03d.%s.smoothed.func.gii'%(task,task,copenum,hemis)))

    if len(copefiles)==0:
        print 'problem - no copefiles for',task,copenum,hemis
    copedata={}
    varcopedata={}
    ctr=0
    for c in copefiles:
        f=nibabel.gifti.giftiio.read(c)
        copedata[ctr]=f.darrays[0].data
        vf=nibabel.gifti.giftiio.read(c.replace('cope','varcope'))
        varcopedata[ctr]=vf.darrays[0].data
        ctr+=1


    ## from jeanette:
    ## the weights (w_i) are 1/sigma2_i, where the sigma2_i are the first level variance estimates.  If you use matrix math, let
    ## W= diagonal matrix with w_i on diagonal
    ## X = vector of 1's
    ## Y= data

    ## beta-hat = (X'WX)^{-1} X'WY
    ## var-beta-hat = (X'WX)^{-1}
    ## T = beta-hat / sqrt (var-beta-hat)

    nvox=len(copedata[0])
    nsess=len(copedata)

    tstat=numpy.zeros(nvox,dtype=numpy.float32)
    cope=numpy.zeros((nsess,nvox))
    varcope=numpy.zeros((nsess,nvox))

    # arrange data into matrices
    for s in range(nsess):
        cope[s,:]=copedata[s]
        varcope[s,:]=varcopedata[s]

    X=numpy.ones((1,nsess)).T

    for v in range(nvox):
        if numpy.min(varcope[:,v])==0:
            continue
        W=numpy.diag(1.0/varcope[:,v])
        if numpy.sum(W)==0:
            continue
        Y=cope[:,v].reshape((nsess,1))
        wls=sm.WLS(Y,X,weights=1.0/varcope[:,v])
        res=wls.fit()
        #beta_hat = numpy.linalg.inv(X.T.dot(W).dot(X)).dot(X.T).dot(W).dot(Y)   #(X'WX)^{-1} X'WY
        #var_beta_hat = numpy.linalg.inv(X.T.dot(W).dot(X)) #(X'WX)^{-1}
        #tstat[v]=beta_hat / numpy.sqrt(var_beta_hat)
        tstat[v]=res.tvalues[0]

    outdir='/corral-repl/utexas/poldracklab/data/selftracking/surface_stats_333'

    fname=os.path.join(outdir,'task%03d_cope%03d.%s.tstat.smoothed.func.gii'%(task,copenum,hemis))
    if hemis=='L':
        structure='CORTEX_LEFT'
    else:
        structure='CORTEX_RIGHT'
    img=nibabel.gifti.GiftiImage()
    img.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(tstat,intent=f.darrays[0].intent,datatype=f.darrays[0].datatype,ordering='F',meta={'Name':'task%03d_cope%03d.tstat'%(task,copenum)}))
    nibabel.gifti.giftiio.write(img,fname)
    cmd='wb_command -set-structure %s %s'%(fname,structure)
    run_shell_cmd.run_shell_cmd(cmd)
