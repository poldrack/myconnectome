
module load intel/14.0.1.106
module load mvapich2/2.0b
module load perl
module load fastx_toolkit
module load samtools
module load picard/1.98
module load Rstats/3.0.3
module load python/2.7.6
module load htseq
export PATH=/work/01329/poldrack/software_stampede/bowtie2-2.2.2:/work/01329/poldrack/software_stampede/tophat-2.0.11.Linux_x86_64:${PATH}


java -jar ${TACC_PICARD_DIR}/ReorderSam.jar I=/scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/sub002/accepted_hits_sorted.bam O=/scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/sub002/accepted_hits_sorted_reordered.bam REFERENCE=/scratch/projects/UT/poldracklab/poldrack/selftracking/hg19/Sequence/WholeGenomeFasta/genome.fa
