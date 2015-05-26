"""
run infomap on all sessions using compiled version
"""

import os,glob

filedir='/scratch/01329/poldrack/selftracking/graph_files'

graph_files=glob.glob(os.path.join(filedir,'*.net'))
graph_files.sort()

for f in graph_files:
    print '/corral-repl/utexas/poldracklab/software_lonestar/build/infomap/Infomap %s /scratch/01329/poldrack/selftracking/infomap_results --clu --map'%f
