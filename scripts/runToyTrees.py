#!/usr/bin/env python
import os
for i in range(0,100):
    cmd = 'qsub run_toy_job.sh ../output_resampling/data_ICHEP.root data_ICHEP '+str(i)
    os.system(cmd)
#    print cmd
