#!/usr/bin/env python
import argparse,ROOT,os,math,glob
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inFile')
args = parser.parse_args()
inFile = ROOT.TFile.Open(args.inFile)

etaList = ['cen','for']
regionList = ['4jVRbU','4jVRbM']

for eta in etaList:
    for region in regionList:
        print eta, region
        hDress = inFile.Get('h_avgMass_'+eta+'_dress_'+region)
        hKin = inFile.Get('h_avgMass_'+eta+'_kin_'+region)
#        for bin in range(1,hDress.GetNbinsX()+1):
#            number of std away from mean:
#           print bin,(hKin.GetBinContent(bin)-hDress.GetBinContent(bin))/hDress.GetBinError(bin)
#           error in %:
#           print bin,(hKin.GetBinContent(bin)-hDress.GetBinContent(bin))/hDress.GetBinContent(bin)
#pythia correction factors
#corrDict = {'cen_4jSRbU':[-.063,.029,-.059,-.034,-.034,-.039,0,0,0,0,0,0,0,0,0],
#            'cen_4jSRbM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            'for_4jSRbU':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#            'for_4jSRbM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
#ICHEP correction factors
#corrDict = {'cen_4jSRbU':[-.024,-.020,-.031,-.015,-.018,-.02,0,0,0,0,0,0,0,0,0],
#            'cen_4jSRbM':[0,0,0,0,0,0,-.053,-.046,-.071,0,0,0,0,0,0],
#            'for_4jSRbU':[-.032,-.033,-.028,-.028,-.025,-.054,-.048,0,0,0,0,0,0,0,0],
#            'for_4jSRbM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
#Post-ICHEP correction factors
corrDict = {'cen_4jSRbU':[-.007,-.023,-.021,-.032,-.021,-.018,-.017,0,.016,.038,.021,.024,.020,.031,.052],
            'cen_4jSRbM':[-.039,-.046,-.030,0,0,0,0,0,0,0,0,0,0,0,0],
            'for_4jSRbU':[-.02,-.014,-.02,-.022,-.03,-.023,-.04,-.027,0,0,0,0,0,0,0],
            'for_4jSRbM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
regionList = ['4jSRbU','4jSRbM']
for eta in etaList:
    for region in regionList:
        key = eta+'_'+region
        print key
        hDress = inFile.Get('h_avgMass_'+eta+'_dress_'+region)
        hKin = inFile.Get('h_avgMass_'+eta+'_kin_'+region)
        for bin in range(1,hDress.GetNbinsX()+1):
            dressVal = hDress.GetBinContent(bin)
            dressValCorr = dressVal*(1+corrDict[key][bin-1])
            kinVal = hKin.GetBinContent(bin)
            print bin,(dressVal-kinVal)/dressVal,(dressValCorr-kinVal)/dressValCorr
