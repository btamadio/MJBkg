#!/usr/bin/env python
import argparse,os,ROOT
from array import array
from glob import glob
parser = argparse.ArgumentParser(add_help=False, description='compare pT, eta, and mass distributions for resampling')
parser.add_argument('inFile')
parser.add_argument('inFileResamp')
parser.add_argument('jobName')
parser.add_argument('date')
args = parser.parse_args()
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

inFile = ROOT.TFile.Open(args.inFile)
inFileResamp = ROOT.TFile.Open(args.inFileResamp)

tree = inFile.Get('miniTree')
treeResamp = inFileResamp.Get('miniTree')

drawStrings = ['jet_pt[0]','jet_pt[1]','jet_pt[2]','jet_pt[3]',
               'abs(jet_eta[0])','abs(jet_eta[1])','abs(jet_eta[2])','abs(jet_eta[3])']
selString = 'njet==4'
xLabs = ['p_{T1} [TeV]','p_{T2} [TeV]','p_{T3} [TeV]','p_{T4} [TeV]',
         '#eta_{1}','#eta_{2}','#eta_{3}','#eta_{4}',
         'M_{J}^{#Sigma} [TeV]']

xMin = [0.44,0.2,0.2,0.2,0,0,0,0]
xMax = [2.5,1.8,1.0,0.8,2,2,2,2]
nBins = [50,50,50,50,20,20,20,20]
hists = [ROOT.TH1F('h_'+str(i),'h_'+str(i),nBins[i],xMin[i],xMax[i]) for i in range(len(xMin))]
histsResamp = [ROOT.TH1F('h_re_'+str(i),'h_re_'+str(i),nBins[i],xMin[i],xMax[i]) for i in range(len(xMin))]
for i in range(len(drawStrings)):
    tree.Draw(drawStrings[i]+'>>'+'h_'+str(i),selString,'goff')
    treeResamp.Draw(drawStrings[i]+'>>'+'h_re_'+str(i),selString,'goff')
hists.append(inFile.Get('h_MJ_dressNom_4jb9'))
histsResamp.append(inFileResamp.Get('h_MJ_dressNom_4jb9'))
hKin = inFile.Get('h_MJ_kin_4jb9')
cans = []
legs = []

outDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/Resampling/'+args.date+'_'+args.jobName
cmd = 'mkdir -p '+outDir
os.system(cmd)
fileNameList = ['pt1','pt2','pt3','pt4','eta1','eta2','eta3','eta4','MJ']

for i in range(len(hists)):
    cans.append(ROOT.TCanvas('c_'+str(i),'c_'+str(i),800,600))
    cans[-1].cd()
    if i<4:
        cans[-1].SetLogy()
    if i < 8:
        hists[i].SetLineColor(ROOT.kBlack)
        histsResamp[i].SetLineColor(ROOT.kRed)
        hists[i].Draw()
        histsResamp[i].Draw('same')
        hists[i].GetXaxis().SetTitle(xLabs[i])
        hists[i].GetYaxis().SetTitle('Events')
        legs.append(ROOT.TLegend(0.65,0.7,0.85,0.9))
        legs[-1].AddEntry(hists[i],'Kinematic','F')
        legs[-1].AddEntry(histsResamp[i],'Resampled','F')
    else:
        cans[-1].SetLogy()
        hKin.SetLineColor(ROOT.kBlack)
        histsResamp[i].SetLineColor(ROOT.kRed)
        hists[i].SetLineColor(ROOT.kGreen)
        hKin.Draw()
        hists[i].Draw('same')
        histsResamp[i].Draw('same')
        legs.append(ROOT.TLegend(0.45,0.7,0.65,0.9))
        legs[-1].AddEntry(hKin,'Kinematic','F')
        legs[-1].AddEntry(hists[i],'Dressed','F')
        legs[-1].AddEntry(histsResamp[i],'Resampled and Dressed','F')
        hKin.GetXaxis().SetTitle(xLabs[i])
        hKin.GetYaxis().SetTitle('Events')
    legs[-1].SetLineColor(0)
    legs[-1].SetTextSize(0.05)
    legs[-1].SetShadowColor(0)
    legs[-1].SetFillStyle(0)
    legs[-1].SetFillColor(0)
    legs[-1].Draw()

    fileName = outDir+'/'+'plot_'+fileNameList[i]+'_kinematic_vs_resamp'
    cans[-1].Print(fileName+'.pdf')
    cans[-1].Print(fileName+'.png')
    cans[-1].Print(fileName+'.C')

os.system('chmod a+rx '+outDir)
os.system('chmod a+r '+outDir+'/*')
