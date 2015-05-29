"""
utility function to load parcel data
"""


import numpy

def load_parcel_data(infile):
    f=open(infile)
    lines=f.readlines()
    f.close()
    
    # 'na' is subcortical
    network_keys={'Somatomotor': 10,
     'Frontal-Parietal-Other': 11,
     'Parietal-Episodic-Retrieval': 12,
     'Parieto-Occipital': 13,
     'Default': 1,
     'Second-Visual': 2,
     'Frontal-Parietal': 3,
     'First-Visual-V1+': 4,
     'First-Dorsal-Attention': 5,
     'Second-Dorsal-Attention': 6,
     'Ventral-Attention-Language': 7,
     'Salience': 8,
     'Cingulo-opercular': 9,
     'none':0,
     'na':14}

    fields=['parcelnum','hemis','x','y','z','lobe','region','powernetwork','yeo7network','yeo17network']
    parcelinfo_list=[]
    parcelinfo_dict={}
    for l in lines:
        l_s=l.strip().split('\t')
        parcelinfo_list.append(l_s)
        parcelnum=int(l_s[0])
        parcelinfo_dict[parcelnum]={}
        parcelinfo_dict[parcelnum]['powernum']=network_keys[l_s[7]]
        for i in range(1,len(fields)):
            try:
                parcelinfo_dict[parcelnum][fields[i]]=float(l_s[i])
            except:
                parcelinfo_dict[parcelnum][fields[i]]=l_s[i]
        
    return parcelinfo_dict