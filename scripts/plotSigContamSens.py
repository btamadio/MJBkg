#!/usr/bin/env python
import argparse,ROOT,glob,math,os,sys
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetPaintTextFormat('2.1f')
parser = argparse.ArgumentParser(add_help=False, description='make signal contamination sensitivy plots')
#inDir: directory of singal-injected samples (output_prediction files)
#inFile: baseline data sample (output_prediction file)
parser.add_argument('inDir')
parser.add_argument('inFile')
parser.add_argument('mjCut')
parser.add_argument('date')
args = parser.parse_args()
fileList = glob.glob(args.inDir+'/*')
file0 = ROOT.TFile.Open(args.inFile)

sensDict = {}
biasDict = {}
errDict = {}
           
columns = []

region = '5jSRb1'
scaleFact = 36.45 / 14.8
mjCut = float(args.mjCut)

#variables definitions:
#n_obs = number observed (from kin histogram)
#n_pred = number predicted (mean of dressed srYield hist)
#n_meas = n_obs - n_pred
#last digit is 0 for data-only, S for signal-injected

errList = ['eta1_b0','eta2_b0','eta3_b0','eta4_b0',
           'eta1_b1','eta2_b1','eta3_b1','eta4_b1']

#histograms of SR yield for data only
h_srYield_shift_0 = [file0.Get('h_srYieldShift_'+err+'_'+region) for err in errList]
h_srYield_nom_0 = file0.Get('h_srYieldNom_'+region)
h_MJ_kin_0 = file0.Get('h_MJ_kin_'+region)

n_obs_0 = scaleFact*h_MJ_kin_0.Integral(h_MJ_kin_0.FindBin(mjCut),h_MJ_kin_0.GetNbinsX())
n_pred_0 = scaleFact*h_srYield_nom_0.GetMean()
n_meas_0 = n_obs_0 - n_pred_0
print 'data only'
for hist in h_srYield_shift_0:
    erri = abs(n_pred_0 - scaleFact*hist.GetMean())
    print erri
print n_pred_0
print n_obs_0

for fName in fileList:
    dsid = int(fName.split('_')[5])
    f = ROOT.TFile.Open(fName)
    h_srYield_nom_S = f.Get('h_srYieldNom_'+region)
    h_srYield_shift_S = [f.Get('h_srYieldShift_'+err+'_'+region) for err in errList]
    h_MJ_kin_S = f.Get('h_MJ_kin_'+region)
    n_obs_S = scaleFact*h_MJ_kin_S.Integral(h_MJ_kin_S.FindBin(mjCut),h_MJ_kin_S.GetNbinsX()+1)
    n_pred_S = scaleFact*h_srYield_nom_S.GetMean()
    n_meas_S = n_obs_S - n_pred_S
    errStat = math.sqrt(n_pred_S)
    errSyst = 0.0
    mG = pointDict[dsid][0]
    mX = pointDict[dsid][1]
    errDict[(mG,mX)] = []
#    print mG,mX,n_obs_0,n_pred_0,n_meas_0
    print mG,mX
    for hist in h_srYield_shift_S:
        erri = abs(n_pred_S - scaleFact*hist.GetMean())
        errSyst += erri
        print hist.GetName(),erri
        errDict[(mG,mX)].append(erri)
    print n_pred_S
    print n_obs_S
    errTot = math.sqrt(errStat*errStat+errSyst*errSyst)
    sensDict[dsid] = n_meas_S/errTot
    biasDict[dsid] = (n_meas_S-n_meas_0)/(n_obs_S-n_obs_0)
sensHist = ROOT.TH2F('h_sens','h_sens',11,850,1950,10,-50,1950)
biasHist = ROOT.TH2F('h_bias','h_bias',11,850,1950,10,-50,1950)
for dsid in sensDict:
    mG = pointDict[dsid][0]
    mX = pointDict[dsid][1]
    xBin = sensHist.GetXaxis().FindBin(mG)
    yBin = sensHist.GetYaxis().FindBin(mX)
    sensHist.SetBinContent(xBin,yBin,sensDict[dsid])
    biasHist.SetBinContent(xBin,yBin,biasDict[dsid])

can = ROOT.TCanvas('c1','c1',800,600)
can.cd()
sensHist.Draw('text')
sensHist.SetMarkerSize(2)
sensHist.GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
sensHist.GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
lat = ROOT.TLatex()
lat.DrawLatexNDC(0.225,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
lat.DrawLatexNDC(0.225,0.7,'N_{sig}^{measured} / #sigma_{bkg}')
lat.DrawLatexNDC(0.225,0.625,'scaled to 36.45 fb^{-1}')
plotDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalInjection/'+args.date
os.system('mkdir -p '+plotDir)
os.system('chmod a+rx '+plotDir)
fName = plotDir+'/plot_n_meas_over_sigma_b'
can.Print(fName+'.pdf')
can.Print(fName+'.png')
can.Print(fName+'.C')
os.system('chmod a+r '+plotDir+'/*')

can2 = ROOT.TCanvas('c2','c2',800,600)
can2.cd()
biasHist.Draw('text')
biasHist.SetMarkerSize(2)
biasHist.GetXaxis().SetTitle('m_{#tilde{g}} [GeV]')
biasHist.GetYaxis().SetTitle('m_{#tilde{#chi}_{1}^{0}} [GeV]')
ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
lat = ROOT.TLatex()
lat.DrawLatexNDC(0.225,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
lat.DrawLatexNDC(0.225,0.7,'#Delta N_{sig}^{measured} / N_{sig}^{injected}')
lat.DrawLatexNDC(0.225,0.625,'scaled to 36.45 fb^{-1}')
fName = plotDir+'/plot_delta_n_meas_over_n_inj'
can2.Print(fName+'.pdf')
can2.Print(fName+'.png')
can2.Print(fName+'.C')
os.system('chmod a+r '+plotDir+'/*')
