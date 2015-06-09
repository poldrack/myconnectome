"""
preprocessing for metabolomics data
"""

import os
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.get_data import *


filepath=os.path.dirname(os.path.abspath(__file__))
basepath=os.path.dirname(filepath)

basedir=os.environ['MYCONNECTOME_DIR']
metabdir=os.path.join(basedir,'metabolomics')
if not os.path.exists(metabdir):
    os.mkdir(metabdir)
    
show_R_web_reports=False

# check R dependencies

R_dependencies=['apcluster']

f=open(os.path.join(filepath,'check_depends.R'),'w')
f.write('# automatically generated knitr command file\n')
f.write('source("%s/utils/pkgTest.R")\n'%basepath)
for d in R_dependencies:
    f.write('pkgTest("%s")\n'%d)
f.close()
run_shell_cmd('Rscript %s/check_depends.R'%filepath)


if not os.path.exists(os.path.join(metabdir,'Metabolomics_clustering.html')):
    f=open(os.path.join(filepath,'knit_metab_cluster.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('setwd("%s")\n'%metabdir)
    f.write("knit('%s/Metabolomics_clustering.Rmd', '%s/Metabolomics_clustering.md')\n"%
        (filepath.replace('scripts','metabolomics'),metabdir))
    f.write("markdownToHTML('%s/Metabolomics_clustering.md', '%s/Metabolomics_clustering.html')\n"%
        (metabdir,metabdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_metab_cluster.R'%filepath)

if not os.path.exists(os.path.join(metabdir,'Make_metabolomics_table.html')):
    f=open(os.path.join(filepath,'knit_metab_table.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('setwd("%s")\n'%metabdir)
    f.write("knit('%s/Make_metabolomics_table.Rmd', '%s/Make_metabolomics_table.md')\n"%
        (filepath.replace('scripts','metabolomics'),metabdir))
    f.write("markdownToHTML('%s/Make_metabolomics_table.md', '%s/Make_metabolomics_table.html')\n"%
        (metabdir,metabdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_metab_table.R'%filepath)

