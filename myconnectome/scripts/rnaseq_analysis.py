"""
script to run the entire analysis pathway for RNAseq analyses
NOTE: filter_gene_types was run separately because of the need for vega 
anotation which required local indexing - results are on AWS 

"""

from myconnectome.rnaseq import *
from myconnectome.utils.get_data import *
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.log_time import log_time, get_time
import os

filepath=os.path.dirname(os.path.abspath(__file__))
basepath=os.path.dirname(filepath)

show_R_web_reports=False

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')


try:
    timefile = os.environ["TIME_LOG_FILE"]
except:
    raise RuntimeError('you must first set the TIME_LOG_FILE environmental variable')


rnaseqdir=os.path.join(basedir,'rna-seq')

if not os.path.exists(rnaseqdir):
    os.mkdir(rnaseqdir)



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
    starttime = get_time()
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
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'RNAseq_data_preparation.html'))


# do regression against RIN and first 3 PCs
if not os.path.exists(os.path.join(rnaseqdir,'varstab_data_prefiltered_rin_3PC_regressed.txt')):
    starttime = get_time()
    regress_rin_pca.regress_rin_pca()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'varstab_data_prefiltered_rin_3PC_regressed.txt'))
    
# run WGCNA
if not os.path.exists(os.path.join(rnaseqdir,'Run_WGCNA.html')):
    print 'Running WGCNA - this could take a little while...'
    starttime = get_time()
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
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'Run_WGCNA.html'))


# extract ImmPort pathways

if not os.path.exists(os.path.join(rnaseqdir,'ImmPort/ImmPort_eigengenes_prefilt_rin3PCreg.txt')):
    starttime = get_time()
    get_ImmPort_eigengenes.get_ImmPort_eigengenes()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'ImmPort/ImmPort_eigengenes_prefilt_rin3PCreg.txt'))

# do annotation using DAVID
if not os.path.exists(os.path.join(rnaseqdir,'WGCNA/DAVID_thr8_prefilt_rin3PCreg_GO_set063.txt')):
    starttime = get_time()
    try:
        os.environ['DAVID_EMAIL']
        get_WGCNA_DAVID_annotation.get_WGCNA_DAVID_annotation()
    except:
        print 'Environment variable DAVID_EMAIL is not set'
        print 'downloading precomputed results from S3'
        get_directory('david')
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'WGCNA/DAVID_thr8_prefilt_rin3PCreg_GO_set063.txt'))
    
# do annotation using DAVID
if not os.path.exists(os.path.join(rnaseqdir,'WGCNA/module_descriptions')):
    starttime = get_time()
    get_module_descriptions.get_module_descriptions()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(os.path.join(rnaseqdir,'WGCNA/module_descriptions')))
    
    
# make table
if not os.path.exists(os.path.join(rnaseqdir,'Make_rnaseq_table.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_rnaseq_table.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%rnaseqdir)
    f.write("knit('%s/Make_rnaseq_table.Rmd', '%s/Make_rnaseq_table.md')\n"%
        (filepath.replace('scripts','rnaseq'),rnaseqdir))
    f.write("markdownToHTML('%s/Make_rnaseq_table.md', '%s/Make_rnaseq_table.html')\n"%
        (rnaseqdir,rnaseqdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_rnaseq_table.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'Make_rnaseq_table.html'))

# make QA page
if not os.path.exists(os.path.join(rnaseqdir,'QA_summary_rnaseq.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_rnaseq_qa.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%rnaseqdir)
    f.write("knit('%s/QA_summary_rnaseq.Rmd', '%s/QA_summary_rnaseq.md')\n"%
        (filepath.replace('scripts','qa'),rnaseqdir))
    f.write("markdownToHTML('%s/QA_summary_rnaseq.md', '%s/QA_summary_rnaseq.html')\n"%
        (rnaseqdir,rnaseqdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_rnaseq_qa.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(os.path.join(rnaseqdir,'QA_summary_rnaseq.html')))

# do snyderome preparation
if not os.path.exists(os.path.join(rnaseqdir,'snyderome/Snyderome_data_preparation.html')):
    starttime = get_time()
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
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'snyderome/Snyderome_data_preparation.html'))

# do comparison to snyderome
if not os.path.exists(os.path.join(rnaseqdir,'rna-seq/snyderome_vs_myconnectome.txt')):
    starttime = get_time()
    compare_snyderome_myconnectome.compare_snyderome_myconnectome()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rnaseqdir,'rna-seq/snyderome_vs_myconnectome.txt'))
