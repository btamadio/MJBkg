#!/usr/bin/env python
import argparse,ROOT
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
parser = argparse.ArgumentParser(add_help=False, description='make plots')
parser.add_argument('inFile')
parser.add_argument('jobName')
args = parser.parse_args()

class plotMaker:
    def __init__(self,inFile,jobName):
        self.inFile = ROOT.TFile.Open(inFile)
        self.jobName = jobName
        self.cans = {}
        self.pad1s = {}
        self.pad2s = {}
        self.kHists = {}
        self.dHistsNom = {}
        self.dHistsUp = {}
        self.dHistsDown = {}
        self.rHistsUp = {}
        self.rHistsNom = {}
        self.rHistsDown = {}
    def makePlot(self,var,region):
        canName = var+'_'+region
        self.cans[canName]=ROOT.TCanvas(canName,canName,800,800)
        self.cans[canName].cd()
        self.pad1s[canName] = ROOT.TPad(canName+'_p1',canName+'_p1',0,0.3,1,1.0)
        self.pad1s[canName].SetBottomMargin(0.01)
        self.pad1s[canName].Draw()
        self.pad1s[canName].cd()
        self.pad1s[canName].SetLogy()
        self.kHists[canName] = self.inFile.Get('h_'+var+'_kin_'+region)
        self.dHistsUp[canName] = self.inFile.Get('h_'+var+'_dressUp_'+region)
        self.dHistsNom[canName] = self.inFile.Get('h_'+var+'_dressNom_'+region)
        self.dHistsDown[canName] = self.inFile.Get('h_'+var+'_dressDown_'+region)
        dHistNom = self.dHistsNom[canName]
        dHistUp = self.dHistsUp[canName]
        dHistDown = self.dHistsDown[canName]
        kHist = self.kHists[canName]
        dHistNom.SetLineColor(ROOT.kRed)
        dHistUp.SetLineColor(ROOT.kRed)
        dHistDown.SetLineColor(ROOT.kRed)
        kHist.SetMarkerColor(ROOT.kBlack)
        kHist.SetLineColor(ROOT.kBlack)
        kHist.SetLineWidth(2)
        kHist.SetMarkerStyle(20)
        self.rHistsUp[canName] = dHistUp.Clone()        
        self.rHistsNom[canName] = kHist.Clone()
        self.rHistsDown[canName] = dHistDown.Clone()
        rHistUp = self.rHistsUp[canName]
        rHistDown = self.rHistsDown[canName]
        rHistNom = self.rHistsNom[canName]
        rHistUp.Divide(dHistNom)
        rHistDown.Divide(dHistNom)
        rHistNom.Divide(dHistNom)

        for bin in range(1,dHistNom.GetNbinsX()+1):
            errUp = abs(dHistUp.GetBinContent(bin) - dHistNom.GetBinContent(bin))
            errDown = abs(dHistDown.GetBinContent(bin) - dHistNom.GetBinContent(bin))
#            dHistNom.SetBinError(bin,(errUp+errDown)/2.0)
        dHistNom.Draw('e')
        dHistUp.Draw('same')
        dHistDown.Draw('same')
        kHist.Draw('same ep')
        self.cans[canName].cd()
        self.pad2s[canName] = ROOT.TPad(canName+'_p2',canName+'_p2',0,0.05,1,0.3)
        self.pad2s[canName].SetTopMargin(0)
        self.pad2s[canName].SetBottomMargin(0.2)
        self.pad2s[canName].SetGridy()
        self.pad2s[canName].Draw()
        self.pad2s[canName].cd()




        rHistNom.Draw('ep')
        rHistNom.SetMinimum(0)
        rHistNom.SetMaximum(2)
        rHistUp.Draw('same')

        rHistDown.Draw('same')
        rHistNom.GetYaxis().SetNdivisions(505)
        rHistNom.GetYaxis().SetTitleSize(20)
        rHistNom.GetYaxis().SetTitleFont(43)
        rHistNom.GetYaxis().SetTitleOffset(1.55)
        rHistNom.GetYaxis().SetLabelFont(43)
        rHistNom.GetYaxis().SetLabelSize(15)
        rHistNom.GetXaxis().SetTitleSize(20)
        rHistNom.GetXaxis().SetTitleFont(43)
        rHistNom.GetXaxis().SetTitleOffset(3.8)
        rHistNom.GetXaxis().SetLabelFont(43)
        rHistNom.GetXaxis().SetLabelSize(15)
        
p=plotMaker(args.inFile,args.jobName)
p.makePlot('MJ','4jSRb9')
