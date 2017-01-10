#!/usr/bin/env python
import argparse,ROOT,glob,math,os
import pprint
from pointDict import pointDict
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gStyle.SetPaintTextFormat('2.1f')
parser = argparse.ArgumentParser(add_help=False, description='make signal contamination sensitivy plots')
parser.add_argument('inDir')
parser.add_argument('inFile')
args = parser.parse_args()
fileList = glob.glob(args.inDir+'/*')
nomFile = ROOT.TFile.Open(args.inFile)
#For each file, get the nominal background prediction, scale up by 2.46, and use sqrt(N) as stat. uncert
#Get systematic error by combining differences in shifted background predictions
#get kinematic yield
#N_injected = kinematic yield - nominal kinematic yield (scale up by 2.46)

sensDict = {}
biasDict = {}
errDict = {}
           
columns = []

region = '5jSRb1'
scaleFact = 36.45 / 14.8
nKin_nom = 6*scaleFact
mjCut = 0.8
n_meas_nom = scaleFact*2.821667
errList = ['eta1_b0','eta2_b0','eta3_b0','eta4_b0',
           'eta1_b1','eta2_b1','eta3_b1','eta4_b1']
h_srYield_nom_list = [nomFile.Get('h_srYieldShift_'+err+'_'+region) for err in errList]
h_srYield_data_only = nomFile.Get('h_srYieldNom_'+region)
#for hist in h_srYield_nom_list:
#    print scaleFact*abs(h_srYield_data_only.GetMean()-hist.GetMean())
#print h_srYield_data_only.GetMean()*scaleFact
for fName in fileList:
    dsid = int(fName.split('_')[5])
    f = ROOT.TFile.Open(fName)
    h_srYield_nom = f.Get('h_srYieldNom_'+region)
    errList = ['eta1_b0','eta2_b0','eta3_b0','eta4_b0',
               'eta1_b1','eta2_b1','eta3_b1','eta4_b1']
    h_srYield_list = [f.Get('h_srYieldShift_'+err+'_'+region) for err in errList]
    h_MJ_kin = f.Get('h_MJ_kin_'+region)
    nKin_inj = scaleFact*h_MJ_kin.Integral(h_MJ_kin.FindBin(mjCut),h_MJ_kin.GetNbinsX()+1)
    nPred_nom = h_srYield_nom.GetMean()*scaleFact
    n_meas = nKin_inj-nPred_nom
    errStat = h_srYield_nom.GetRMS()*math.sqrt(scaleFact)
    errSyst = 0.0
    mG = pointDict[dsid][0]
    mX = pointDict[dsid][1]
    errDict[(mG,mX)] = []
    print mG,mX,nPred_nom
    for hist in h_srYield_list:
        errSyst += abs(nPred_nom - scaleFact*hist.GetMean())
        errDict[(mG,mX)].append(abs(nPred_nom-scaleFact*hist.GetMean()))
    errTot = math.sqrt(errStat*errStat+errSyst*errSyst)
    sensDict[dsid] = n_meas/errTot
    biasDict[dsid] = (n_meas-n_meas_nom)/(nKin_inj-nKin_nom)
# for key in errDict:
#     print key
#     for err in errDict[key]:
#         print err
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
plotDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalInjection/01_09'
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
plotDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/SignalInjection/01_09'
os.system('mkdir -p '+plotDir)
os.system('chmod a+rx '+plotDir)
fName = plotDir+'/plot_delta_n_meas_over_n_inj'
can2.Print(fName+'.pdf')
can2.Print(fName+'.png')
can2.Print(fName+'.C')
os.system('chmod a+r '+plotDir+'/*')
