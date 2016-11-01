#!/usr/bin/env python
import os
nToys = 100
kinFile = '../../bkgEstimation/samples/pythia_qgMatch/main_pythia_qgMatch.root'
templateFiles = ['../output_templates/pythia_qg.root','../output_templates/pythia_nsubjet.root']
jobNames = ['pythia_qg','pythia_nsubjet']
templateTypes = ['3','4']
counter = 0
for i in range(2):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)
        os.system(cmd)
        counter+=1
print 'Submitted %i jobs.' % counter
#data
kinFile = '../../bkgEstimation/samples/DS4_BDT_PtRatios/main_DS4_BDT_PtRatios.root'
templateFiles = ['../output_templates/data_eta.root',
                '../output_templates/data_bdt.root',
                '../output_templates/data_ichep.root']
jobNames = ['data_eta_corr','data_bdt_corr','data_ichep_corr']
templateTypes = ['0','1','2']
counter = 0
#for i in range(len(templateFiles)):
for i in range(3):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)
#        os.system(cmd)
#        counter+=1

#pythia
kinFile = '../../bkgEstimation/samples/pythia_BDT_PtRatios/main_pythia_BDT_PtRatios.root'
templateFiles = ['../output_templates/pythia_eta.root',
                '../output_templates/pythia_bdt.root',
                '../output_templates/pythia_ichep.root']
jobNames = ['pythia_eta_corr','pythia_bdt_corr','pythia_ichep_corr']
templateTypes = ['0','1','2']
for i in range(3):
    for j in range(nToys):
        cmd = 'qsub run_dressing_job.sh '+kinFile+' '+templateFiles[i]+' '+jobNames[i]+' '+templateTypes[i]+' '+str(j)
#        os.system(cmd)
#        counter+=1

