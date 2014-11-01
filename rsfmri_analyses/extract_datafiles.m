cd /Users/poldrack/Dropbox/data/selftracking/rsfmri
data=load('all_selected_sessions_newparcel_timecourses.mat')

s=textscan(fopen('all_selected_sessions_names.txt'),'%s')
sessnames=s{1}

for x=1:84,
    d=data.watertime_both(x);
    dd=d{1};
    fname=sprintf('subdata/%s.txt',sessnames{x})
    save(fname,'dd','-ASCII')
end    
asdf

tmasks=load('all_selected_sessions_tmasks.mat')
for x=1:84,
    tmask=tmasks.tmasks(:,x)
    fname=sprintf('tmasks/%s.txt',sessnames{x})
    save(fname,'tmask','-ASCII')
end    
