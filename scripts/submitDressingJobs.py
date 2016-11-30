#!/usr/bin/env python
import os
nToys = 100

#kinFile = '../../bkgEstimation/samples/data2016_PostICHEP/main_data2016_PostICHEP.root'
#templateFiles = ['../output_templates/data_PostICHEP.root']
#jobNames = ['data_PostICHEP']

kinFile = '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root'
templateFiles = ['../output_templates/SignalInjection_403566.root']
jobNames = ['SignalInjection_ICHEP_403566']

signalNum = 403566
signalLumi = 14.8
templateTypes = ['0']

counter = 0
for i in range(len(templateFiles)):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)+' '+str(signalNum)+' '+str(signalLumi)
        os.system(cmd)
        print cmd
        counter+=1
print 'Submitted %i jobs.' % counter
