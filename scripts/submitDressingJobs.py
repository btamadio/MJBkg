#!/usr/bin/env python
import os
nToys = 100
# kinFileList = ['../../bkgEstimation/samples/data_ICHEP/main_data_ICHEP.root',
#                '../../bkgEstimation/samples/pythia_qgMatch/main_pythia_qgMatch.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
#                '../../bkgEstimation/samples/data2016_PostICHEP/main_data2016_PostICHEP.root']
# templateFileList = ['../output_templates/data_ICHEP.root',
#                     '../output_templates/pythia.root',
#                     '../output_templates/SignalInjection_dataICHEP_403566.root',
#                     '../output_templates/data_PostICHEP.root']
# jobNameList = ['data_ICHEP','pythia','SignalInjection_dataICHEP_403566','data_PostICHEP']
# templateTypeList = ['0','0','0','0']
# signalNumList = [0,0,403566,0]
# signalLumiList = [0,0,14.8,0]

# kinFileList = ['../../bkgEstimation/samples/data_ICHEP/main_data_ICHEP.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root']
# templateFileList = ['../output_templates/data_ICHEP_nsubjet.root',
#                     '../output_templates/SignalInjection_dataICHEP_403566_nsubjet.root']
# jobNameList = ['data_ICHEP_nsubjet',
#                'SignalInjection_dataICHEP_403566_nsubjet']
# templateTypeList = ['4','4']
# signalNumList = [0,403566]
# signalLumiList = [0,14.8]

kinFileList = ['../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
               '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
               '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
               '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
               '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
               '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
               '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root']
templateFileList = ['../output_templates/SignalInjection_dataICHEP_403555.root',
                    '../output_templates/SignalInjection_dataICHEP_403560.root',
                    '../output_templates/SignalInjection_dataICHEP_403571.root',
                    '../output_templates/SignalInjection_dataICHEP_403605.root',
                    '../output_templates/SignalInjection_dataICHEP_403607.root',
                    '../output_templates/SignalInjection_dataICHEP_403609.root',
                    '../output_templates/SignalInjection_dataICHEP_403611.root']
jobNameList = ['SignalInjection_dataICHEP_403555',
               'SignalInjection_dataICHEP_403560',
               'SignalInjection_dataICHEP_403571',
               'SignalInjection_dataICHEP_403605',
               'SignalInjection_dataICHEP_403607',
               'SignalInjection_dataICHEP_403609',
               'SignalInjection_dataICHEP_403611']
templateTypeList = ['0','0','0','0','0','0','0']
signalNumList = [403555,403560,403571,403605,403607,403609,403611]
signalLumiList = [14.8]*7

counter = 0
for i in range(len(templateFileList)):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+ kinFileList[i] + ' ' + templateFileList[i] + ' ' +jobNameList[i]+' '+templateTypeList[i]+' '+str(j)+' '+str(signalNumList[i])+' '+str(signalLumiList[i])
        os.system(cmd)
        counter+=1
print 'Submitted %i jobs.' % counter
