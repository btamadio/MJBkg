#!/usr/bin/env python
import os
from pointDict import pointDict
from bkgPredictor import bkgPredictor
from glob import glob
for dsid in pointDict:
    fileList = glob('../output_dressed/SignalInjection_dataICHEP_'+str(dsid)+'/*')
    if len(fileList)==0:
        continue
    fileDir = '../output_dressed/SignalInjection_dataICHEP_'+str(dsid)+'/'
    jobName = 'SignalInjection_dataICHEP_'+str(dsid)
    templateFile = '../output_templates/SignalInjection_dataICHEP_'+str(dsid)+'.root'
    mjCut = 0.6
    lumi = 1.0
    templateType = 0
    p = bkgPredictor(fileList,jobName,templateFile,mjCut,lumi,templateType)
    p.getResponse()
    p.loopAndFill()

