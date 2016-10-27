#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

jobNameList = ['data_eta_uncorr','data_bdt_uncorr','data_ichep_uncorr']
filesList = [glob.glob('../output_dressed/data_eta/*.root'),
             glob.glob('../output_dressed/data_bdt/*.root'),
             glob.glob('../output_dressed/data_ichep/*.root')]
for i in range(len(jobNameList)):
    p = bkgPredictor(filesList[i],jobNameList[i],1,i)
    p.getResponse()
    p.loopAndFill()

jobNameList = ['pythia_eta_uncorr','pythia_bdt_uncorr','pythia_ichep_uncorr']
filesList = [glob.glob('../output_dressed/pythia_eta/*.root'),
             glob.glob('../output_dressed/pythia_bdt/*.root'),
             glob.glob('../output_dressed/pythia_ichep/*.root')]
for i in range(len(jobNameList)):
    p = bkgPredictor(filesList[i],jobNameList[i],35,i)
    p.getResponse()
    p.loopAndFill()
