#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

#jobNameList = ['data_PostICHEP_uncorrected']
#filesList = [sorted(glob.glob('../output_dressed/data_PostICHEP_uncorrected/*.root'))]

jobNameList = ['SignalInjection_dataICHEP_403566_corrected']
filesList = [sorted(glob.glob('../output_dressed/SignalInjection_dataICHEP_403566_corrected/*.root'))]
templateFileName = '../output_templates/SignalInjection_dataICHEP_403566.root'
#jobNameList = ['data_ICHEP_uncorrected']
#filesList = [sorted(glob.glob('../output_dressed/data_ICHEP_uncorrected/*.root'))]

#jobNameList = ['data_ICHEP_correct_all']
#filesList = [sorted(glob.glob('../output_dressed/data_ICHEP_correct_all/*.root'))]
#templateFileName = '../output_templates/data_ICHEP.root'
mjcut = 0.6



for i in range(len(jobNameList)):
    lumi = 35
    if 'data' in jobNameList[i]:
        lumi = 1
    p = bkgPredictor(filesList[i],jobNameList[i],templateFileName,mjcut,lumi,i)
    p.getResponse()
    p.loopAndFill()
