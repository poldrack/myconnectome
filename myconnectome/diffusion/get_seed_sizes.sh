module load fsl

echo "Getting seed sizes for combined eddy corrected..."
cd /scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/stanford_diffusion/combined_eddy_corrected/
ls seed_masks/* > foo
cat foo | sed 's/^/fslstats /' | sed 's/$/ -V/' | bash > tmp
cat tmp | cut -d" " -f1 > seedsizes
rm tmp

#echo "Getting seed sizes for skyra..."
#cd /scratch/PI/russpold/data/MYCONNECTOME/skyra_data/
#ls seed_masks/* > foo
#cat foo | sed 's/^/fslstats /' | sed 's/$/ -V/' | bash > tmp
#cat tmp | cut -d" " -f1 > seedsizes
rm tmp
