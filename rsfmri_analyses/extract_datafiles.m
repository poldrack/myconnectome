cd /corral-repl/utexas/poldracklab/data/selftracking/laumann
data=load('parcel_timecourses_LR_mirpad_startpos50.mat')

s=textscan(fopen('all_selected_sessions_names.txt'),'%s')
sessnames=s{1}

for x=1:84,
    d=data.watertime_both(x);
    dd=d{1};
    fname=sprintf('/corral-repl/utexas/poldracklab/data/selftracking/subdata/%s.txt',sessnames{x})
    save(fname,'dd','-ASCII')
end    
asdf

tmasks=load('all_selected_sessions_tmasks.mat')
for x=1:84,
    tmask=tmasks.tmasks(:,x)
    fname=sprintf('/corral-repl/utexas/poldracklab/data/selftracking/tmasks/%s.txt',sessnames{x})
    save(fname,'tmask','-ASCII')
end    
