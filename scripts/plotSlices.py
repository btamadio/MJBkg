#!/usr/bin/env python
import argparse,ROOT,os
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()

parser = argparse.ArgumentParser(add_help=False, description='plot slices')
parser.add_argument('inFile')
args = parser.parse_args()

f = ROOT.TFile.Open(args.inFile)
t = f.Get('miniTree')

#runList = [361023,361024,361025,361026,361027,361028,361029,361030,
#           426043,426044,426045,426046,426047,426048,426049,426050]

#runList = [426043,426044,
runList=[426043,426044,426045,426046,426047,426048,426049,426050]
histList = [ROOT.TH1F('h_'+str(run),'h_'+str(run),200,0.44,5) for run in runList]
colorList = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kBlack,
             ROOT.kYellow,ROOT.kOrange,ROOT.kViolet,ROOT.kCyan]
#colorList = [1,2,3,4,5,6,7,8,
#             1,2,3,4,5,6,7,8]
stack = ROOT.THStack('hs','')
for i in range(len(runList)):
    run=runList[i]
    t.Draw('jet_pt[0]>>h_'+str(run),'weight*(mcChannelNumber=='+str(run)+')','goff')
    histList[i].SetFillColor(colorList[i])
    histList[i].SetMarkerSize(0)
    stack.Add(histList[i])
c=ROOT.TCanvas('c','c',800,600)
c.SetLogy()
stack.Draw('h')
