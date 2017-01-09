#!/usr/bin/env python
import argparse,ROOT,os,math,glob,pprint
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetPaintTextFormat('2.1f')

mjCut = 0.6

file0 = ROOT.TFile.Open('../output_prediction/data_ICHEP.root')
fileNameList = glob.glob('../output_prediction/SignalInjection_dataICHEP_*.root')

h_kin0 = file0.Get('h_MJ_kin_5jSRb1')
h_dress0 = file0.Get('h_MJ_dressNom_5jSRb1')

n_pred_noInj = h_dress0.Integral(h_dress0.FindBin(mjCut),h_dress0.GetNbinsX()+1)
n_kin_noInj = h_kin0.Integral(h_kin0.FindBin(mjCut),h_kin0.GetNbinsX()+1)

n_pred_dict = {}
n_kin_dict = {}

h0 = ROOT.TH2F('h0','#Delta_{N_{pred}}',11,850,1950,10,-50,1950)
h1 = ROOT.TH2F('h1','#Delta_{N_{pred}} / N_{injected}',11,850,1950,10,-50,1950)

for fileName in sorted(fileNameList):
    dsid = int(fileName.split('_')[-1].split('.')[0])
    if dsid in range(403580,403584) or dsid > 403604:
        continue
    f= ROOT.TFile.Open(fileName)
    h_kin = f.Get('h_MJ_kin_5jSRb1')
    h_dress = f.Get('h_MJ_dressNom_5jSRb1')
    n_pred_dict[dsid] = h_dress.Integral(h_dress.FindBin(mjCut),h_dress.GetNbinsX()+1)
    n_kin_dict[dsid] = h_kin.Integral(h_kin.FindBin(mjCut),h_kin.GetNbinsX()+1)
for key in n_pred_dict:
    mG = pointDict[key][0]
    mX = pointDict[key][1]
    nInj = n_kin_dict[key] - n_kin_noInj
    dN = n_pred_dict[key] - n_pred_noInj
    x = h0.GetXaxis().FindBin(mG)
    y = h0.GetYaxis().FindBin(mX)
    h0.SetBinContent(x,y,dN)
    h1.SetBinContent(x,y,100*dN/nInj)
can0 = ROOT.TCanvas('c0','c0',800,600)
can0.cd()
h0.Draw('text')
h0.SetMarkerSize(1.8)
h0.GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
h0.GetYaxis().SetTitle('m_{#tilde{#chi_{1}^{0}}} [GeV]')
ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
lat = ROOT.TLatex()
lat.DrawLatexNDC(0.225,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
lat.DrawLatexNDC(0.225,0.7,'N_{pred}^{sig. inj} - N_{pred}^{nom}')

can1 = ROOT.TCanvas('c1','c1',800,600)
can1.cd()
h1.Draw('text')
h1.SetMarkerSize(1.8)
h1.GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
h1.GetYaxis().SetTitle('m_{#tilde{#chi_{1}^{0}}} [GeV]')
ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
lat = ROOT.TLatex()
lat.DrawLatexNDC(0.225,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
lat.DrawLatexNDC(0.225,0.655,'100#times #frac{N_{pred}^{sig. inj} - N_{pred}^{nom}}{N_{injected}}')
plotDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalInjection/01_06'
fName = plotDir+'/plot_npred_inj_minus_nom'
can0.Print(fName+'.pdf')
can0.Print(fName+'.png')
can0.Print(fName+'.C')
fName = plotDir+'/plot_npred_inj_minus_nom_over_n_inj'
can1.Print(fName+'.pdf')
can1.Print(fName+'.png')
can1.Print(fName+'.C')
os.system('chmod a+rx '+plotDir)
os.system('chmod a+r '+plotDir+'/*')
