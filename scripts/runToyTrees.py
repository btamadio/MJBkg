#!/usr/bin/env python
import os
for i in range(0,100):
    cmd = './makeToyTree.py ../output_resampling/data_ICHEP.root data_ICHEP '+str(i)
    os.system(cmd)
    print 'Processing toy number %i ' % i
