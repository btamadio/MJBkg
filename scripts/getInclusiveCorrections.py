#!/usr/bin/env python
import argparse,ROOT,os,math,glob
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inDir')
args = parser.parse_args()
inFileList = [ROOT.TFile.Open(fileName) for fileName in glob.glob(args.inDir+'/*')]

region = '4js1'
def mean(lst):
    return sum(lst) / float(len(lst))
kinProf = []
dressProf = []
dressAvg = []

dressAvg = {}

hKin = inFileList[0].Get('h_prof1d_kin_'+region).ProjectionX()
kinProf = []
dressProf = []
kinErr=[]
for bin in range(1,hKin.GetNbinsX()+1):
    kinProf.append(hKin.GetBinContent(bin))
    kinErr.append(hKin.GetBinError(bin))
    dressProf.append([])
i=0
for inFile in inFileList:
    hDress = inFile.Get('h_prof1d_dress_'+region).ProjectionX('prof_'+str(i))
    for bin in range(1,hDress.GetNbinsX()+1):
        dressProf[bin-1].append(hDress.GetBinContent(bin))
    i+=1

dressAvg = []
uncert = 0.0
for i in range(len(dressProf)):
    dressAvg.append(mean(dressProf[i]))
    corr = (kinProf[i]-dressAvg[i])/dressAvg[i]
    err = kinErr[i]/dressAvg[i]
    print corr
    #print i,corr,corr/err
    #if abs(corr) < err:
    #    if abs(corr) > uncert:
    #        uncert = abs(corr)
    #        corr = 0.0
    #print corr
    #print 'uncert = ',uncert
