#!/usr/bin/env python
import argparse,ROOT,os,math
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasStyle.C')
ROOT.gROOT.LoadMacro('/global/homes/b/btamadio/atlasstyle/AtlasLabels.C')
ROOT.SetAtlasStyle()
ROOT.gROOT.SetBatch()
parser = argparse.ArgumentParser(add_help=False, description='make plots')
parser.add_argument('inFile')
parser.add_argument('jobName')
parser.add_argument('date')
args = parser.parse_args()

class plotMaker:
    def __init__(self,inFile,jobName,date,lumi=35):
        self.outDir = '/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/bkgEstimation/'
        self.outDir+=date+'_'+jobName
        os.system('mkdir -p '+self.outDir)
        os.system('chmod a+rx '+self.outDir)
        self.inFile = ROOT.TFile.Open(inFile)
        self.MJcut = 0.8
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
        self.rHistsPred = {}
        self.rHistsKin = {}
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
        os.system('mkdir -p '+self.outDir+'/'+region)
        os.system('chmod a+rx '+self.outDir+'/'+region)
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
        self.eHists[canName] = dHistNom.Clone('eHist')
        eHist = self.eHists[canName]
        eHist.SetMarkerSize(0.001)
        eHist.SetFillColor(ROOT.kRed)
        eHist.SetFillStyle(3010)

        for bin in range(1,dHistNom.GetNbinsX()+1):
            errUp = abs(dHistUp.GetBinContent(bin) - dHistNom.GetBinContent(bin))
            errDown = abs(dHistDown.GetBinContent(bin) - dHistNom.GetBinContent(bin))
            eHist.SetBinError(bin,(errUp+errDown)/2.0)
        eHist.Draw('e2')
        yMax = pow(10,math.ceil(math.log(kHist.GetMaximum(),10)))
        eHist.SetMaximum(yMax)
        dHistNom.Draw('hist same')

        kHist.Draw('same ep')
        eHist.GetXaxis().SetTitle(labelDict[var][0])
        eHist.GetYaxis().SetTitle(labelDict[var][1])
        lat = ROOT.TLatex()
        if 'bdt' in self.jobName:
            lat.DrawLatexNDC(0.24,0.4,'#splitline{p_{T}/BDT}{binning}')
        if 'eta' in self.jobName:
            lat.DrawLatexNDC(0.24,0.4,'#splitline{p_{T}/|#eta|}{binning}')
        if 'ichep' in self.jobName:
            lat.DrawLatexNDC(0.24,0.4,'#splitline{ICHEP}{binning}')
        lat.DrawLatexNDC(0.24,0.22,self.regionLabel(region))

        ROOT.ATLASLabel(0.4,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.4,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        elif 'data' in self.jobName:
            lat.DrawLatexNDC(0.4,0.78,'#sqrt{s} = 13 TeV, '+str(int(self.lumi))+' fb^{-1}')
        self.legs[canName] = ROOT.TLegend(0.65,0.55,0.85,0.75)
        leg = self.legs[canName]
        leg.AddEntry(kHist,'Kinematic','LP')
        leg.AddEntry(eHist,'Prediction','LF')
        leg.SetLineColor(0)
        leg.SetTextSize(0.05)
        leg.SetShadowColor(0)
        leg.SetFillStyle(0)
        leg.SetFillColor(0)
        leg.Draw()
        err = 0
        nObs = 0
        nPred = 0
        if var is 'MJ':
            nObs = kHist.Integral(kHist.FindBin(self.MJcut),kHist.GetNbinsX()+1)
            nPred = dHistNom.Integral(dHistNom.FindBin(self.MJcut),dHistNom.GetNbinsX()+1)
            nPredUp = dHistUp.Integral(dHistUp.FindBin(self.MJcut),dHistUp.GetNbinsX()+1)
            nPredDown = dHistDown.Integral(dHistDown.FindBin(self.MJcut),dHistDown.GetNbinsX()+1)
            errUp = abs(nPredUp-nPred)
            errDown = abs(nPredDown-nPred)
            err = (errUp+errDown)/2.0
            if 'pythia' in self.jobName:
                lat.DrawLatexNDC(0.65,0.82,'#splitline{n_{pred} = %.1f #pm %.1f}{n_{obs} = %.1f}' % (nPred,err,nObs))

        self.cans[canName].cd()
        self.pad2s[canName] = ROOT.TPad(canName+'_p2',canName+'_p2',0,0.05,1,0.3)
        self.pad2s[canName].SetTopMargin(0)
        self.pad2s[canName].SetBottomMargin(0.2)
        self.pad2s[canName].SetGridy()
        self.pad2s[canName].Draw()
        self.pad2s[canName].cd()
        self.rHistsPred[canName] = eHist.Clone()
        self.rHistsKin[canName] = kHist.Clone()
        rHistPred = self.rHistsPred[canName]
        rHistKin  = self.rHistsKin[canName]
        rHistPred.Divide(dHistNom)
        rHistKin.Divide(dHistNom)
        rHistPred.Draw('e2')
        rHistKin.Draw('ep same')
        rHistPred.GetYaxis().SetTitle('Kin/Pred')
        rHistPred.SetMinimum(0.0)
        rHistPred.SetMaximum(1.7)
        rHistPred.GetYaxis().SetNdivisions(505)
        rHistPred.GetYaxis().SetTitleSize(20)
        rHistPred.GetYaxis().SetTitleFont(43)
        rHistPred.GetYaxis().SetTitleOffset(1.55)
        rHistPred.GetYaxis().SetLabelFont(43)
        rHistPred.GetYaxis().SetLabelSize(15)
        rHistPred.GetXaxis().SetTitleSize(17)
        rHistPred.GetXaxis().SetTitleFont(43)
        rHistPred.GetXaxis().SetTitleOffset(3.8)
        rHistPred.GetXaxis().SetLabelFont(43)
        rHistPred.GetXaxis().SetLabelSize(15)

        outFileName = self.outDir+'/'+region+'/plot_'+var+'_SR_cut_'+str(int(self.MJcut*1000))+'gev_'+region+'_'+self.jobName
        self.cans[canName].Print(outFileName+'.pdf')
        self.cans[canName].Print(outFileName+'.png')
        self.cans[canName].Print(outFileName+'.C')
        os.system('chmod a+r '+self.outDir+'/'+region+'/*')
p=plotMaker(args.inFile,args.jobName,args.date)
for var in ['MJ','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']:
    for region in ['4jVRb0','4jVRb1','4jVRb9','4jSRb0','4jSRb1','4jSRb9',
                   '5jVRb0','5jVRb1','5jVRb9','5jSRb0','5jSRb1','5jSRb9']:
        p.makePlot(var,region)
