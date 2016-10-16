"""
analysis inspired by
http://www.nature.com/mp/journal/vaop/ncurrent/full/mp2016143a.html
"""
import sys
import pandas,numpy
import statsmodels.api as sm


sys.path.append('../timeseries')
from load_myconnectome_data import *


xvar_names=['panas.positive','panas.negative']

rnaseq_data,gene_names,rnaseq_dates,rnaseq_subcodes=load_rnaseq_data(use_wgcna=False)
behavdata,behav_vars,behav_dates,behav_subcodes=load_behav_data(xvars=xvar_names)


rnaseq_joint,behavdata_joint,subcodes_joint=get_matching_datasets(rnaseq_data,behavdata,rnaseq_subcodes,behav_subcodes)
X=sm.add_constant(behavdata_joint)

geneidx=[i for i in range(len(gene_names)) if gene_names[i].find('MIR181')==0]
assert len(geneidx)==1
genedata=rnaseq_joint[:,geneidx[0]]
#print(numpy.corrcoef(genedata,behavdata_joint[:,0])[0,1])
#print(numpy.corrcoef(genedata,behavdata_joint[:,1])[0,1])

rlm_model = sm.RLM(genedata, X, M=sm.robust.norms.HuberT())
rlm_results = rlm_model.fit()
print (rlm_results.params)
