#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

date ='10_19'
name ='pythia_bdt'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
os.system('mkdir -p ../output_prediction/')
p = bkgPredictor(dressedFileNames,name)

#p.histDict['n4jVR_b0'].Draw('h')
#p.histDict['n4jVR_b0'].SetMarkerSize(0)
#p.histDict['n4jVR_b0'].SetFillColor(ROOT.kRed)
#p.histDict['n4jVR_b0'].SetFillStyle(3001)
#p.histDict['n4jVR_b0'].Draw('e2')
#p.obsDict['n4jVR_b0'].Draw('p same')
