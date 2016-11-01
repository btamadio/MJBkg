#!/usr/bin/env python
import argparse,ROOT,os,math,array
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()

ptBins3 = [0.2,0.221,0.244,0.270,0.293,0.329,0.364,0.402,0.445,0.492,0.544,0.6,0.644,0.733,0.811,0.896]
ptBins4 = [0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733,0.896]
ptBins5 = [0.2,0.244,0.293,0.364,0.445,0.52,0.6,0.733]

nBins4 = len(ptBins4)-1
nBins5 = len(ptBins5)-1

binArray4 = array.array('d',ptBins4)
binArray5 = array.array('d',ptBins5)

def regionLabel(region):
    regionLabel = '#splitline{N_{jet} '
    if '3j' in region:
        regionLabel+='= 3}'        
    if '4j' in region:
        regionLabel+='= 4}'
    elif '5j' in region:
        regionLabel+='#geq 5}'
    regionLabel+='{#splitline{'
    if 'b0' in region:
        regionLabel+='b-veto}'
    elif 'b1' in region:
        regionLabel+='b-tag}'
    elif 'b9' in region:
        regionLabel+='b-inclusive}'
    elif 'bM' in region:
        regionLabel+='b-matched}'
    elif 'bU' in region:
        regionLabel+='non-b-matched}'
    if 'SR' in region:
        regionLabel+='{|#Delta #eta| < 1.4}}'
    elif 'VR' in region:
        regionLabel+='{|#Delta #eta| > 1.4}}'
    return regionLabel
outDir = '/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/bkgEstimation/10_27_pythia_compare/'
inFileNameList= ['../output_prediction/pythia_ichep_uncorr.root',
                 '../output_prediction/pythia_eta_uncorr.root',
                 '../output_prediction/pythia_bdt_uncorr.root',
                 '../output_prediction/pythia_qg.root',
                 '../output_prediction/pythia_nsubjet.root']
colors = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kViolet,ROOT.kOrange+8]
legLabels = ['ICHEP','p_{T}/|#eta|/b-match','p_{T}/BDT/b-match','p_{T}/|#eta|/ q/g-match','p_{T}/|#eta|/n_{subjet}']
inFileList = [ROOT.TFile.Open(inFile) for inFile in inFileNameList]
cans = {}
p1 = {}
p2 = {}
hists = {}
ratioHists = {}
kinHists = {}
kinRatioHists = {}
leg = {}
plot = 'prof1d'
#plot = 'MJ'
regionList = ['3jVRb0','3jVRb1','3jVRb9',
              '3jSRb0','3jSRb1','3jSRb9',
              '4jVRb0','4jVRb1','4jVRb9',
              '4jSRb0','4jSRb1','4jSRb9',
              '5jVRb0','5jVRb1','5jVRb9',
              '5jSRb0','5jSRb1','5jSRb9']
if plot == 'prof1d':
    regionList = ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
                  '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
                  '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
                  '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
                  '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM',
                  '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM']
    
for region in regionList:
    kinHists[region] = inFileList[0].Get('h_'+plot+'_kin_'+region)
    hists[region] = []
    ratioHists[region] = []
    cans[region] = ROOT.TCanvas(region,region,800,800)
    cans[region].cd()
    p1[region] = ROOT.TPad(region+'_p1',region+'_p1',0,0.3,1,1.0)
    p1[region].SetBottomMargin(0.01)
    p1[region].Draw()
    p1[region].cd()
    if plot is 'MJ':
        p1[region].SetLogy()
    lat = ROOT.TLatex()
    leg[region] = ROOT.TLegend(0.625,0.5,0.825,0.90)
    leg[region].SetLineColor(0)
    leg[region].SetTextSize(0.05)
    leg[region].SetShadowColor(0)
    leg[region].SetFillStyle(0)
    leg[region].SetFillColor(0)
    yMax = pow(10,math.ceil(math.log(kinHists[region].GetMaximum(),10)))
    if (yMax-kinHists[region].GetMaximum())/yMax < 0.4:
        yMax*=5
    lastBinCont = 0
    bin = kinHists[region].GetNbinsX()
    while lastBinCont == 0 and bin > 1:
        lastBinCont = kinHists[region].GetBinContent(bin)
        bin -=1
    yMin = pow(10,math.floor(math.log(lastBinCont,10)))/2
    for i in range(len(inFileList)):
        if plot is 'MJ':
            hists[region].append(inFileList[i].Get('h_'+plot+'_dressNom_'+region))
        elif plot is 'prof1d':
            if '3j' in region:
                hists[region].append(inFileList[i].Get('h_'+plot+'_dressNom_'+region))
            elif '4j' in region:
                hists[region].append((inFileList[i].Get('h_'+plot+'_dressNom_'+region)).Rebin(nBins4,'newHist_'+str(i),binArray4))
                                   
            elif '5j' in region:
                hists[region].append((inFileList[i].Get('h_'+plot+'_dressNom_'+region)).Rebin(nBins5,'newHist_'+str(i),binArray5))                                     
        hists[region][i].SetLineColor(colors[i])
        hists[region][i].SetLineWidth(2)
        if plot is 'MJ':
            ratioHists[region].append(hists[region][i].Clone('ratio_'+region+'_'+str(i)))
            ratioHists[region][i].Divide(hists[region][0])
        elif plot is 'prof1d':
            ratioHists[region].append(hists[region][i].Clone('ratio_'+region+'_'+str(i)).ProjectionX())
            ratioHists[region][i].Divide(hists[region][0].ProjectionX())
        leg[region].AddEntry(hists[region][i],legLabels[i],'LF')
        if i == 0:
            hists[region][i].Draw('hist')
            if plot is 'MJ':
                hists[region][i].SetMinimum(yMin)
                hists[region][i].SetMaximum(yMax)
            else:
                hists[region][i].SetMinimum(0)
                hists[region][i].SetMaximum(0.25)
            hists[region][i].GetYaxis().SetTitle('Events / Bin Width [TeV^{-1}]')
        else:
            hists[region][i].Draw('hist same')
    kinHists[region].Draw('same')
    kinHists[region].SetMarkerColor(ROOT.kBlack)
    kinHists[region].SetLineColor(ROOT.kBlack)
    kinHists[region].SetLineWidth(2)
    kinHists[region].SetMarkerStyle(20)
    if plot is 'MJ':
        kinRatioHists[region] = kinHists[region].Clone('h_kinRatio_'+region)
        kinRatioHists[region].Divide(hists[region][0])
    elif plot is 'prof1d':
        kinRatioHists[region] = kinHists[region].Clone('h_kinRatio_'+region).ProjectionX()
        kinRatioHists[region].Divide(hists[region][0].ProjectionX())
    leg[region].AddEntry(kinHists[region],'kinematic','LP')
    leg[region].Draw()
    ROOT.ATLASLabel(0.4,0.85,'Internal',0.05,0.115,1)
    lat.DrawLatexNDC(0.4,0.78,'35 fb^{-1} Pythia')
    if plot is 'MJ':
        lat.DrawLatexNDC(0.24,0.22,regionLabel(region))
    elif plot is 'prof1d':
        lat.DrawLatexNDC(0.24,0.4,regionLabel(region))
    cans[region].cd()
    p2[region] = ROOT.TPad(region+'_p2',region+'_p2',0,0.05,1,0.3)
    p2[region].SetTopMargin(0)
    p2[region].SetBottomMargin(0.2)
    p2[region].SetGridy()
    p2[region].Draw()
    p2[region].cd()
    for i in range(1,len(ratioHists[region])):
        ratioHists[region][i].SetLineColor(colors[i])
        if i == 1:
            ratioHists[region][i].Draw('hist')
            if plot is 'MJ':
                ratioHists[region][i].SetMinimum(0.5)
                ratioHists[region][i].SetMaximum(1.8)
                ratioHists[region][i].GetXaxis().SetTitle('M_{J}^{#Sigma} [TeV]')
            elif plot is 'prof1d':
                ratioHists[region][i].SetMinimum(0.9)
                ratioHists[region][i].SetMaximum(1.1)
                ratioHists[region][i].GetXaxis().SetTitle('jet p_{T} [TeV]')
            ratioHists[region][i].GetYaxis().SetTitle(' ./ ICHEP')
            ratioHists[region][i].GetYaxis().SetNdivisions(505)
            ratioHists[region][i].GetYaxis().SetTitleSize(20)
            ratioHists[region][i].GetYaxis().SetTitleFont(43)
            ratioHists[region][i].GetYaxis().SetTitleOffset(1.55)
            ratioHists[region][i].GetYaxis().SetLabelFont(43)
            ratioHists[region][i].GetYaxis().SetLabelSize(15)
            ratioHists[region][i].GetXaxis().SetTitleSize(17)
            ratioHists[region][i].GetXaxis().SetTitleFont(43)
            ratioHists[region][i].GetXaxis().SetTitleOffset(3.8)
            ratioHists[region][i].GetXaxis().SetLabelFont(43)
            ratioHists[region][i].GetXaxis().SetLabelSize(15)
        else:
            ratioHists[region][i].Draw('hist same')
    kinRatioHists[region].Draw('same')
    outFileName= outDir+plot+'_w_ratios_'+region
    cans[region].cd()
    cans[region].Print(outFileName+'.png')
    cans[region].Print(outFileName+'.pdf')
    cans[region].Print(outFileName+'.C')
    os.system('chmod a+r '+outDir+'*')
