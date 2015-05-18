% get network stats using BCT - https://sites.google.com/site/bctnet/
% BCT must already be in MATLAB path!

Q=zeros(84,1);
Ppos=zeros(84,630);
Geff_pos=zeros(84,1);

basedir=getenv('MYCONNECTOME_DIR');
subcodes=textread(sprintf('%s/subcodes.txt',basedir),'sub%03d');

for session = 1:length(subcodes)
    disp(sprintf('processing session %d of %d',session,length(subcodes)))
    subcode=subcodes(session);
    rawdata=textread(sprintf('%s/combined_data_scrubbed/sub%03d.txt',basedir,subcode));
    data=corrcoef(rawdata);
    [Ci,Q(session)]=modularity_louvain_und_sign(data);
    Ppos(session,:)= participation_coef_sign(data,Ci);
    datapos=data;
    datapos(find(data<0))=0;
    Geff_pos(session)=efficiency_wei(datapos);
end

Ppos=transpose(Ppos);

save(sprintf('%s/rsfmri/geff_pos.txt',basedir),'Geff_pos','-ascii','-tabs')
save(sprintf('%s/rsfmri/modularity_weighted_louvain_bct.txt',basedir), 'Q', '-ascii', '-tabs')
save(sprintf('%s/rsfmri/PIpos_weighted_louvain_bct.txt',basedir),'Ppos', '-ascii' ,'-tabs')
