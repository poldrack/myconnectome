ls ../../rna-seq/expression_sep_files/| sed 's/expr_snpPCreg_//' | sed 's/.txt//' | sed 's/^/Rscript gwas_wincorr.R /'>run_all_gwas.sh
