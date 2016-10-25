#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from bkgPredictor import bkgPredictor

name = 'data_eta'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
p0 = bkgPredictor(dressedFileNames,name,1.0,0)
p0.loopAndFill()
p0.plotResponse()

name ='data_bdt'
dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
p2 = bkgPredictor(dressedFileNames,name,1.0,1)
p2.loopAndFill()
p2.plotResponse()

#name = 'data_ichep'
#dressedFileNames = glob.glob('../output_dressed/'+name+'/*.root')
#p3 = bkgPredictor(dressedFileNames,name,1.0,2)
#p3.loopAndFill()
#p3.plotResponse()
