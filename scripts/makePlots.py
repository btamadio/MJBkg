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
ROOT.gErrorIgnoreLevel = ROOT.kWarning
class plotMaker:
    def __init__(self,inFile,jobName,date,lumi=28):
        self.outDir = '/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/bkgEstimation/'
        self.outDir+=date+'_'+jobName
        os.system('mkdir -p '+self.outDir)
        os.system('chmod a+rx '+self.outDir)
        self.inFile = ROOT.TFile.Open(inFile)
        self.MJcut = 0.6
        self.jobName = jobName
        self.lumi=lumi
        self.legs = {}
        self.cans = {}
        self.pad1s = {}
        self.pad2s = {}
        self.kHists = {}
        self.eHists = {}
        self.dHistsNom = {}
        self.dHistsShift_cenb0 = {}
        self.dHistsShift_cenb1 = {}
        self.dHistsShift_forb0 = {}
        self.dHistsShift_forb1 = {}
        self.dHistsUp = {}
        self.dHistsDown = {}
        self.rHistsPred = {}
        self.rHistsPredUp = {}
        self.rHistsPredDown = {}
        self.rHistsKin = {}
        self.yieldHistsNom = {}
        self.yieldHistsShift_cenb0 = {}
        self.yieldHistsShift_cenb1 = {}
        self.yieldHistsShift_forb0 = {}
        self.yieldHistsShift_forb1 = {}
    def regionLabel(self,region):
        regionLabel = '#splitline{N_{jet} '
        if region is '3js0':
            regionLabel +='= 3}{n_{soft jet} = 0}'
            return regionLabel
        elif '3js1' in region:
            regionLabel +='= 3}{n_{soft jet} = 1}'
            return regionLabel
        elif '3js2' in region:
            regionLabel +='= 3}{n_{soft jet} #geq 2}'
            return regionLabel
        elif '4js0' in region:
            regionLabel +='= 4}{n_{soft jet} = 0}'
            return regionLabel
        elif '4js1' in region:
            regionLabel +='= 4}{n_{soft jet} #geq 1}'
            return regionLabel
        elif region is '5j':
            regionLabel +='#geq 5}{}'
            return regionLabel
        if '3j' in region:
            regionLabel+='= 3}'        
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
        elif 'bM' in region:
            regionLabel+='b-matched}'
        elif 'bU' in region:
            regionLabel+='non-b-matched}'
        if 'SR' in region:
            regionLabel+='{|#Delta #eta| < 1.4}}'
        elif 'VR' in region:
            regionLabel+='{|#Delta #eta| > 1.4}}'
        return regionLabel
    def makeYieldPlot(self,region):
        os.system('mkdir -p '+self.outDir+'/'+region)
        os.system('chmod a+rx '+self.outDir+'/'+region)
        labels = ('SR yield','Number of toys')
        canName = 'srYield_'+region
        self.cans[canName]=ROOT.TCanvas(canName,canName,800,600)
        self.cans[canName].cd()
        self.yieldHistsNom[canName] = self.inFile.Get('h_srYieldNom_'+region)
        yHist = self.yieldHistsNom[canName]
        yHist.SetLineColor(ROOT.kBlue)
        yHist.SetLineWidth(2)
        yHist.Draw('hist')
        yHist.GetXaxis().SetTitle(labels[0])
        yHist.GetYaxis().SetTitle(labels[1])
        lat = ROOT.TLatex()
        yLoc = 0.625
        if 'bdt' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/BDT/b-match}{binning}')
        if 'eta' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/b-match}{binning}')
        if 'ichep' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{ICHEP}{binning}')
        if 'qg' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/qg-match}{binning}')
        if 'nsubjet' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/n_{subjet}}{binning}')
        lat.DrawLatexNDC(0.24,yLoc-0.18,self.regionLabel(region))
        ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.225,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        elif 'sherpa' in self.jobName:
            lat.DrawLatexNDC(0.225,0.78,str(int(self.lumi))+' fb^{-1} Sherpa')
        elif 'data' in self.jobName:
            if 'PostICHEP' in self.jobName:
                lat.DrawLatexNDC(0.3,0.78,'#sqrt{s} = 13 TeV, 15.5 fb^{-1}')
            elif 'ICHEP' in self.jobName:
                lat.DrawLatexNDC(0.3,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
        lat.DrawLatexNDC(0.7,0.8,'#splitline{mean = %.1f}{std = %.1f}' % (yHist.GetMean(),yHist.GetRMS()))
        outFileName = self.outDir+'/'+region+'/plot_srYield_'+region+'_'+self.jobName
        self.cans[canName].Print(outFileName+'.pdf')
        self.cans[canName].Print(outFileName+'.png')
        self.cans[canName].Print(outFileName+'.C')
        os.system('chmod a+r '+self.outDir+'/'+region+'/*')
    def makePlot(self,var,region):
        if var is 'jetmass4' and '3j' in region:
            return
        os.system('mkdir -p '+self.outDir+'/'+region)
        os.system('chmod a+rx '+self.outDir+'/'+region)
        labelDict = {'jetmass':('jet mass [TeV]','Jets'),
                     'jetmass1':('leading jet mass [TeV]','Jets'),
                     'jetmass2':('2nd leading jet mass [TeV]','Jets'),
                     'jetmass3':('3rd leading jet mass [TeV]','Jets'),
                     'jetmass4':('4th leading jet mass [TeV]','Jets'),
                     'MJ':('M_{J}^{#Sigma} [TeV]','Events'),
                     'prof1d':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'prof1d_cen':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'prof1d_for':('jet p_{T} [TeV]','<m_{jet}> [TeV]')}
        canName = var+'_'+region
        self.cans[canName]=ROOT.TCanvas(canName,canName,800,800)
        self.cans[canName].cd()
        self.pad1s[canName] = ROOT.TPad(canName+'_p1',canName+'_p1',0,0.3,1,1.0)
        self.pad1s[canName].SetBottomMargin(0.01)
        self.pad1s[canName].Draw()
        self.pad1s[canName].cd()
        if not 'prof1d' in var:
            self.pad1s[canName].SetLogy()
            self.dHistsNom[canName] = self.inFile.Get('h_'+var+'_dressNom_'+region)
            self.dHistsUp[canName] = self.dHistsNom[canName].Clone('h_'+var+'_dressNom_'+region)
            self.dHistsDown[canName] = self.dHistsNom[canName].Clone('h_'+var+'_dressNom_'+region)
            self.dHistsUp[canName].SetDirectory(0)
            self.dHistsDown[canName].SetDirectory(0)
            self.dHistsShift_cenb0[canName] = self.inFile.Get('h_'+var+'_dressShift_cenb0_'+region)
            self.dHistsShift_cenb1[canName] = self.inFile.Get('h_'+var+'_dressShift_cenb1_'+region)
            self.dHistsShift_forb0[canName] = self.inFile.Get('h_'+var+'_dressShift_forb0_'+region)
            self.dHistsShift_forb1[canName] = self.inFile.Get('h_'+var+'_dressShift_forb1_'+region)
        else:
            self.dHistsNom[canName] = self.inFile.Get('h_'+var+'_dress_'+region)
        self.kHists[canName] = self.inFile.Get('h_'+var+'_kin_'+region)            
        dHistNom = self.dHistsNom[canName]
        kHist = self.kHists[canName]
        if 'prof1d' in var:
            dHistNom = self.dHistsNom[canName].ProjectionX()
            kHist = self.kHists[canName].ProjectionX()
        else:
            self.dHistsUp[canName].SetLineColor(ROOT.kBlue)
            self.dHistsUp[canName].SetLineWidth(2)
            self.dHistsDown[canName].SetLineColor(ROOT.kGreen)
            self.dHistsDown[canName].SetLineWidth(2)            
        dHistNom.SetLineColor(ROOT.kRed)
        dHistNom.SetLineColor(2)
        dHistNom.SetMarkerColor(2)
        dHistNom.SetLineWidth(2)
        kHist.SetMarkerColor(ROOT.kBlack)
        kHist.SetLineColor(ROOT.kBlack)
        kHist.SetLineWidth(2)
        kHist.SetMarkerStyle(20)
        if (var is not 'MJ') and not ('prof1d' in var):
           kHist.Rebin(10)
        self.eHists[canName] = dHistNom.Clone('eHist')
        eHist = self.eHists[canName]
        eHist.SetMarkerSize(0.001)
        eHist.SetFillColor(ROOT.kRed)
        eHist.SetFillStyle(3010)
        print region
        for bin in range(1,dHistNom.GetNbinsX()+1):
            errSyst = 0
            if not 'prof1d' in var:
                errSyst  = abs(self.dHistsShift_cenb0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_cenb1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_forb0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_forb1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                self.dHistsUp[canName].SetBinContent( bin, dHistNom.GetBinContent(bin) + errSyst )
                self.dHistsDown[canName].SetBinContent( bin, dHistNom.GetBinContent(bin) - errSyst )
                print ' ',bin,dHistNom.GetBinContent(bin), errSyst
            errStat = eHist.GetBinError(bin)
            errTot = math.sqrt(errSyst*errSyst+errStat*errStat)
            eHist.SetBinError(bin,errTot)
        eHist.Draw('e2')
        if kHist.GetMaximum() <= 0:
            print 'Error, empty histogram. var = %s, region = %s'%(var,region)
        yMax = pow(10,math.ceil(math.log(kHist.GetMaximum(),10)))
        if (yMax-kHist.GetMaximum())/yMax < 0.4:
            yMax*=5
        lastBinCont = 0
        bin = kHist.GetNbinsX()
        while lastBinCont == 0 and bin > 1:
            lastBinCont = kHist.GetBinContent(bin)
            bin -=1
        yMin = pow(10,math.floor(math.log(lastBinCont,10)))/2
        if 'prof1d' in var:
            eHist.SetMinimum(0.0)
            eHist.SetMaximum(0.25)
        else:
            eHist.SetMinimum(yMin)
            eHist.SetMaximum(yMax)
        dHistNom.Draw('hist same')
        if not 'prof1d' in var:
            self.dHistsUp[canName].Draw('hist same')
            self.dHistsDown[canName].Draw('hist same')
        #blinding - add this as an option at some point
#        if '5jSRb1' in region and var is 'MJ' and 'data' in self.jobName and '3j' not in region:
#            for bin in range(kHist.FindBin(self.MJcut),kHist.GetNbinsX()+1):
#                kHist.SetBinContent(bin,0)
#                kHist.SetBinError(bin,0)
        if not 'prof1d' in var:
            kHist.SetBinErrorOption(1)
        kHist.Draw('same ep')
        eHist.GetXaxis().SetTitle(labelDict[var][0])
        eHist.GetYaxis().SetTitle(labelDict[var][1])
        lat = ROOT.TLatex()
        yLoc = 0.4
        if 'prof1d' in var:
            yLoc += 0.2
            if 'cen' in var:
                lat.DrawLatexNDC(0.78,0.18,'|#eta| < 1.0')
            elif 'for' in var:
                lat.DrawLatexNDC(0.78,0.18,'|#eta| > 1.0')
        if 'bdt' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/BDT/b-match}{binning}')
        if 'eta' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/b-match}{binning}')
        if 'ichep' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{ICHEP}{binning}')
        if 'qg' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/qg-match}{binning}')
        if 'nsubjet' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/n_{subjet}}{binning}')
        lat.DrawLatexNDC(0.24,yLoc-0.18,self.regionLabel(region))

        ROOT.ATLASLabel(0.35,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.35,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        if 'sherpa' in self.jobName:
            lat.DrawLatexNDC(0.35,0.78,str(int(self.lumi))+' fb^{-1} Sherpa')
        elif 'data' in self.jobName:
            if 'PostICHEP' in self.jobName:
                lat.DrawLatexNDC(0.3,0.78,'#sqrt{s} = 13 TeV, 15.5 fb^{-1}')
            else:
                lat.DrawLatexNDC(0.3,0.78,'#sqrt{s} = 13 TeV, 14.8 fb^{-1}')
        if 'prof1d' in var:
            self.legs[canName] = ROOT.TLegend(0.65,0.7,0.85,0.9)
        else:            
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
            errNobs = ROOT.Double(0)
            nObs = kHist.IntegralAndError(kHist.FindBin(self.MJcut),kHist.GetNbinsX()+1,errNobs)
            yieldHistNom = self.inFile.Get('h_srYieldNom_'+region)
            yieldHistShift_cenb0 = self.inFile.Get('h_srYieldShift_cenb0_'+region)
            yieldHistShift_cenb1 = self.inFile.Get('h_srYieldShift_cenb1_'+region)
            yieldHistShift_forb0 = self.inFile.Get('h_srYieldShift_forb0_'+region)
            yieldHistShift_forb1 = self.inFile.Get('h_srYieldShift_forb1_'+region)

            nPredMean = yieldHistNom.GetMean()
            print region,yieldHistNom.GetMean()
            errStat = yieldHistNom.GetRMS()
            errSyst = (yieldHistShift_cenb0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_cenb1.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_forb0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_forb1.GetMean() - nPredMean)
            if 'pythia' in self.jobName or 'sherpa' in self.jobName:
                lat.DrawLatexNDC(0.6,0.82,'#splitline{n_{pred} = %.1f #pm %.1f #pm %.1f}{n_{obs} = %.1f #pm %.1f}' % (nPredMean,errStat,errSyst,nObs,errNobs))
            elif 'data' in self.jobName:
                lat.DrawLatexNDC(0.6,0.82,'#splitline{n_{pred} = %.1f #pm %.1f #pm %.1f}{n_{obs} = %i}' % (nPredMean,errStat,errSyst,nObs))
        self.cans[canName].cd()
        self.pad2s[canName] = ROOT.TPad(canName+'_p2',canName+'_p2',0,0.05,1,0.3)
        self.pad2s[canName].SetTopMargin(0)
        self.pad2s[canName].SetBottomMargin(0.2)
        self.pad2s[canName].SetGridy()
        self.pad2s[canName].Draw()
        self.pad2s[canName].cd()
        self.rHistsPred[canName] = eHist.Clone()
        if not 'prof1d' in var:
            self.rHistsPredUp[canName] = self.dHistsUp[canName].Clone()
            self.rHistsPredDown[canName] = self.dHistsDown[canName].Clone()
            self.rHistsPredUp[canName].Divide(dHistNom)
            self.rHistsPredDown[canName].Divide(dHistNom)
        self.rHistsKin[canName] = kHist.Clone()
        rHistPred = self.rHistsPred[canName]
        for bin in range(1,rHistPred.GetNbinsX()+1):
            if rHistPred.GetBinContent(bin) > 0:
                rHistPred.SetBinError( bin, rHistPred.GetBinError(bin) / rHistPred.GetBinContent(bin))
            else:
                rHistPred.SetBinError( bin, 1)
            rHistPred.SetBinContent(bin, 1)
        rHistKin  = self.rHistsKin[canName]
        for bin in range(1,rHistKin.GetNbinsX()+1):
            if eHist.GetBinContent(bin) > 0:
                rHistKin.SetBinError(bin,rHistKin.GetBinError(bin) / eHist.GetBinContent(bin))
                rHistKin.SetBinContent(bin,rHistKin.GetBinContent(bin) / eHist.GetBinContent(bin))
            else:
                rHistKin.SetBinError(bin,1)
                rHistKin.SetBinContent(bin,0)
        rHistPred.Draw('e2')
        rHistKin.Draw('e0 same')
        if not 'prof1d' in var:
            self.rHistsPredUp[canName].Draw('hist same')
            self.rHistsPredDown[canName].Draw('hist same')
        rHistPred.GetYaxis().SetTitle('Kin/Pred')
        rHistPred.SetMinimum(0.0)
        rHistPred.SetMaximum(1.7)
        if 'prof1d' in var:
            rHistPred.SetMinimum(0.8)
            rHistPred.SetMaximum(1.2)
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
        outFileName = self.outDir+'/'+region+'/plot_'+var+'_'+region+'_'+self.jobName
        self.cans[canName].Print(outFileName+'.pdf')
        self.cans[canName].Print(outFileName+'.png')
        self.cans[canName].Print(outFileName+'.C')
        os.system('chmod a+r '+self.outDir+'/'+region+'/*')
lumi = 14.8
if 'pythia' in args.jobName or 'sherpa' in args.jobName:
    lumi = 35
p=plotMaker(args.inFile,args.jobName,args.date,lumi)

for var in ['MJ','jetmass','jetmass1','jetmass2','jetmass3','jetmass4','prof1d','prof1d_cen','prof1d_for']:
   for region in ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM','3js0','3js1','3js2',
                  '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM','4js0','4js1',
                  '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
                  '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
                  '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM','5j',
                  '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM']:
       if var is not 'MJ':
           p.makePlot(var,region)
       else:
           if 'bU' not in region and 'bM' not in region:
               p.makePlot(var,region)
               p.makeYieldPlot(region)
