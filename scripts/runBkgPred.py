#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor
jobNameList = ['pythia_eta',
#               'pythia_bdt',
               'pythia_ichep',
#               'pythia_qg',
               'pythia_nsubjet']
filesList = [glob.glob('../output_dressed/pythia_eta/*.root'),
#             glob.glob('../output_dressed/pythia_bdt/*.root'),
             glob.glob('../output_dressed/pythia_ichep/*.root'),
#             glob.glob('../output_dressed/pythia_qg/*.root'),
             glob.glob('../output_dressed/pythia_nsubjet/*.root')]
for i in range(len(jobNameList)):
    p = bkgPredictor(filesList[i],jobNameList[i],35,i)
    p.getResponse()
    p.loopAndFill()

# jobNameList = ['data_eta_corr','data_bdt_corr','data_ichep_corr']
# filesList = [glob.glob('../output_dressed/data_eta_corr/*.root'),
#              glob.glob('../output_dressed/data_bdt_corr/*.root'),
#              glob.glob('../output_dressed/data_ichep_corr/*.root')]
# for i in range(len(jobNameList)):
#     p = bkgPredictor(filesList[i],jobNameList[i],1,i)
#     p.getResponse()
#     p.loopAndFill()

# jobNameList = ['pythia_eta_corr','pythia_bdt_corr','pythia_ichep_corr']
# filesList = [glob.glob('../output_dressed/pythia_eta_corr/*.root'),
#              glob.glob('../output_dressed/pythia_bdt_corr/*.root'),
#              glob.glob('../output_dressed/pythia_ichep_corr/*.root')]
# for i in range(len(jobNameList)):
#     p = bkgPredictor(filesList[i],jobNameList[i],35,i)
#     p.getResponse()
#     p.loopAndFill()

