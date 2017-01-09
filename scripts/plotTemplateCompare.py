#!/usr/bin/env python
import argparse,ROOT,os,math
from controlDict import controlDict

ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()
parser = argparse.ArgumentParser(add_help=False, description='make template comparison plots')
parser.add_argument('inFile1')
parser.add_argument('inFile2')
args = parser.parse_args()

class templatePlotter:
    def __init__(self,hist1,hist2):
        self.outDir = '/project/projectdirs/atlas/www/multijet/RPV/btamadio/bkgEstimation/01_07_templates/'
        self.hist1 = hist1
        self.hist2 = hist2
        self.hist2.Sumw2()
        if self.hist1.Integral() > 0:
            self.hist1.Scale(1./self.hist1.Integral())
        if self.hist2.Integral() > 0:
            self.hist2.Scale(1./self.hist2.Integral())
        self.hist2.SetLineColor(ROOT.kBlack)
        self.hist2.SetMarkerStyle(20)
        self.hist2.SetLineWidth(1)
        self.hist3 = hist2.Clone(self.hist2.GetName()+'_clone')
        self.hist3.Divide(self.hist1)
        for bin in range(1,self.hist3.GetNbinsX()+1):
            if self.hist1.GetBinContent(bin) > 0:
                self.hist3.SetBinError(bin,self.hist2.GetBinError(bin)/self.hist1.GetBinContent(bin))        
    def plotTemplates(self):
        can = ROOT.TCanvas(self.hist1.GetName(),self.hist1.GetName(),800,800)
        ROOT.SetOwnership(can,0)
        can.cd()
        pad1= ROOT.TPad(self.hist1.GetName()+'_p1',self.hist1.GetName()+'_p1',0,0.3,1,1.0)
        pad1.SetBottomMargin(0.01)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy()
        self.hist1.Draw('hist')
        self.hist1.GetYaxis().SetTitle('fraction of jets')
        self.hist1.GetYaxis().SetTitleOffset(1.2)
        self.hist2.Draw('EX0 same')
 
        self.hist1.SetMinimum(0.5E-3)
        self.hist1.SetLineWidth(1)
        ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
        lat = ROOT.TLatex()
        lat.DrawLatexNDC(0.225,0.75,'#sqrt{s} = 13 TeV, 30.2 fb^{-1}')
        labs = self.getLabels()
        lat.DrawLatexNDC(0.225,0.675,labs[0])
        lat.DrawLatexNDC(0.225,0.6,labs[1])
        lat.DrawLatexNDC(0.225,0.525,labs[2])
        leg = ROOT.TLegend(0.225,0.2,0.35,0.4)
        ROOT.SetOwnership(leg,0)
        leg.AddEntry(self.hist2,'Data','ep')
        leg.AddEntry(self.hist1,'Pythia','f')
        leg.SetLineColor(0)
        leg.SetTextSize(0.05)
        leg.SetShadowColor(0)
        leg.SetFillStyle(0)
        leg.SetFillColor(0)
        leg.Draw()
        can.cd()
        pad2 = ROOT.TPad(self.hist1.GetName()+'_p2',self.hist1.GetName()+'_p2',0,0.05,1,0.3)
        pad2.SetTopMargin(0)
        pad2.SetBottomMargin(0.2)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        self.hist3.Draw('EX0')
        self.hist3.GetXaxis().SetTitle('log(m/p_{T})')
        self.hist3.GetYaxis().SetTitle('Data/MC')
        self.hist3.SetMaximum(1.42)
        self.hist3.SetMinimum(0.6)
        self.hist3.GetYaxis().SetNdivisions(505)
        self.hist3.GetYaxis().SetTitleSize(20)
        self.hist3.GetYaxis().SetTitleFont(43)
        self.hist3.GetYaxis().SetTitleOffset(1.55)
        self.hist3.GetYaxis().SetLabelFont(43)
        self.hist3.GetYaxis().SetLabelSize(15)
        self.hist3.GetXaxis().SetTitleSize(17)
        self.hist3.GetXaxis().SetTitleFont(43)
        self.hist3.GetXaxis().SetTitleOffset(3.8)
        self.hist3.GetXaxis().SetLabelFont(43)
        self.hist3.GetXaxis().SetLabelSize(15)
        can.Print(self.outDir+self.hist1.GetName()+'.pdf')
        can.Print(self.outDir+self.hist1.GetName()+'.png')
        can.Print(self.outDir+self.hist1.GetName()+'.C')
        os.system('chmod a+r '+self.outDir+'*')
    def getLabels(self):
        name = self.hist1.GetName()
        ptBin = int(name.split('_')[2].split('ptBin')[1])
        etaBin = int(name.split('_')[3].split('etaBin')[1])
        labelList = ['','','']
        ptBins = controlDict[0]['ptBins3']
        etaBins = controlDict[0]['yBins']
        if ptBin == 15:
            labelList[0] = 'p_{T} > '+str(int(1000*ptBins[ptBin-1]))+' GeV'
        else:
            labelList[0] = str(int(1000*ptBins[ptBin-1])) + ' < p_{T} < '+str(int(1000*ptBins[ptBin]))+' GeV'
        labelList[1] = str(etaBins[etaBin-1]) + ' < |#eta| < ' + str(etaBins[etaBin])
        if 'b0' in name:
            labelList[2] = 'b-matched'
        else:
            labelList[2] = 'non-b-matched'
        return tuple(labelList)
file1 = ROOT.TFile.Open(args.inFile1)
file2 = ROOT.TFile.Open(args.inFile2)

for key in file1.GetListOfKeys():
    h1 = file1.Get(key.GetName())
    h2 = file2.Get(key.GetName())
    t=templatePlotter(h1,h2)
    t.plotTemplates()
