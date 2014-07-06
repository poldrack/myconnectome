#!/usr/bin/env python
"""
make config files to visualize data from selftracking
parcellations (from Wash U)  using Circos

based on tutorial from van horn group - http://circos.ca/documentation/tutorials/recipes/cortical_maps/

use mean connectivity for outer ring and power modules for inner ring
"""


import os,sys
import numpy
import scipy.stats
import igraph

edge_density=0.01
datatype='positive_neg' # 'corr'
model='adj' #'meancorr' # 'var','threshcorr'
adjsize=634
utr=numpy.triu_indices(adjsize,1)
binarize_adj=False
include_labels=False
include_pos=True
include_neg=False
if include_pos and include_neg:
	edge_density = edge_density / 2.0

labelfile='/Users/poldrack/code/selftracking/rsfmri/parcel_data.txt'
assert os.path.exists(labelfile)

if datatype=='pcorr':
	print 'using partial correlation'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/huge_adj.npy'
	data=numpy.load(datafile)
	data=data[:,4,:]
elif datatype=='tu_th':
	print 'using tu_th_fdrcorr'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/tth_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='tu_th_pos':
	print 'using tu_th_fdrcorr_pos'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/tth_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='tu_th_neg':
	print 'using tu_th_fdrcorr_neg'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/tth_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)*-1.0
elif datatype=='fatigue_pos':
	print 'using fatigue_fdrcorr_pos'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/fatigue_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='fatigue_neg':
	print 'using fatigue_fdrcorr_neg'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/fatigue_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)*-1
elif datatype=='positive_pos':
	print 'using positive_fdrcorr_pos'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/postive_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='positive_neg':
	print 'using positive_fdrcorr_neg'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/postive_all_fdr_t.txt'
	data=numpy.loadtxt(datafile)*-1
elif datatype=='negative_pos':
	print 'using negative_fdrcorr_pos'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/negative_panas_fdr_pos_t.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='negative_neg':
	print 'using negative_fdrcorr_neg'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/negative_panas_fdrneg_t.txt'
	data=numpy.loadtxt(datafile)*-1
elif datatype=='withinvar':
	print 'using within-sess variance'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/windowed_corr_var/mean_windowed_var_overlap4_64windows.txt'
	data=numpy.loadtxt(datafile)
elif datatype=='dti':
	print 'using dti'
	datafile='/Users/poldrack/Dropbox/data/selftracking/DTI/tracksumm_distcorr.txt'
	d=numpy.loadtxt(datafile)
	#import scipy.special
	data=.5*(d + d.T)[utr]
else:
	print 'using correlation'
	datafile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/corrdata.npy'
	data=numpy.load(datafile)



if model=='threshcorr': # thresh corr
    threshdata=numpy.zeros(data.shape)
    for i in range(data.shape[0]):
        thresh=scipy.stats.scoreatpercentile(data[i,:],100.0 - 100.0*edge_density)
        threshdata[i,:]=data[i,:]>thresh
    triudata=numpy.sum(threshdata,0)/float(data.shape[0])

elif model=='meancorr':
	triudata=numpy.mean(data,0)	
elif model=='var':
    triudata=numpy.var(data,0)
elif model=='adj':
	triudata=data
else:
    print 'bad model'
    sys.exit()


meanthresh_pos=scipy.stats.scoreatpercentile(triudata,100.0 - 100.0*edge_density)
meanthresh_neg=scipy.stats.scoreatpercentile(triudata,100.0*edge_density)
mean_cc=numpy.zeros((adjsize,adjsize))
if include_pos:
	mean_cc[utr]+=triudata>meanthresh_pos
if include_neg:
	mean_cc[utr]+=triudata<meanthresh_neg

mean_corrdata=numpy.zeros((adjsize,adjsize))
mean_corrdata[utr]=triudata
full_corrdata=mean_corrdata + mean_corrdata.T
mean_parcel_corr=numpy.mean(full_corrdata,0)

if binarize_adj:
	mean_corrdata=(mean_corrdata!=0).astype('float32')
	
print 'thresholds=',meanthresh_pos,meanthresh_neg
print 'density = ',numpy.sum(mean_cc>0)/float(len(utr[0]))



output_dir='selftracking_%s_%.03f_%s'%(model,edge_density,datatype)
if include_pos:
	output_dir=output_dir+'_pos'
if include_neg:
	output_dir=output_dir+'_neg'

#print triudata.shape

print 'using output directory:',output_dir

print 'using edge density of',edge_density


if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(os.path.join(output_dir,'etc')):
    os.mkdir(os.path.join(output_dir,'etc'))
if not os.path.exists(os.path.join(output_dir,'data')):
    os.mkdir(os.path.join(output_dir,'data'))
    
# get labels

f=open(labelfile)
lines=f.readlines()
f.close()

xloc=[]
yloc=[]
zloc=[]
lobe=[]
label=[]
hemis=[]
rsn_power=[]
rsn_yeo7=[]
rsn_yeo17=[]

power_network_parcellation=numpy.loadtxt('/Users/poldrack/Dropbox/data/selftracking/parcellation/power_network_assignments_parcellation.txt')

ctr=0
for l in lines:
    l_s=l.strip().split()
    #print l_s
    hemis.append(l_s[1])
    xloc.append(int(numpy.round(float(l_s[2]))))
    yloc.append(int(numpy.round(float(l_s[3]))))
    zloc.append(int(numpy.round(float(l_s[4]))))
    lobe.append(l_s[5])
    label.append(l_s[6])
    if ctr<620:
    	rsn_power.append(power_network_parcellation[ctr])
    else:
    	rsn_power.append(0)
    #rsn_power.append(l_s[7])
    rsn_yeo7.append(l_s[8])
    rsn_yeo17.append(l_s[9])
    ctr+=1

modules=rsn_power

power_network_names={-1:'none',0:'none',1:'Default',2:'Second-Visual',3:'Frontal-Parietal',4.5:'First-Visual-V1+',5:'First-Dorsal-Attention',6:'Second-Dorsal-Attention',7:'Ventral-Attention-Language',8:'Salience',9:'Cingulo-opercular',10:'Somatomotor',11.5:'Frontal-Parietal-Other',15:'Parietal-Episodic-Retrieval',16:'Parieto-Occipital',17:'na'}
# power_network_reverse={}
# for k in power_network_names.iterkeys():
# 	try:
# 		power_network_reverse[power_network_names[k]]=k
# 	except:
# 		power_network_reverse[power_network_names[int(k)]]=int(k)


#modules=[]
# for l in rsn_power:
# 	try:
# 		modules.append(power_network_reverse[l])
# 	except:
# 		modules.append(power_network_reverse[int(l)])

lobes=['Frontal','Temporal','Insula','None','Parietal','Occipital']

unique_labels=list(set(label))

label_counter={'L':{},'R':{},'M':{}}

for i in range(len(label)):
    label_counter[hemis[i]][label[i]]=0
    
# need to give unique names to each ROI
labels_fixed=[]

for i in range(len(label)):
    labels_fixed.append('%s_%d'%(label[i],label_counter[hemis[i]][label[i]]+1))
    label_counter[hemis[i]][label[i]]+=1

# make data/structure.labels.txt
# e.g.
# fro-l 0 99 TrFPoG/S
# fro-l 100 199 FMarG/S

# first make all the labels, then order them
lobehemi=[]
for i in range(len(label)):
    lobehemi.append('%s-%s'%(hemis[i],lobe[i]))

lobehemi_unique=list(set(lobehemi))
lobehemi_y={}
for l in lobehemi_unique:
    lobehemi_y[l]=[]
for l in range(len(lobehemi)):
    offset=0
    if hemis[l]=='R':
        lobehemi_y[lobehemi[l]].append(-1.0*yloc[l]-1000)
    elif hemis[l]=='M':
        lobehemi_y[lobehemi[l]].append(yloc[l]-500)
    else:
        lobehemi_y[lobehemi[l]].append(yloc[l])
mean_ylocs={}
for l in lobehemi_unique:
    mean_ylocs[l]=numpy.mean(lobehemi_y[l])

lobehemi_tmp=mean_ylocs.keys()
lobehemi_locs=[mean_ylocs[i] for i in lobehemi_tmp]
lobehemi_ordered=[lobehemi_tmp[i] for i in numpy.argsort(lobehemi_locs)]


f_order=open(os.path.join(output_dir,'etc/segment.order.conf'),'w')
cmd='chromosomes_order = '
for l in lobehemi_ordered:
    cmd+='%s,'%l
cmd=cmd[:-1]
#print cmd
f_order.write(cmd+'\n')
f_order.close()
    


# now find all the locations for each lobehemi
lobehemi_regions={}
lobehemi_ylocs={}

for lh in lobehemi_ordered:
    lobehemi_regions[lh]=[]
    lobehemi_ylocs[lh]=[]

for i in range(len(label)):
    lobehemi_regions[lobehemi[i]].append(labels_fixed[i])
    lobehemi_ylocs[lobehemi[i]].append(yloc[i])

f_label=open(os.path.join(output_dir,'data/structure.label.txt'),'w')
f_seg=open(os.path.join(output_dir,'data/segments.txt'),'w')
f_module=open(os.path.join(output_dir,'data/measure.0.txt'),'w')

region_startvals_dict={}
region_zval_dict={}
region_module_dict={}

if len(mean_parcel_corr[mean_parcel_corr<0])>0:
	mean_parcel_corr[mean_parcel_corr<0]=(mean_parcel_corr[mean_parcel_corr<0] 
		- numpy.max(mean_parcel_corr[mean_parcel_corr<0]))/numpy.abs(numpy.min(mean_parcel_corr[mean_parcel_corr<0]) 
		- numpy.max(mean_parcel_corr[mean_parcel_corr<0]))

if len(mean_parcel_corr[mean_parcel_corr>0])>0:
	mean_parcel_corr[mean_parcel_corr>0]=(mean_parcel_corr[mean_parcel_corr>0] 
		- numpy.min(mean_parcel_corr[mean_parcel_corr>0]))/numpy.abs(numpy.min(mean_parcel_corr[mean_parcel_corr>0]) 
		- numpy.max(mean_parcel_corr[mean_parcel_corr>0]))

for i in range(len(lobehemi)):
    region_zval_dict[lobehemi[i]+'_'+labels_fixed[i]]=mean_parcel_corr[i]*128.0  # zloc[i]
    region_module_dict[lobehemi[i]+'_'+labels_fixed[i]]=modules[i]

for l in lobehemi_ordered:
    blklen=100*len(lobehemi_regions[l]) - 1
    f_seg.write('chr - %s %s 0 %d black\n'%(l,l.split('-')[1],blklen))
    if l[0]=='R':
        yorder=numpy.argsort(lobehemi_ylocs[l])[::-1]
    else:
        #reverse direction for left hemisphere
        yorder=numpy.argsort(lobehemi_ylocs[l])
    ordered_regions=[lobehemi_regions[l][i] for i in yorder]
    startval=0
    for r in ordered_regions:
        f_label.write('%s %d %d %s\n'%(l,startval,startval+99,r))
        f_module.write('%s %d %d %s\n'%(l,startval,startval+99,region_module_dict[l+'_'+r]))
        region_startvals_dict[l+'_'+r]=startval
        colornum=numpy.floor(region_zval_dict[l+'_'+r])
        if colornum==0:
            colornum+=1
        #colorname='z%d'%region_zval_dict[l+'_'+r]
        f_seg.write('band %s %s %s %d %d %d\n'%(l,r,r,startval,startval+99,colornum))
        startval+=100

f_label.close()
f_seg.close()
f_module.close()


region_startvals=[]
for i in range(len(labels_fixed)):
    region_startvals.append(region_startvals_dict[lobehemi[i]+'_'+labels_fixed[i]])
    
# create links file

adjmtx=mean_corrdata/numpy.max(numpy.abs(mean_corrdata))*mean_cc

f_link=open(os.path.join(output_dir,'data/links.txt'),'w')
for i in range(adjsize):
    for j in range(i,adjsize):
        if adjmtx[i,j]!=0:
            if adjmtx[i,j]>0:
                corrtype=1
            else:
                corrtype=2
            f_link.write('%s %d %d %s %d %d type=%d,score=%f\n'%(lobehemi[i],region_startvals[i],region_startvals[i]+99,
                lobehemi[j],region_startvals[j],region_startvals[j]+99,corrtype,numpy.abs(adjmtx[i,j])))
f_link.close()



# write ideogram file
f=open(os.path.join(output_dir,'etc/ideogram.conf'),'w')
cmd='''

<ideogram>

<spacing>
default = 0.005r
<pairwise %s %s>
spacing = 5r
</pairwise>
</spacing>

<<include ideogram.position.conf>>
<<include ideogram.label.conf>>
<<include bands.conf>>

</ideogram>

'''%(lobehemi_ordered[0],lobehemi_ordered[-1])
f.write(cmd)
f.close()

# make colors file
f_colors=open(os.path.join(output_dir,'etc/color.brain.conf'),'w')
# 
# use mean connectivity for color scale
# for l in list(set(region_zval_dict.values())):
#     c=(l-numpy.min(mean_parcel_corr)+1) * 2.1
#     f_colors.write('z%s = %d,0,0\n'%(l,c))
#f_colors.write('0=0,0,0\n')
f_colors.write('0=black\n')
f_colors.write('-1=black\n')


for i in range(1,129):
	if i<65:
		f_colors.write('%d=%d,%d,%d\n'%(i,i*2-1,0,0))
	else:
		f_colors.write('%d=%d,%d,%d\n'%(i,i*2-1,i+(i-64)*2.0 - 1,0))
for i in range(2,129):
		f_colors.write('-%d=%d,%d,%d\n'%(i,i,i,i*2-1)) #i*2-1))
#	else:
#		f_colors.write('-%d=%d,%d,%d\n'%(i,i+(i-64)*2.0 - 1,i+(i-64)*2.0 - 1,i*2-1))

f_colors.close()


# these files do not require any changes for now:


# etc/bands.conf
f=open(os.path.join(output_dir,'etc/bands.conf'),'w')
f.write("""show_bands            = yes
fill_bands            = yes
band_stroke_thickness = 1
band_stroke_color     = black
band_transparency     = 0
""")
f.close()

# etc/ideogram.label.conf
f=open(os.path.join(output_dir,'etc/ideogram.label.conf'),'w')

if include_labels:
	label_radius=' + 250p'
else:
	label_radius=' + 0.05r'
f.write('label_radius     = dims(ideogram,radius_outer)%s\n'%label_radius)

f.write("""
show_label       = yes
label_font       = default
label_size       = 36
label_parallel   = yes
label_case       = upper
# you can format the label by using properties
# of the ideogram, accessible with var(PROPERTY):
#
# chr, chr_with_tag, chrlength, display_idx, end, idx, 
# label, length, reverse, scale, size, start, tag

#label_format     = eval(sprintf("region %s",var(label)))

""")
f.close()


# etc/ideogram.position.conf
f=open(os.path.join(output_dir,'etc/ideogram.position.conf'),'w')
f.write('''radius           = 0.85r
thickness        = 75p
fill             = no
stroke_thickness = 1
stroke_color     = black
''')
f.close()

# etc/ticks.conf

# come back to these later
f=open(os.path.join(output_dir,'etc/ticks.conf'),'w')

f.write('''
show_ticks          = yes
show_tick_labels    = yes
show_grid           = yes

<ticks>

radius           = dims(ideogram,radius_outer)
color            = black
thickness        = 2p
size             = 0

<tick>
spacing        = 0.5u
size           = 5p
grid           = yes
grid_color     = black
grid_thickness = 1p
grid_start     = 1r-conf(ideogram,thickness)
grid_end       = 0.825r
</tick>

<tick>
spacing        = 1u
</tick>

</ticks>

''')
f.close()

# etc/heatmap.conf - needed if we are going to use heatmaps
f=open(os.path.join(output_dir,'etc/heatmap.conf'),'w')
f.write('''        <plot>
init_counter = heatmap:0
post_increment_counter = heatmap:1
type         = heatmap
file         = data/measure.counter(heatmap).txt
color        = eval((split(",","conf(hm_colors)"))[counter(heatmap)])
r1           = eval(sprintf("%fr",conf(hm_r)-counter(heatmap)*(conf(hm_w)+conf(hm_pad))))
r0           = eval(sprintf("%fr",conf(hm_r)-counter(heatmap)*(conf(hm_w)+conf(hm_pad))+conf(hm_w)))

stroke_color = white
stroke_thickness = 3

</plot>
''')
f.close()

if not os.path.exists(os.path.join(output_dir,'etc/tracks')):
    os.mkdir(os.path.join(output_dir,'etc/tracks'))
f=open(os.path.join(output_dir,'etc/tracks/link.conf'),'w')

f.write('''
ribbon           = no
color            = black
thickness        = 1
radius           = 0.40r
bezier_radius    = 0r
crest                = 0.5
bezier_radius_purity = 0.75
''')
f.close()

f=open(os.path.join(output_dir,'etc/tracks/heatmap.conf'),'w')

f.write('''
color            = spectral-11-div
stroke_thickness = 1
stroke_color     = vlgrey
r1               = 0.975r
r0               = 0.95r
''')
f.close()

f=open(os.path.join(output_dir,'etc/tracks/text.conf'),'w')

f.write('''
label_font     = default
label_size     = 12
color          = black

r0             = 0.85r
r1             = 0.95r

show_links     = no
link_dims      = 2p,4p,8p,4p,2p
link_thickness = 1p
link_color     = red

padding        = 0p
rpadding       = 0p

label_snuggle             = no
max_snuggle_distance      = 1r
snuggle_sampling          = 1
snuggle_tolerance         = 0.25r

snuggle_refine                 = no
snuggle_link_overlap_test      = no
snuggle_link_overlap_tolerance = 2p
''')
f.close()


# removed: 

# 
f=open(os.path.join(output_dir,'etc/circos.conf'),'w')

f.write('''

<<include ideogram.conf>>

chromosomes_units = 100
<<include ticks.conf>>

<image>
angle_offset* = -87
<<include etc/image.conf>>
</image>

### single genomes

karyotype = data/segments.txt

<<include segment.order.conf>>

chromosomes_reverse = /.*-l/

hm_r      = 0.95
hm_w      = 0.025
hm_pad    = 0.005

hm_colors = spectral-11-div,oranges-4-seq,greens-4-seq,blues-4-seq,purples-4-seq

<plots>

<<include heatmap.conf>>
''')

if include_labels:
	f.write("""<plot>
	type       = text
	file       = data/structure.label.txt
	color      = black
	label_font = default
	label_size = 16
	r0         = 1r
	r1         = 1.5r
	rpadding   = 10p
	</plot>""")

f.write("""

<plot>
type  = heatmap
file  = data/segments.txt
r1    = 0.89r
r0    = 0.88r
</plot>
""")

f.write('''</plots>

<links>

<link>
file   = data/links.txt
radius = 0.925r # eval(sprintf("%fr",conf(hm_r)-counter(heatmap)*(conf(hm_w)+conf(hm_pad))+conf(hm_w)))

bezier_radius = 0r
bezier_radius_purity = 0.5
crest         = 0.25
thickness     = 2
color         = black

<rules>
<rule>
# this rule is part of variant #1
# to use it, set use=yes and also adjust radius above to 0.7r
use       = no
condition = var(chr1) eq var(chr2)
bezier_radius = 1r
radius    = 0.71r
flow      = continue
</rule>
<rule>
condition = 1
thickness = eval(remap_int(var(score),0,1,1,5)) 
flow      = continue
</rule>
<rule>
condition = var(type) == 0 
color     = eval(sprintf("greys-5-seq-%d",remap_int(var(score),0,1,1,5)))
</rule>
<rule>
condition = var(type) == 1
color     = eval(sprintf("reds-5-seq-%d",remap_int(var(score),0,1,1,5)))
</rule>
<rule>
condition = var(type) == 2
color     = eval(sprintf("blues-5-seq-%d",remap_int(var(score),0,1,1,5)))
</rule>
</rules>

</link>

</links>

<<include etc/colors_fonts_patterns.conf>>
<colors>
<<include color.brain.conf>>
</colors>

restrict_parameter_names* = no
<<include etc/housekeeping.conf>>

''')
f.close()
