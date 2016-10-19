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
    def __init__(self,inFile,jobName,lumi=35):
        self.inFile = ROOT.TFile.Open(inFile)
        self.jobName = jobName
        self.lumi=lumi
        self.legs = {}
        self.cans = {}
        self.pad1s = {}
        self.pad2s = {}
        self.kHists = {}
        self.eHists = {}
        self.dHistsNom = {}
        self.dHistsUp = {}
        self.dHistsDown = {}
        self.rHists = {}
        self.rHistsUp = {}
        self.rHistsNom = {}
        self.rHistsDown = {}
    def regionLabel(self,region):
        regionLabel = '#splitline{N_{jet} '
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
        if 'SR' in region:
            regionLabel+='{|#Delta #eta| < 1.4}}'
        elif 'VR' in region:
            regionLabel+='{|#Delta #eta| > 1.4}}'
        return regionLabel
    def makePlot(self,var,region):
        labelDict = {'jetmass':('jet mass [TeV]','Jets / Bin Width [TeV^{-1}]'),
                      'jetmass1':('leading jet mass [TeV]','Jets / Bin Width [TeV^{-1}]'),
                      'jetmass2':('2nd leading jet mass [TeV]','Jets / Bin Width [TeV^{-1}]'),
                      'jetmass3':('3rd leading jet mass [TeV]','Jets / Bin Width [TeV^{-1}]'),
                      'jetmass4':('4th leading jet mass [TeV]','Jets / Bin Width [TeV^{-1}]'),
                      'MJ':('M_{J}^{#Sigma} [TeV]','Events / Bin Width [TeV^{-1}]')}
        
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
        dHistNom.SetLineColor(2)
        dHistNom.SetMarkerColor(2)
        dHistNom.SetLineWidth(2)

        self.eHists[canName] = dHistNom.Clone('eHist')
        eHist = self.eHists[canName]
        eHist.SetMarkerSize(0.001)
        eHist.SetFillColor(ROOT.kRed)
        eHist.SetFillStyle(3010)

        dHistUp.SetLineColor(ROOT.kRed)
        dHistDown.SetLineColor(ROOT.kRed)
        dHistUp.SetLineStyle(ROOT.kDashed)
        dHistDown.SetLineStyle(ROOT.kDashed)

        kHist.SetMarkerColor(ROOT.kBlack)
        kHist.SetLineColor(ROOT.kBlack)
        kHist.SetLineWidth(2)
        kHist.SetMarkerStyle(20)

        if var is not 'MJ':
            dHistNom.Rebin(10)
            dHistUp.Rebin(10)
            dHistDown.Rebin(10)
            kHist.Rebin(10)

        for bin in range(1,dHistNom.GetNbinsX()+1):
            errUp = abs(dHistUp.GetBinContent(bin) - dHistNom.GetBinContent(bin))
            errDown = abs(dHistDown.GetBinContent(bin) - dHistNom.GetBinContent(bin))
            eHist.SetBinError(bin,(errUp+errDown)/2.0)
        eHist.Draw('e2')
        eHist.SetMaximum(1E5)
        dHistNom.Draw('hist same')
#        dHistUp.Draw('hist same')
#        dHistDown.Draw('hist same')
        kHist.Draw('same ep')
        kHist.GetXaxis().SetTitle(labelDict[var][0])
        dHistNom.GetYaxis().SetTitle(labelDict[var][1])
        dHistNom.GetYaxis().SetTitleOffset(0.8)
        lat = ROOT.TLatex()
        lat.DrawLatexNDC(0.24,0.22,self.regionLabel(region))
        ROOT.ATLASLabel(0.4,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.4,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        elif 'data' in self.jobName:
            lat.DrawLatexNDC(0.4,0.78,'#sqrt{s} = 13 TeV, '+str(int(self.lumi))+' fb^{-1}')
        self.legs[canName] = ROOT.TLegend(0.65,0.6,0.85,0.8)
        leg = self.legs[canName]
        leg.AddEntry(kHist,'Kinematic','LP')
        leg.AddEntry(eHist,'Prediction','LF')
        leg.SetLineColor(0)
        leg.SetTextSize(0.05)
        leg.SetShadowColor(0)
        leg.SetFillStyle(0)
        leg.SetFillColor(0)
        leg.Draw()

        self.cans[canName].cd()
        self.pad2s[canName] = ROOT.TPad(canName+'_p2',canName+'_p2',0,0.05,1,0.3)
        self.pad2s[canName].SetTopMargin(0)
        self.pad2s[canName].SetBottomMargin(0.2)
        self.pad2s[canName].SetGridy()
        self.pad2s[canName].Draw()
        self.pad2s[canName].cd()
        self.rHists[canName] = eHist.Clone()
        self.rHistsUp[canName] = dHistUp.Clone()        
        self.rHistsNom[canName] = kHist.Clone()
        self.rHistsDown[canName] = dHistDown.Clone()
        rHist = self.rHists[canName]
        rHistUp = self.rHistsUp[canName]
        rHistDown = self.rHistsDown[canName]
        rHistNom = self.rHistsNom[canName]
        rHist.Divide(dHistNom)
        rHistUp.Divide(dHistNom)
        rHistDown.Divide(dHistNom)
        rHistNom.Divide(dHistNom)

        rHist.Draw('e2')
        rHistNom.Draw('ep same')
        rHist.SetMinimum(0.5)
        rHist.SetMaximum(1.7)
#        rHistUp.Draw('hist same')
#        rHistDown.Draw('hist same')
        rHist.GetYaxis().SetNdivisions(505)
        rHist.GetYaxis().SetTitleSize(20)
        rHist.GetYaxis().SetTitleFont(43)
        rHist.GetYaxis().SetTitleOffset(1.55)
        rHist.GetYaxis().SetLabelFont(43)
        rHist.GetYaxis().SetLabelSize(15)
        rHist.GetXaxis().SetTitleSize(17)
        rHist.GetXaxis().SetTitleFont(43)
        rHist.GetXaxis().SetTitleOffset(3.8)
        rHist.GetXaxis().SetLabelFont(43)
        rHist.GetXaxis().SetLabelSize(15)
        
p=plotMaker(args.inFile,args.jobName)
p.makePlot('MJ','4jSRb9')
