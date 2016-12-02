#!/usr/bin/env python
import argparse,ROOT,os,math,glob,pprint
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inFileName')
args = parser.parse_args()
inFile = ROOT.TFile.Open(args.inFileName)

etaList = ['eta1','eta2','eta3','eta4']
regionList = ['4js1bU','4js1bM']

hKin = {}
hDress = {}
kinProf = {}
dressProf = {}
kinErr = {}
corrections = {}
finalCorrections = {}

for eta in etaList:
    for region in regionList:
        key = eta+'_'+region
        hKin[key] = inFile.Get('h_avgMass_'+eta+'_kin_'+region)
        hDress[key] = inFile.Get('h_avgMass_'+eta+'_dress_'+region)
        kinProf[key] = []
        dressProf[key] = []
        kinErr[key]=[]
        for bin in range(1,hKin[key].GetNbinsX()+1):
            kinProf[key].append(hKin[key].GetBinContent(bin))
            kinErr[key].append(hKin[key].GetBinError(bin))
            dressProf[key].append(hDress[key].GetBinContent(bin))

for eta in etaList:
    for region in regionList:
        key = eta+'_'+region
        corrections[key] = []
        finalCorrections[key] = []
        for i in range(len(dressProf[key])):
            corr = (kinProf[key][i]-dressProf[key][i])/dressProf[key][i]
            err = kinErr[key][i]/dressProf[key][i]
            corrections[key].append(corr)
            finalCorrections[key].append(0)

for key in corrections:
    for i in range(len(corrections[key])):
        doCorrection = False
        if abs(corrections[key][i]) > (kinErr[key][i] / dressProf[key][i]):
            thisSign = math.copysign(1,corrections[key][i])
            if i == 0:
                if(abs(corrections[key][i+1]) > (kinErr[key][i+1] / dressProf[key][i+1])):
                    if math.copysign(1,corrections[key][i+1]) == thisSign:
                        doCorrection = True
            elif i == len(corrections[key]) - 1:
                if(abs(corrections[key][i-1]) > kinErr[key][i-1] / dressProf[key][i-1]):
                    if math.copysign(1,corrections[key][i-1]) == thisSign:
                        doCorrection = True
            elif (abs(corrections[key][i+1]) > kinErr[key][i+1] / dressProf[key][i+1]) and (abs(corrections[key][i-1]) > kinErr[key][i-1] / dressProf[key][i-1]):
                if math.copysign(1,corrections[key][i-1]) == thisSign and math.copysign(1,corrections[key][i+1]) == thisSign:
                    doCorrection = True
            if doCorrection:
                finalCorrections[key][i] = corrections[key][i]
                if i > 0:
                    finalCorrections[key][i-1] = corrections[key][i-1]
                if i < len(corrections[key])-1:
                    finalCorrections[key][i+1] = corrections[key][i+1]
for key in sorted(corrections):
    maxErr = 0
    print key
    print finalCorrections[key]
    for i in range(len(corrections[key])):
        if finalCorrections[key][i] == 0:
            thisErr = abs(corrections[key][i])
            if thisErr > maxErr:
                maxErr = thisErr
    print 'uncertainty = ',maxErr
