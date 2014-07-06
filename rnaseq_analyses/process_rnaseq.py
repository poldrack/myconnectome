"""
run the rna-seq processing stream

- create a shell script that contains all of the appropriate commands

"""

import os,glob,sys
from run_shell_cmd import run_shell_cmd
import launch_slurm
import re

class argsClass:

    def __init__(self):
        self.ncores = 16
        self.qsubfile=None
        self.jobname=None
        self.test=True
        self.run_tophat=True
        self.run_cufflinks=True
        self.run_samtools=True
        self.run_qa=True
        self.keepqsubfile=False

args=argsClass()

testmode=False

module_text="""
module load intel/14.0.1.106
module load mvapich2/2.0b
module load perl
module load fastx_toolkit
module load samtools
module load picard/1.98
module load Rstats/3.0.3
module load python/2.7.6
module load htseq
module load fastqc
export PATH=/work/01329/poldrack/software_stampede/bowtie2-2.2.2:/work/01329/poldrack/software_stampede/tophat-2.0.11.Linux_x86_64:/work/01329/poldrack/software_stampede/cufflinks-2.2.0.Linux_x86_64:${PATH}

"""


basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq'
genomedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/hg19'

samplecodes=[i.split("/")[-1] for i in glob.glob(os.path.join(basedir,'seqdata/sub*'))]
samplecodes.sort()
print samplecodes

RNASEQC='/scratch/projects/UT/poldracklab/poldrack/selftracking/RNA-SeQC_v1.1.7.jar'
GENOME='/scratch/projects/UT/poldracklab/poldrack/selftracking/hg19/Sequence/WholeGenomeFasta/genome.fa'

tophat_outdir=os.path.join(basedir,'tophat_output')
if not os.path.exists(tophat_outdir):
    os.mkdir(tophat_outdir)

cufflinks_outdir=os.path.join(basedir,'cufflinks_output')
if not os.path.exists(cufflinks_outdir):
    os.mkdir(cufflinks_outdir)

qa_outdir=os.path.join(basedir,'qa_output')
if not os.path.exists(qa_outdir):
    os.mkdir(qa_outdir)

insertsize=250

for samplecode in samplecodes:
    print 'using',samplecode

    samp_datadir=os.path.join(basedir,'seqdata/%s'%samplecode)
    assert os.path.exists(samp_datadir)

    tophat_sampdir=os.path.join(tophat_outdir,'%s'%samplecode)
    cufflinks_sampdir=os.path.join(cufflinks_outdir,'%s'%samplecode)
    qa_sampdir=os.path.join(qa_outdir,'%s'%samplecode)

    if not os.path.exists(tophat_sampdir):
        os.mkdir(tophat_sampdir)
    if not os.path.exists(cufflinks_sampdir):
        os.mkdir(cufflinks_sampdir)
    if not os.path.exists(qa_sampdir):
        os.mkdir(qa_sampdir)

    fastqfiles=glob.glob(os.path.join(samp_datadir,'*fastq'))
    if len(fastqfiles)>2:

        sampfiles='%s_L1_R1.fastq,%s_L2_R1.fastq %s_L1_R2.fastq,%s_L2_R2.fastq'%(os.path.join(samp_datadir,samplecode),os.path.join(samp_datadir,samplecode),os.path.join(samp_datadir,samplecode),os.path.join(samp_datadir,samplecode))

    else:
        sampfiles='%s_L1_R1.fastq %s_L1_R2.fastq'%(os.path.join(samp_datadir,samplecode),os.path.join(samp_datadir,samplecode))

    for s in re.split(',| ',sampfiles):
        try:
            assert os.path.exists(s)
        except:
            print 'problem with',s


    jobid=[]
    if not os.path.exists(os.path.join(tophat_sampdir,'accepted_hits.bam')) and args.run_tophat:
        tophat_cmd="tophat -o %s --rg-id Paired --rg-library RNAseq --rg-sample %s --rg-platform ILLUMINA \
    -G %s/Annotation/Genes/genes.gtf --mate-inner-dist 100 \
    --b2-very-sensitive -p 15 -r %d \
    --transcriptome-index %s/transcriptome/known \
    %s/Sequence/Bowtie2Index/genome \
    %s"%(tophat_sampdir,samplecode,genomedir,insertsize,basedir,genomedir,sampfiles)

        print tophat_cmd
        cmdfile=os.path.join(tophat_sampdir,'tophat_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write(tophat_cmd+'\n')
        f.close()
        if testmode:
           args.test=True



    if not os.path.exists(os.path.join(tophat_sampdir,'accepted_hits_sorted_reordered.bam')):

        reorder_cmd='java -jar ${TACC_PICARD_DIR}/ReorderSam.jar I=%s/accepted_hits_sorted.bam O=%s/accepted_hits_sorted_reordered.bam REFERENCE=%s'%(tophat_sampdir,tophat_sampdir,GENOME)

        print reorder_cmd
        cmdfile=os.path.join(tophat_sampdir,'reorder_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write(reorder_cmd+'\n')
        f.close()
        if testmode:
           args.test=True

    if not os.path.exists(os.path.join(tophat_sampdir,'htcount.txt')):

        sortbyread_cmd='samtools sort -n %s/accepted_hits_sorted.bam %s/accepted_hits_sorted_by_read'%(tophat_sampdir,tophat_sampdir)
        htcount_cmd='samtools view %s/accepted_hits_sorted_by_read.bam | htseq-count - /scratch/projects/UT/poldracklab/poldrack/selftracking/hg19/Annotation/Genes/genes.gtf -s no > %s/htcount.txt'%(tophat_sampdir,tophat_sampdir)

        print sortbyread_cmd
        cmdfile=os.path.join(tophat_sampdir,'htseq_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write("export PATH=${PATH}:$TACC_HTSEQ_DIR/bin\n")
        f.write(sortbyread_cmd+'\n')
        f.write(htcount_cmd+'\n')
        f.close()
        if testmode:
           args.test=True


    if not os.path.exists(os.path.join(tophat_sampdir,'accepted_hits_sorted_reordered.bam.bai')):

        index_cmd='samtools index %s/accepted_hits_sorted_reordered.bam'%tophat_sampdir

        print index_cmd
        cmdfile=os.path.join(tophat_sampdir,'index_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write(index_cmd+'\n')
        f.close()
        if testmode:
           args.test=True


    if not os.path.exists(os.path.join(cufflinks_sampdir,'genes.fpkm_tracking')) and args.run_cufflinks:
        cufflinks_cmd='cufflinks -G %s/Annotation/Genes/genes.gtf -p 15 -o %s %s/accepted_hits.bam'%(genomedir,cufflinks_sampdir,tophat_sampdir)

        print cufflinks_cmd
        cmdfile=os.path.join(cufflinks_sampdir,'cufflinks_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write('lfs setstripe -c 1 %s\n'%cufflinks_sampdir)
        f.write(cufflinks_cmd+'\n')
        f.close()
        if testmode:
           args.test=True


    if not os.path.exists(os.path.join(tophat_sampdir,'accepted_hits_sorted.bam')) and args.run_samtools:
        samtools_cmd='samtools sort %s/accepted_hits.bam %s/accepted_hits_sorted'%(tophat_sampdir,tophat_sampdir)


        print samtools_cmd
        cmdfile=os.path.join(tophat_sampdir,'samtools_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write(samtools_cmd+'\n')
        f.close()
        if testmode:
           args.test=True



    if not os.path.exists(os.path.join(qa_sampdir,'insertsize')) and args.run_qa:
        qa_cmd='java -Xmx4g -Djava.io.tmpdir=/tmp -jar ${TACC_PICARD_DIR}/CollectInsertSizeMetrics.jar INPUT=%s/accepted_hits_sorted_reordered.bam OUTPUT=%s/insertsize HISTOGRAM_FILE=%s/insert_hist REFERENCE_SEQUENCE=%s/Sequence/Bowtie2Index/genome.fa'%(tophat_sampdir,qa_sampdir,qa_sampdir,genomedir)

        qa_cmd2='java -Xmx4g -Djava.io.tmpdir=/tmp -jar $TACC_PICARD_DIR/CollectAlignmentSummaryMetrics.jar MAX_INSERT_SIZE=300 INPUT=%s/accepted_hits_sorted_reordered.bam OUTPUT=%s/alignment_metrics REFERENCE_SEQUENCE=%s/Sequence/Bowtie2Index/genome.fa'%(tophat_sampdir,qa_sampdir,genomedir)            

        qa_cmd3='java -Xmx4g -Djava.io.tmpdir=/tmp -jar $TACC_PICARD_DIR/CollectRnaSeqMetrics.jar INPUT=%s/accepted_hits_sorted_reordered.bam OUTPUT=%s/rnaseq_metrics REFERENCE_SEQUENCE=%s/Sequence/Bowtie2Index/genome.fa REF_FLAT=%s/Annotation/Archives/archive-2010-09-27-22-25-17/refFlat.txt STRAND_SPECIFICITY=NONE'%(tophat_sampdir,qa_sampdir,genomedir,genomedir)

        qa_cmd4='java -jar %s -o %s -r %s -t %s/transcripts.gtf -s "%s|%s/accepted_hits_sorted_reordered.bam|None"'%(RNASEQC,qa_sampdir,GENOME,cufflinks_sampdir,samplecode,tophat_sampdir)


        print qa_cmd
        print qa_cmd2
        print qa_cmd3
        #print qa_cmd4

        cmdfile=os.path.join(qa_sampdir,'qa_cmd.sh')
        f=open(cmdfile,'w')
        f.write('%s\n'%module_text)
        f.write(qa_cmd+'\n')
        f.write(qa_cmd2+'\n')
        f.write(qa_cmd3+'\n')
        #f.write(qa_cmd4+'\n')
        f.close()
        if testmode:
           args.test=True



cmd="find /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/*/tophat_cmd.sh | sed 's/^/bash /'> run_all_tophat.sh"
import run_shell_cmd
print cmd
run_shell_cmd.run_shell_cmd(cmd)

cmd="find /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/*/samtools_cmd.sh | sed 's/^/bash /'> run_all_samtools.sh"
print cmd
run_shell_cmd.run_shell_cmd(cmd)

cmd="find /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/*/reorder_cmd.sh | sed 's/^/bash /'> run_all_reorder.sh"
print cmd
run_shell_cmd.run_shell_cmd(cmd)

cmd="find /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/*/index_cmd.sh | sed 's/^/bash /'> run_all_index.sh"
print cmd
run_shell_cmd.run_shell_cmd(cmd)

cmd="find /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/cufflinks_output/*/cufflinks_cmd.sh | sed 's/^/bash /'> run_all_cufflinks.sh"
print cmd
run_shell_cmd.run_shell_cmd(cmd)
