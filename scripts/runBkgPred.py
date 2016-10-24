#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

name ='data_bdt'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
os.system('mkdir -p ../output_prediction/')
p = bkgPredictor(dressedFileNames,name,1.0)

name = 'data_eta'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
p2 = bkgPredictor(dressedFileNames,name,1.0)

name = 'data_ichep'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
p3 = bkgPredictor(dressedFileNames,name,1.0)

#p.histDict['n4jVR_b0'].Draw('h')
#p.histDict['n4jVR_b0'].SetMarkerSize(0)
#p.histDict['n4jVR_b0'].SetFillColor(ROOT.kRed)
#p.histDict['n4jVR_b0'].SetFillStyle(3001)
#p.histDict['n4jVR_b0'].Draw('e2')
#p.obsDict['n4jVR_b0'].Draw('p same')
