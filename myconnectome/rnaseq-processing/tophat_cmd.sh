
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
which bowtie

tophat -o /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/tophat_output/sub002 --rg-id Paired --rg-library RNAseq --rg-sample sub002 --rg-platform ILLUMINA     -G /scratch/projects/UT/poldracklab/poldrack/selftracking/hg19/Annotation/Genes/genes.gtf --mate-inner-dist 100     --b2-very-sensitive -p 15 -r 250     --transcriptome-index /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/transcriptome/known     /scratch/projects/UT/poldracklab/poldrack/selftracking/hg19/Sequence/Bowtie2Index/genome     /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/seqdata/sub002/sub002_L1_R1.fastq,/scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/seqdata/sub002/sub002_L2_R1.fastq /scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/seqdata/sub002/sub002_L1_R2.fastq,/scratch/projects/UT/poldracklab/poldrack/selftracking/rna-seq/seqdata/sub002/sub002_L2_R2.fastq
