#!/usr/bin/env python
import os
nToys = 100
#kinFile = '../../bkgEstimation/samples/data2016_PostICHEP/main_data2016_PostICHEP.root'
#templateFiles = ['../output_templates/data_PostICHEP.root']
#jobNames = ['data_PostICHEP']

kinFile = '../../bkgEstimation/samples/pythia_qgMatch/main_pythia_qgMatch.root'
templateFiles = ['../output_templates/pythia_eta.root']
jobNames = ['pythia_uncorrected']

templateTypes = ['0']

counter = 0
for i in range(len(templateFiles)):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)
        os.system(cmd)
        counter+=1
print 'Submitted %i jobs.' % counter
