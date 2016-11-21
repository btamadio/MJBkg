#!/usr/bin/env python
import argparse,ROOT,os,math,pprint
from sigContamDict10 import sigContamDict10
from sigContamDict6 import sigContamDict6
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()

regionList = ['4jVRb0','4jVRb1','4jSRb0','4jSRb1',
              '5jVRb0','5jVRb1','5jSRb0','5jSRb1']

histDict10 = {}
histDict6 = {}
labelsDict = {'4jVRb0':('n_{jet} = 4','b-veto','|#Delta #eta_{12}| > 1.4'),
              '4jVRb1':('n_{jet} = 4','b-tag', '|#Delta #eta_{12}| > 1.4'),
              '4jSRb0':('n_{jet} = 4','b-veto','|#Delta #eta_{12}| < 1.4'),
              '4jSRb1':('n_{jet} = 4','b-tag', '|#Delta #eta_{12}| < 1.4'),
              '5jVRb0':('n_{jet} #geq 5','b-veto','|#Delta #eta_{12}| > 1.4'),
              '5jVRb1':('n_{jet} #geq 5','b-tag', '|#Delta #eta_{12}| > 1.4'),
              '5jSRb0':('n_{jet} #geq 5','b-veto','|#Delta #eta_{12}| < 1.4'),
              '5jSRb1':('n_{jet} #geq 5','b-tag', '|#Delta #eta_{12}| < 1.4')}

for region in regionList:
    histName10 = 'h_RPV10_sigContam_'+region
    histName6 = 'h_RPV6_sigContam_'+region
    histDict10[region] = ROOT.TH2F(histName10,histName10,13,750,2050,11,-50,2150)
    histDict6[region] = ROOT.TH1F(histName6,histName6,10,850,1850)
    for dsid in sigContamDict10:
        mG = pointDict[dsid][0]
        mX = pointDict[dsid][1]
        binX = histDict10[region].GetXaxis().FindBin(mG)
        binY = histDict10[region].GetYaxis().FindBin(mX)
        check0 = histDict10[region].GetBinContent(binX,binY)
        if check0 != 0:
            print 'Warning, bin already filled!, value = %f' % check0
            print mG,mX,binX,binY
        histDict10[region].SetBinContent(binX,binY,sigContamDict10[dsid][region])
    for dsid in sigContamDict6:
        mG = pointDict[dsid][0]
        binX = histDict6[region].GetXaxis().FindBin(mG)
        check0 = histDict6[region].GetBinContent(binX)
        if check0 !=0:
            print 'Warning, bin already filled!, value = %f' % check0
            print mG,binX
        histDict6[region].SetBinContent(binX,sigContamDict6[dsid][region])
ROOT.gStyle.SetPaintTextFormat('2.1f')
can10 = []
for region in histDict10:
    labels = labelsDict[region]
    hist = histDict10[region]
    hist.SetMarkerSize(2)
    can10.append(ROOT.TCanvas('c10_'+region,'c10_'+region,800,600))
    can10[-1].cd()
    hist.Draw('text')
    ROOT.ATLASLabel(0.175,0.875,'Internal',0.05,0.125,1)
    lat = ROOT.TLatex()
    lat.DrawLatexNDC(0.5,0.875,'#sqrt{s} = 13 TeV, 35 fb^{-1}')
    lat.DrawLatexNDC(0.175,0.775,labels[1])
    lat.DrawLatexNDC(0.275,0.775,labels[2])
    lat.DrawLatexNDC(0.47,0.775,'#frac{signal}{#sqrt{background}}')
    lat.DrawLatexNDC(0.175,0.675,labels[0])
    lat.DrawLatexNDC(0.175,0.575,'M_{J}^{#Sigma} > 800 GeV')
    fileName = '/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalContam/pythia_11_20/plot_sigContam_RPV10_'+region
    os.system('mkdir -p /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalContam/pythia_11_20/')
    can10[-1].Print(fileName+'.pdf')
    can10[-1].Print(fileName+'.png')
    can10[-1].Print(fileName+'.C')
    os.system('chmod a+r /global/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalContam/pythia_11_20/*')
