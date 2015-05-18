"""
preprocessing for metabolomics data
"""

import os
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.get_data import *


filepath=os.path.dirname(os.path.abspath(__file__))

basedir=os.environ['MYCONNECTOME_DIR']
metabdir=os.path.join(basedir,'metabolomics')
if not os.path.exists(metabdir):
    os.mkdir(metabdir)
    
show_R_web_reports=False

if not os.path.exists(os.path.join(metabdir,'metabolomics.txt')):
    get_file_from_s3('ds031/metabolomics/metabolomics.txt',os.path.join(metabdir,'metabolomics.txt'))

if not os.path.exists(os.path.join(metabdir,'metabolomics_labels.txt')):
    get_file_from_s3('ds031/metabolomics/metabolomics_labels.txt',os.path.join(metabdir,'metabolomics_labels.txt'))


if not os.path.exists(os.path.join(metabdir,'Metabolomics_clustering.html')):
    f=open(os.path.join(filepath,'knit_metab_cluster.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%metabdir)
    f.write("knit('%s/Metabolomics_clustering.Rmd', '%s/Metabolomics_clustering.md')\n"%
        (filepath.replace('scripts','metabolomics'),metabdir))
    f.write("markdownToHTML('%s/Metabolomics_clustering.md', '%s/Metabolomics_clustering.html')\n"%
        (metabdir,metabdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_metab_cluster.R'%filepath)

