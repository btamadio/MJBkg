#!/usr/bin/env python
import argparse,ROOT,os,math,glob
parser = argparse.ArgumentParser(add_help=False, description='make plots')
parser.add_argument('inDir')
args = parser.parse_args()
region = '4jVRb0'
inFileList = [ROOT.TFile.Open(fileName) for fileName in glob.glob(args.inDir+'/*')]
def mean(lst):
    return sum(lst) / float(len(lst))
kinProf = []
dressProf = []
dressAvg = []
hKin = inFileList[0].Get('h_prof1d_kin_'+region).ProjectionX()
for bin in range(1,hKin.GetNbinsX()+1):
    kinProf.append(hKin.GetBinContent(bin))
    dressProf.append([])
for inFile in inFileList:
    hDress = inFile.Get('h_prof1d_dressNom_'+region).ProjectionX()
    for bin in range(1,hDress.GetNbinsX()+1):
        dressProf[bin-1].append(hDress.GetBinContent(bin))
for i in range(len(dressProf)):
    dressAvg.append(mean(dressProf[i]))
    print (dressAvg[i]-kinProf[i])/kinProf[i]
