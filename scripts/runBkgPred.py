#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

#jobNameList = ['data_PostICHEP']
#filesList = [glob.glob('../output_dressed/data_PostICHEP/*.root')]

jobNameList = ['data_ICHEP']
filesList = [glob.glob('../output_dressed/data_ICHEP/*.root')]

for i in range(len(jobNameList)):
    lumi = 35
    if 'data' in jobNameList[i]:
        lumi = 1
    p = bkgPredictor(filesList[i],jobNameList[i],lumi,i)
    p.getResponse()
    p.loopAndFill()
