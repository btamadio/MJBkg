#!/usr/bin/env python
import ROOT,argparse
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
parser = argparse.ArgumentParser(add_help=False, description='plot SR optimization')
parser.add_argument('inFile')
args = parser.parse_args()
inFile = ROOT.TFile.Open(args.inFile)
h_mj = inFile.Get('h_mj')
h_dEta = inFile.Get('h_dEta')
ROOT.gStyle.SetPaintTextFormat('2.2f')
hists = [h_mj,h_dEta]
labels = ['Optimal M_{J}^{#Sigma} Cut [TeV]','Optimal |#Delta #eta| cut']
cans = []
for i in range(len(hists)):
    cans.append(ROOT.TCanvas('c'+str(i),'c'+str(i),800,600))
    cans[-1].cd()
    hists[i].SetMarkerSize(1.5)
    hists[i].Draw('text')
    hists[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
    hists[i].GetXaxis().SetTitleOffset(1.5)

    hists[i].GetYaxis().SetTitle('m_{#tilde{#chi_{1}^{0}}} [GeV]')
    hists[i].GetYaxis().SetTitleOffset(1.5)
    ROOT.ATLASLabel(0.18,0.85,'Internal',0.05,0.115,1)
    lat = ROOT.TLatex()
    lat.DrawLatexNDC(0.18,0.75,'Pythia #int L dt = 36.5 fb^{-1}')
    lat.DrawLatexNDC(0.18,0.65,labels[i])
    
mjcuts = [600,750]
dEtaCuts = [1.4,1.7]
oldSig = ROOT.TH2F('h_oldSig','h_oldSig',13,650,1950,9,-50,1750)
newSig = ROOT.TH2F('h_newSig','h_newSig',13,650,1950,9,-50,1750)
sigs = [oldSig,newSig]
for dsid in pointDict:
    mG = pointDict[dsid][0]
    mX = pointDict[dsid][1]
    if mX == 0:
        continue
    h = inFile.Get('h_sig_'+str(dsid))
    s_old = h.GetBinContent(h.FindBin(.6,1.4))
    s_new = h.GetBinContent(h.FindBin(.75,1.7))
    xBin = oldSig.GetXaxis().FindBin(mG)
    yBin = oldSig.GetYaxis().FindBin(mX)
    oldSig.SetBinContent(xBin,yBin,s_old)
    newSig.SetBinContent(xBin,yBin,s_new)
sigLabels = ['#splitline{M_{J}^{#Sigma} > 600 GeV, |#Delta #eta| < 1.4}{S/#sqrt{B}}',
             '#splitline{M_{J}^{#Sigma} > 750 GeV, |#Delta #eta| < 1.7}{S/#sqrt{B}}']
for i in range(len(sigs)):
    cans.append(ROOT.TCanvas('c'+str(i+2),'c'+str(i+2),800,600))
    cans[-1].cd()
    sigs[i].SetMarkerSize(1.5)
    sigs[i].Draw('text')
    sigs[i].GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
    sigs[i].GetXaxis().SetTitleOffset(1.5)
    sigs[i].GetYaxis().SetTitle('m_{#tilde{#chi_{1}^{0}}} [GeV]')
    sigs[i].GetYaxis().SetTitleOffset(1.5)
    ROOT.ATLASLabel(0.18,0.875,'Internal',0.05,0.115,1)
    lat = ROOT.TLatex()
    lat.DrawLatexNDC(0.18,0.775,'Pythia #int L dt = 36.5 fb^{-1}')
    lat.DrawLatexNDC(0.18,0.65,sigLabels[i])
