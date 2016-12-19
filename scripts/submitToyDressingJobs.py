#!/usr/bin/env python
import os,sys
from glob import glob
kinFileList = sorted(glob('../output_resampling/data_ICHEP/*.root'))
templateFile = '../output_templates/data_ICHEP.root'
jobName = 'data_ICHEP_resamp'
counter = 0
for i in range(len(kinFileList)):
    cmd = 'qsub run_dressing_job.sh '+ kinFileList[i] + ' ' + templateFile + ' ' +jobName+'_'+str(i)+' 0 0 0 0'
#    print cmd
    os.system(cmd)
    counter+=1
print 'Submitted %i jobs.' % counter
