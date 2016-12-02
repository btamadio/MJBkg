#!/usr/bin/env python
import os
nToys = 100
signalNum = 0
signalLumi =0
#kinFile = '../../bkgEstimation/samples/data2016_PostICHEP/main_data2016_PostICHEP.root'
#templateFiles = ['../output_templates/data_PostICHEP.root']
#jobNames = ['data_PostICHEP']

kinFile = '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root'
templateFiles = ['../output_templates/SignalInjection_dataICHEP_403566.root']
ljobNames = ['SignalInjection_dataICHEP_403566_corrected']
signalNum = 403566
signalLumi = 14.8

#kinFile = '../../bkgEstimation/samples/data_ICHEP/main_data_ICHEP.root'
#templateFiles = ['../output_templates/data_ICHEP.root']
#jobNames = ['data_ICHEP']

templateTypes = ['0']

counter = 0
for i in range(len(templateFiles)):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)+' '+str(signalNum)+' '+str(signalLumi)
        os.system(cmd)
        counter+=1
print 'Submitted %i jobs.' % counter
