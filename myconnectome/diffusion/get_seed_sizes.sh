ls parcels_dtispace/* > foo
cat foo | sed 's/^/fslstats /' | sed 's/$/ -V/' | bash > tmp
cat tmp | cut -d" " -f1 > seedsizes
rm tmp
