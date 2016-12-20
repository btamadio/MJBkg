#!/usr/bin/env python
import argparse,ROOT,os,math,glob,pprint
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inFileName')
args = parser.parse_args()
inFile = ROOT.TFile.Open(args.inFileName)

etaList = ['eta1','eta2','eta3','eta4']
regionList = ['4js1VRb9bU','4js1VRb9bM']

hKin = {}
hDress = {}
kinProf = {}
dressProf = {}
kinErr = {}
corrections = {}
errors = {}
def mean(lst):
    if len(lst) < 1:
        return 0
    return sum(lst) / float(len(lst))
def std(lst):
    if len(lst) < 2:
        return 0
    xbar = 0.0
    std = 0.0
    for entry in lst:
        std += (entry-xbar)*(entry-xbar)
    std /= float(len(lst)-1)
    return math.sqrt(std)

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
        errors[key] = []
        for i in range(len(dressProf[key])):
            corr = dressProf[key][i]/kinProf[key][i]-1.0
            err = kinErr[key][i]/dressProf[key][i]
            corrections[key].append(corr)
            errors[key].append(err)
print 'key','mean error','std of response','ratio'
for eta in etaList:
    for region in regionList:
        key = eta+'_'+region
        print key,mean(errors[key]),std(corrections[key]),std(corrections[key])/mean(errors[key])
