
from __future__ import absolute_import
import numpy
from six.moves import range


def ts_shuffle(y,nblocks=4,min_block_size=5):
    # block permutation
    ntp=y.shape[0]
    if len(y.shape)==1:
        nvars=1
    else:
        nvars=y.shape[1]
    good_set=False
    while not good_set:
        idx=list(range(ntp))
        numpy.random.shuffle(idx)
        boundaries=numpy.sort(idx[:(nblocks-1)])
        boundaries=numpy.hstack((boundaries,[ntp]))
        if boundaries[0]<min_block_size:
            continue
        if numpy.min(boundaries[1:] - boundaries[:-1])<min_block_size:
            continue
        good_set=True
    boundaries=boundaries[:-1]
    indices=numpy.zeros(ntp)
    for i in range(ntp):
        try:
            indices[i]=numpy.max(numpy.where(boundaries <= i)[0])+1
        except:
            pass
    blockorder=list(range(nblocks))
    numpy.random.shuffle(blockorder)
    shuffled_data=numpy.array([])
    if nvars==1:
        for b in blockorder:
            shuffled_data=numpy.hstack((shuffled_data,y[indices==b]))
    else:
        for v in range(nvars):
            shuftmp=numpy.array([])
            for b in blockorder:
                shuftmp=numpy.hstack((shuftmp,y[indices==b,v]))
            try:
                shuffled_data=numpy.vstack((shuffled_data,shuftmp))
            except:
                shuffled_data=shuftmp
        shuffled_data=shuffled_data.T
    return shuffled_data  
