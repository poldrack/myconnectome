"""
script to run the entire analysis pathway for RNAseq analyses
NOTE: filter_gene_types was run separately because of the need for vega 
anotation which required local indexing - results are on AWS 

"""

from myconnectome.rnaseq import *
from myconnectome.utils.get_data import *
from myconnectome.utils.run_shell_cmd import run_shell_cmd
import os

filepath=os.path.dirname(os.path.abspath(__file__))

show_R_web_reports=False

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')


rnaseqdir=os.path.join(basedir,'rna-seq')

if not os.path.exists(rnaseqdir):
    os.mkdir(rnaseqdir)

if not os.path.exists(os.path.join(rnaseqdir,'rin.txt')):
    get_file_from_s3('ds031/RNA-seq/rin.txt',os.path.join(rnaseqdir,'rin.txt'))


# check R dependencies

R_dependencies=['knitr','WGCNA','DESeq','RColorBrewer','vsn','gplots','asstit']

f=open(os.path.join(filepath,'check_depends.R'),'w')
f.write('# automatically generated knitr command file\n')
f.write('pkgTest <- function(x)\n')
f.write('  {\n')
f.write('    if (!require(x,character.only = TRUE))\n')
f.write('    {\n')
f.write('      install.packages(x,dep=TRUE)\n')
f.write('        if(!require(x,character.only = TRUE)) stop("Package not found")\n')
f.write('    }\n')
f.write('  }\n')
for d in R_dependencies:
    f.write('pkgTest("%s")\n'%d)
f.close()
run_shell_cmd('Rscript %s/check_depends.R'%filepath)



# do variance stabilization
# make a knitr command file to knit html for the Rmd file
if not os.path.exists(os.path.join(rnaseqdir,'RNAseq_data_preparation.html')):
    f=open(os.path.join(filepath,'knit_rnaseq_prep.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%rnaseqdir)
    f.write("knit('%s/RNAseq_data_preparation.Rmd', '%s/RNAseq_data_preparation.md')\n"%
        (filepath.replace('scripts','rnaseq'),rnaseqdir))
    f.write("markdownToHTML('%s/RNAseq_data_preparation.md', '%s/RNAseq_data_preparation.html')\n"%
        (rnaseqdir,rnaseqdir))
    f.close()
    if show_R_web_reports:
        browseURL(paste('file://', file.path(getwd(),'RNAseq_data_preparation.html'), sep='')) # open file in browser   
    run_shell_cmd('Rscript %s/knit_rnaseq_prep.R'%filepath)


# do regression against RIN and first 3 PCs
if not os.path.exists(os.path.join(rnaseqdir,'varstab_data_prefiltered_rin_3PC_regressed.txt')):
    regress_rin_pca.regress_rin_pca()
    
# run WGCNA
if not os.path.exists(os.path.join(rnaseqdir,'Run_WGCNA.html')):
    print 'Running WGCNA - this could take a little while...'
    if not os.path.exists(os.path.join(rnaseqdir,'WGCNA')):
        os.mkdir(os.path.join(rnaseqdir,'WGCNA'))
    f=open(os.path.join(filepath,'knit_rnaseq_wgcna.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%rnaseqdir)
    f.write("knit('%s/Run_WGCNA.Rmd', '%s/Run_WGCNA.md')\n"%
        (filepath.replace('scripts','rnaseq'),rnaseqdir))
    f.write("markdownToHTML('%s/Run_WGCNA.md', '%s/Run_WGCNA.html')\n"%
        (rnaseqdir,rnaseqdir))
    f.close()
    if show_R_web_reports:
        browseURL(paste('file://', file.path(getwd(),'Run_WGCNA.html'), sep='')) # open file in browser   
    run_shell_cmd('Rscript %s/knit_rnaseq_wgcna.R'%filepath)

# extract ImmPort pathways
if not os.path.exists(os.path.join(rnaseqdir,'ImmPort/all_ImmPort_pathways.txt')):
    if not os.path.exists(os.path.join(rnaseqdir,'ImmPort')):
        os.mkdir(os.path.join(rnaseqdir,'ImmPort'))
    get_file_from_s3('ds031/RNA-seq/all_ImmPort_pathways.txt',os.path.join(rnaseqdir,'ImmPort/all_ImmPort_pathways.txt'))

if not os.path.exists(os.path.join(rnaseqdir,'ImmPort/ImmPort_eigengenes_prefilt_rin3PCreg.txt')):
    get_ImmPort_eigengenes.get_ImmPort_eigengenes()

# do annotation using DAVID
if not os.path.exists(os.path.join(rnaseqdir,'WGCNA/DAVID_thr8_prefilt_rin3PCreg_GO_set001.txt')):
    get_WGCNA_DAVID_annotation.get_WGCNA_DAVID_annotation()