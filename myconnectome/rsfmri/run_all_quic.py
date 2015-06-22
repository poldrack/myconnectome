import os,glob




subcodes=[os.path.basename(i).replace(".txt",'') for i in glob.glob('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/combined_data_scrubbed/sub*.txt')]
subcodes.sort()

threshvals=['0.005','0.01','0.025','0.05','0.075','0.1']

for t in threshvals:
    f=open('run_all_quic_%s.sh'%t,'w')
    if not os.path.exists('/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/rsfmri/quic/quic_precision_%s'%t):
        os.mkdir('/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/rsfmri/quic/quic_precision_%s'%t)
    
    for s in subcodes:
        f.write('Rscript quic_density.R %s %s\n'%(s,t))
    f.close()
