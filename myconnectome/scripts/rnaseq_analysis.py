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
basepath=os.path.dirname(filepath)

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
if not os.path.exists(os.path.join(rnaseqdir,'drawdates.txt')):
    get_file_from_s3('ds031/RNA-seq/drawdates.txt',os.path.join(rnaseqdir,'drawdates.txt'))
if not os.path.exists(os.path.join(rnaseqdir,'rnaseq-subcodes.txt')):
    get_file_from_s3('ds031/RNA-seq/pathsubs.txt',os.path.join(rnaseqdir,'rnaseq-subcodes.txt'))


# check R dependencies

R_dependencies=['knitr','WGCNA','DESeq','RColorBrewer','vsn','gplots']

f=open(os.path.join(filepath,'check_depends.R'),'w')
f.write('# automatically generated knitr command file\n')
f.write('source("%s/utils/pkgTest.R")\n'%basepath)
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
if not os.path.exists(os.path.join(rnaseqdir,'WGCNA/DAVID_thr8_prefilt_rin3PCreg_GO_set063.txt')):
    try:
        os.environ['DAVID_EMAIL']
        get_WGCNA_DAVID_annotation.get_WGCNA_DAVID_annotation()
    except:
        print 'Environment variable DAVID_EMAIL is not set'
        print 'downloading precomputed results from S3'
        get_s3_directory('RNA-seq/DAVID_annotations',os.path.join(basedir,'rna-seq/WGCNA'))
        f=open(os.path.join(basedir,'rna-seq/WGCNA/USING_CACHED_RESULTS'),'a')
        f.write('DAVID')
        f.close()

    
# do annotation using DAVID
if not os.path.exists(os.path.join(rnaseqdir,'WGCNA/module_descriptions')):
    get_module_descriptions.get_module_descriptions()
    
# do snyderome preparation
if not os.path.exists(os.path.join(rnaseqdir,'snyderome/Snyderome_data_preparation.html')):
    if not os.path.exists(os.path.join(rnaseqdir,'snyderome')):
        os.mkdir(os.path.join(rnaseqdir,'snyderome'))
    f=open(os.path.join(filepath,'knit_snyderome_prep.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%os.path.join(rnaseqdir,'snyderome'))
    f.write("knit('%s/Snyderome_data_preparation.Rmd', '%s/Snyderome_data_preparation.md')\n"%
        (filepath.replace('scripts','rnaseq'),os.path.join(rnaseqdir,'snyderome')))
    f.write("markdownToHTML('%s/Snyderome_data_preparation.md', '%s/Snyderome_data_preparation.html')\n"%
        (os.path.join(rnaseqdir,'snyderome'),os.path.join(rnaseqdir,'snyderome')))
    f.close()
    if show_R_web_reports:
        browseURL(paste('file://', file.path(getwd(),'Snyderome_data_preparation.html'), sep='')) # open file in browser   
    run_shell_cmd('Rscript %s/knit_snyderome_prep.R'%filepath)

# do comparison to snyderome
if not os.path.exists(os.path.join(rnaseqdir,'rna-seq/snyderome_vs_myconnectome.txt')):
    compare_snyderome_myconnectome.compare_snyderome_myconnectome()
 
