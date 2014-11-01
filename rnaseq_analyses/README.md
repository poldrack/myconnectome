## Analysis and processing code for RNA-seq data

The RNA-seq workflow is as follows (starting with a set of paired-end read files; for some sessions there were two lanes, for others only a single lane).

#### data


#### Preprocessing

*process_rnaseq.py: This Python script generates a set of shell scripts for each RNA-seq dataset, which are then run using the grid on TACC Stampede. The raw read data have been uploaded to the Sequence Read Archive (http://www.ncbi.nlm.nih.gov/sra) and will become available upon publication of the results.  They can also be requested directly from Russ Poldrack. 


Examples of the scripts used to run each specific processing step are also included:

* tophat_cmd.sh: perform alignment to hg19 genome using bowtie2 via tophat
* samtools_cmd.sh: sort tophat output
* reorder_cmd.sh: reorder sorted output
* index_cmd.sh: generate bam index for reordered dataset
* htseq_cmd.sh: sort gam file by read, and use htseq-count to get per-gene read counts

#### Post-processing


* RNAseq_data_preparation.Rmd: Rmarkdown code to generate variance-stabilized RNA-seq data and perform some QA on the results.  This code uses the data located in the cloud, so it does not require downloading any additional data.  The results can be viewed at https://s3.amazonaws.com/openfmri/ds031/RNA-seq/RNAseq_data_preparation.html

