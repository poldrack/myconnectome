"""
utility function to load parcel data
"""


import numpy

def load_parcel_data(infile):
    f=open(infile)
    lines=f.readlines()
    f.close()
    
#    1             DMN
# 2             Visual 2
# 3             Fronto-parietal 1
# 4.5          Visual 1
# 5             Dorsal Attention
# 7             Ventral Attention
# 8             Salience
# 9             Cingulo-opercular
# 10        ​   Somato-motor
# 11.5        Fronto-parietal 2
# 15           Medial Parietal
# 16           Parieto-occipital

    # 'na' is subcortical
    network_keys={'Somatomotor': 9,
     'Frontoparietal 2': 10,
     'Medial_Parietal': 11,
     'Parieto_occipital': 12,
     'DMN': 1,
     'Visual_2': 2,
     'Frontoparietal_1': 3,
     'Visual_1': 4,
     'Dorsal_Attention': 5,
     'Ventral_Attention': 6,
     'Salience': 7,
     'Cingulo_opercular': 8,
     'Zero':0,
     'na':13}

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