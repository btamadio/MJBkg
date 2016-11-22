#!/usr/bin/env python
import argparse,ROOT,os,math,glob
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inDir')
args = parser.parse_args()
inFileList = [ROOT.TFile.Open(fileName) for fileName in glob.glob(args.inDir+'/*')]

etaList = ['cen','for']
regionList = ['4jVRbM','4jVRbU']

def mean(lst):
    return sum(lst) / float(len(lst))
kinProf = []
dressProf = []
dressAvg = []

hKin = {}
kinProf = {}
dressProf = {}
kinErr = {}
dressAvg = {}
for eta in etaList:
    for region in regionList:
        key = eta+'_'+region
        hKin[key] = inFileList[0].Get('h_prof1d_'+eta+'_kin_'+region).ProjectionX()
        kinProf[key] = []
        dressProf[key] = []
        kinErr[key]=[]
        for bin in range(1,hKin[key].GetNbinsX()+1):
            kinProf[key].append(hKin[key].GetBinContent(bin))
            kinErr[key].append(hKin[key].GetBinError(bin))
            dressProf[key].append([])
i=0
for inFile in inFileList:
    for eta in etaList:
        for region in regionList:
            key = eta+'_'+region
            hDress = inFile.Get('h_prof1d_'+eta+'_dress_'+region).ProjectionX('prof_'+str(i))
            for bin in range(1,hDress.GetNbinsX()+1):
                dressProf[key][bin-1].append(hDress.GetBinContent(bin))
            i+=1

for eta in etaList:
    for region in regionList:
        print eta,region
        key = eta+'_'+region
        dressAvg[key] = []
        uncert = 0.0
        for i in range(len(dressProf[key])):
            dressAvg[key].append(mean(dressProf[key][i]))
            corr = (kinProf[key][i]-dressAvg[key][i])/dressAvg[key][i]
            err = kinErr[key][i]/dressAvg[key][i]
            if abs(corr) < err:
                if abs(corr) > uncert:
                    uncert = abs(corr)
                corr = 0.0
            print corr
        print 'uncert = ',uncert
