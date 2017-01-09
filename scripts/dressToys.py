#!/usr/bin/env python
import argparse,os,ROOT,glob
from templateMaker import templateMaker
parser = argparse.ArgumentParser(add_help=False, description='dress toys and get Npred histogram')
parser.add_argument('inDir')
parser.add_argument('templateFile')
parser.add_argument('jobName')
args = parser.parse_args()

inFileList = glob.glob(args.inDir+'/*.root')
templateFile = ROOT.TFile.Open(args.templateFile)
rndm = ROOT.TRandom3(0)
outFile = '../output_resampling/npred_'+args.jobName+'.root'
dummyFile = '../../bkgEstimation/samples/data_ICHEP/main_data_ICHEP.root'
tempMaker = templateMaker(dummyFile,args.jobName,0,0,0,0,1)

for fileName in inFileList:
    npred = 0
    f = ROOT.TFile.Open(fileName)
    t = f.Get('toyTree')
    nEntries = t.GetEntries()
    
