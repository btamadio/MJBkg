#!/usr/bin/env python
import argparse,ROOT,os,math
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()
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
colors = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kViolet,ROOT.kOrange]
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
for region in ['3jVRb0','3jVRb1','3jVRb9',
               '3jSRb0','3jSRb1','3jSRb9',
               '4jVRb0','4jVRb1','4jVRb9',
               '4jSRb0','4jSRb1','4jSRb9',
               '5jVRb0','5jVRb1','5jVRb9',
               '5jSRb0','5jSRb1','5jSRb9']:
    kinHists[region] = inFileList[0].Get('h_MJ_kin_'+region)
    hists[region] = []
    ratioHists[region] = []
    cans[region] = ROOT.TCanvas(region,region,800,800)
    cans[region].cd()
    p1[region] = ROOT.TPad(region+'_p1',region+'_p1',0,0.3,1,1.0)
    p1[region].SetBottomMargin(0.01)
    p1[region].Draw()
    p1[region].cd()
    p1[region].SetLogy()
    lat = ROOT.TLatex()
    leg[region] = ROOT.TLegend(0.65,0.55,0.85,0.85)
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
        hists[region].append(inFileList[i].Get('h_MJ_dressNom_'+region))
        hists[region][i].SetLineColor(colors[i])
        hists[region][i].SetLineWidth(2)
        ratioHists[region].append(hists[region][i].Clone('ratio_'+region+'_'+str(i)))
        ratioHists[region][i].Divide(hists[region][0])
        leg[region].AddEntry(hists[region][i],legLabels[i],'LF')
        if i == 0:
            hists[region][i].Draw('hist')
            hists[region][i].SetMinimum(yMin)
            hists[region][i].SetMaximum(yMax)
            hists[region][i].GetYaxis().SetTitle('Events / Bin Width [TeV^{-1}]')
        else:
            hists[region][i].Draw('hist same')
    kinHists[region].Draw('same')
    kinHists[region].SetMarkerColor(ROOT.kBlack)
    kinHists[region].SetLineColor(ROOT.kBlack)
    kinHists[region].SetLineWidth(2)
    kinHists[region].SetMarkerStyle(20)
    kinRatioHists[region] = kinHists[region].Clone('h_kinRatio_'+region)
    kinRatioHists[region].Divide(hists[region][0])
    leg[region].Draw()
    ROOT.ATLASLabel(0.4,0.85,'Internal',0.05,0.115,1)
    lat.DrawLatexNDC(0.4,0.78,'35 fb^{-1} Pythia')
    lat.DrawLatexNDC(0.24,0.22,regionLabel(region))
    cans[region].cd()
    p2[region] = ROOT.TPad(region+'_p2',region+'_p2',0,0.05,1,0.3)
    p2[region].SetTopMargin(0)
    p2[region].SetBottomMargin(0.2)
    p2[region].SetGridy()
    p2[region].Draw()
    p2[region].cd()
    for i in range(1,len(ratioHists[region])):
        if i == 1:
            ratioHists[region][i].Draw('hist')
            ratioHists[region][i].SetMinimum(0.5)
            ratioHists[region][i].SetMaximum(1.8)
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
    outFileName= outDir+'MJ_w_ratios_'+region
    cans[region].cd()
    cans[region].Print(outFileName+'.png')
    cans[region].Print(outFileName+'.pdf')
    cans[region].Print(outFileName+'.C')
    os.system('chmod a+r '+outDir+'*')
