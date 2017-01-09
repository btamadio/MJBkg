#!/usr/bin/env python
import os
nToys = 100

dsids = range(403605,403615)
#kinFile = '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root '
kinFile = '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root '
templateType = '0'
signalLumi = 14.8
counter = 0
for dsid in dsids:
    for j in range(nToys):
        counter+=1
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '
        cmd += '../output_templates/SignalInjection_dataICHEP_'+str(dsid)+'.root '
        cmd += 'SignalInjection_dataICHEP_'+str(dsid)+' '
        cmd += '0 '
        cmd += str(j)+' '
        cmd += str(dsid)+' '
        cmd += '14.8'
        os.system(cmd)
print 'Submitted %i jobs.' % counter
