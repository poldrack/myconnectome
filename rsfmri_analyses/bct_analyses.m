% get net stats using BCT
path(path,'/home1/01329/poldrack/BCT')

Q=zeros(84,1);
clustering_pos=zeros(84,634);
clustering_neg=zeros(84,634);
Ppos=zeros(84,634);
Pneg=zeros(84,634);
Geff_pos=zeros(84,1);
Geff_neg=zeros(84,1);
bwc_pos=zeros(84,634);
bwc_neg=zeros(84,634);
assort_pos=zeros(84,1);
assort_neg=zeros(84,1);

basedir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses'
for session = 1:84
    data=textread(sprintf('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/corrdata_files/corrdata_sess%02d.txt',session));
    [Ci,Q(session)]=modularity_louvain_und_sign(data);
    [Ppos(session,:), Pneg(session,:)] = participation_coef_sign(data,Ci);
    datapos=data;
    datapos(find(data<0))=0;
    clustering_pos(session,:)=clustering_coef_wu(datapos);
    Geff_pos(session)=efficiency_wei(datapos);
    dataneg=data*-1;
    dataneg(find(data<0))=0;
    clustering_neg(session,:)=clustering_coef_wu(dataneg);
    Geff_neg(session)=efficiency_wei(dataneg);
    bwc_pos(session,:)=betweenness_wei(datapos);
    bwc_neg(session,:)=betweenness_wei(dataneg);
    
    assort_pos(session)=assortativity_wei(datapos,0);
    assort_neg(session)=assortativity_wei(dataneg,0);
    
    sprintf('%d',session)
end

Ppos=transpose(Ppos);
Pneg=transpose(Pneg);
bwc_pos=transpose(bwc_pos);
bwc_neg=transpose(bwc_neg);
clustering_pos=transpose(clustering_pos);
clustering_neg=transpose(clustering_neg);

save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/clustering_pos.txt' clustering_pos '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/clustering_neg.txt' clustering_neg '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/bwc_pos.txt' bwc_pos '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/bwc_neg.txt' bwc_neg '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/geff_pos.txt' Geff_pos '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/geff_neg.txt' Geff_neg  '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/assort_pos.txt' assort_pos '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/assort_neg.txt' assort_neg '-ascii' '-tabs'

save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/modularity_weighted_louvain_bct.txt' Q '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/PIpos_weighted_louvain_bct.txt' Ppos '-ascii' '-tabs'
save '/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/PIneg_weighted_louvain_bct.txt' Pneg '-ascii' '-tabs'
