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

# kinFileList = ['../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root',
#                '../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root']
# templateFileList = ['../output_templates/SignalInjection_dataICHEP_403555.root',
#                     '../output_templates/SignalInjection_dataICHEP_403560.root',
#                     '../output_templates/SignalInjection_dataICHEP_403571.root',
#                     '../output_templates/SignalInjection_dataICHEP_403605.root',
#                     '../output_templates/SignalInjection_dataICHEP_403607.root',
#                     '../output_templates/SignalInjection_dataICHEP_403609.root',
#                     '../output_templates/SignalInjection_dataICHEP_403611.root']
# jobNameList = ['SignalInjection_dataICHEP_403555',
#                'SignalInjection_dataICHEP_403560',
#                'SignalInjection_dataICHEP_403571',
#                'SignalInjection_dataICHEP_403605',
#                'SignalInjection_dataICHEP_403607',
#                'SignalInjection_dataICHEP_403609',
#                'SignalInjection_dataICHEP_403611']
# templateTypeList = ['0','0','0','0','0','0','0']
# signalNumList = [403555,403560,403571,403605,403607,403609,403611]
# signalLumiList = [14.8]*7

# kinFileList = ['../../bkgEstimation/samples/data_ICHEP/main_data_ICHEP.root']
# templateFileList = ['../output_templates/data_ICHEP.root']
# jobNameList = ['data_ICHEP']
# templateTypeList = ['0']
# signalNumList = [0]
# signalLumiList = [0]

# kinFileList = ['../../bkgEstimation/samples/combinedMC/main_combinedMC.root']
# templateFileList = ['../output_templates/combinedMC.root']
# jobNameList = ['combined_pythia_herwig']
# templateTypeList = ['0']
# signalNumList = [0]
# signalLumiList = [0]

#kinFileList = ['../../bkgEstimation/samples/data_30fb/main_data_30fb.root']
#templateFileList = ['../output_templates/data_30fb.root']
#jobNameList = ['data_30fb']
#templateTypeList = ['0']
#signalNumList = [0]
#signalLumiList = [0]

# kinFileList = ['../../bkgEstimation/samples/pythia_qgMatch/main_pythia_qgMatch.root']
# templateFileList = ['../output_templates/pythia.root']
# jobNameList = ['pythia_withUncert']
# templateTypeList = ['0']
# signalNumList = [0]
# signalLumiList = [0]

# kinFileList = ['../../bkgEstimation/samples/pythia_scaleHalf/main_pythia_scaleHalf.root',
#                '../../bkgEstimation/samples/herwig_scaleHalf/main_herwig_scaleHalf.root']
# templateFileList = ['../output_templates/combinedMC.root',
#                     '../output_templates/combinedMC.root']
# jobNameList = ['pythia_scaleHalf',
#                'herwig_scaleHalf']
# templateTypeList = ['0','0']
# signalNumList = [0,0]
# signalLumiList = [0,0]

# kinFileList = ['../../bkgEstimation/samples/data_30fb/main_data_30fb.root']
# templateFileList = ['../output_templates/data_30fb.root']
# jobNameList = ['data_30fb_withUncert']
# templateTypeList = ['0']
# signalNumList = [0]
# signalLumiList = [0]

#kinFileList = ['../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root']
#templateFileList = ['../output_templates/SignalInjection_dataICHEP_403587.root']
#jobNameList = ['SignalInjection_dataICHEP_403587_withUncert']
#templateTypeList = ['0']
#signalNumList = [403587]
#signalLumiList=[14.8]

kinFileList = ['../../bkgEstimation/samples/SignalInjection_RPV10/main_SignalInjection_RPV10.root']*9
templateFileList = ['../output_templates/SignalInjection_dataICHEP_403553.root',
                    '../output_templates/SignalInjection_dataICHEP_403555.root',
                    '../output_templates/SignalInjection_dataICHEP_403557.root',
                    '../output_templates/SignalInjection_dataICHEP_403564.root',
                    '../output_templates/SignalInjection_dataICHEP_403567.root',
                    '../output_templates/SignalInjection_dataICHEP_403570.root',
                    '../output_templates/SignalInjection_dataICHEP_403587.root',
                    '../output_templates/SignalInjection_dataICHEP_403591.root',
                    '../output_templates/SignalInjection_dataICHEP_403595.root']
jobNameList = ['SignalInjection_dataICHEP_403553_withUncert',
               'SignalInjection_dataICHEP_403555_withUncert',
               'SignalInjection_dataICHEP_403557_withUncert',
               'SignalInjection_dataICHEP_403564_withUncert',
               'SignalInjection_dataICHEP_403567_withUncert',
               'SignalInjection_dataICHEP_403570_withUncert',
               'SignalInjection_dataICHEP_403587_withUncert',
               'SignalInjection_dataICHEP_403591_withUncert',
               'SignalInjection_dataICHEP_403595_withUncert']
templateTypeList = ['0']*9
signalNumList = [403553,403555,403557,
                 403564,403567,403570,
                 403587,403591,403595]
signalLumiList=[14.8]*9

counter = 0
for i in range(len(templateFileList)):
    for j in range(nToys):
        cmd = 'qsub -l h_vmem=16G run_dressing_job.sh '+ kinFileList[i] + ' ' + templateFileList[i] + ' ' +jobNameList[i]+' '+templateTypeList[i]+' '+str(j)+' '+str(signalNumList[i])+' '+str(signalLumiList[i])
        os.system(cmd)
        counter+=1
print 'Submitted %i jobs.' % counter
