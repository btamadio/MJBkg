#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

jobNameList = ['data_ICHEP_uncorrected']
filesList = [sorted(glob.glob('../output_dressed/data_ICHEP_uncorrected/*.root'))]

mjcut = 0.6
for i in range(len(jobNameList)):
    lumi = 35
    if 'data' in jobNameList[i]:
        lumi = 1
    p = bkgPredictor(filesList[i],jobNameList[i],mjcut,lumi,i)
    p.getResponse()
    p.loopAndFill()
