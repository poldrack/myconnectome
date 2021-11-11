# Function for recording analysis time starts, stops, and writing to file
# Will be output to text file for use to give user of future VMs an idea of how
# long it takes.

from __future__ import absolute_import
from __future__ import print_function
import time

def init_timefile(filepath):
    timefile = open(filepath,"wb")
    timefile.writelines("OUTNAME\tSTART\tSTOP\tELAPSED\n")
    timefile.close()

def get_time():
    return time.time()

def log_time(timefile,start,finish,identifier,echo=False):
    elapsed = finish- start
    timefile = open(timefile,"ab")
    timefile.writelines("%s\t%s\t%s\t%s\n" %(identifier,start,finish,elapsed))
    timefile.close()
    if echo:
        print("%s: ELAPSED:%.2f" %(identifier,elapsed))
