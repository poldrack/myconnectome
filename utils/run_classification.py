import numpy
from get_balanced_folds import get_balanced_folds
import sklearn.svm
from ts_shuffle import ts_shuffle
from sklearn import cross_validation


def run_classification(x,ydata,shuffle=False,n_train_runs=50,n_shuffle_runs=100,verbose=True,type='regression',nfolds=6,clf=sklearn.svm.SVR(kernel='linear')):
    if shuffle==True:
        nruns=n_shuffle_runs
    else:
        nruns=n_train_runs
    
        
    if len(ydata.shape)==1:
        nvars=1
    else:
        nvars=ydata.shape[1]
    
    predacc=numpy.zeros((nruns,nvars))
    for run in range(nruns):
        if not shuffle:
            y_all=ydata.copy()
        else:
            y_all=ts_shuffle(ydata)
        for var in range(nvars):
            if nvars==1:
                y=y_all
            else:
                y=y_all[:,var]
            if len(numpy.unique(y[numpy.isfinite(y)]))>2:
                clf=sklearn.svm.SVR(kernel='linear')
            else:
                clf=sklearn.svm.LinearSVC()
                
            goodcases=numpy.array([not i for i in numpy.isnan(y)])
            y_good=sklearn.preprocessing.scale(y[goodcases])
            x_good=sklearn.preprocessing.scale(x[goodcases,:])
            
            if type=='regression':
                cv=get_balanced_folds(y_good,nfolds)
            else:
                cv=cross_validation.KFold(n=len(y_good),n_folds=nfolds,shuffle=True)
            
            testdata=numpy.zeros(len(y_good))
            for train,test in cv:
                clf.fit(x_good[train,:],y_good[train])
                testdata[test]=clf.predict(x_good[test,:])
            predacc[run,var]=numpy.corrcoef(testdata,y_good)[0,1]
            if verbose:
                print run,var,predacc[run,var],x_good.shape
    return predacc
