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
parser.add_argument('mjcut')
parser.add_argument('lumi')
args = parser.parse_args()
ROOT.gErrorIgnoreLevel = ROOT.kWarning
class plotMaker:
    def __init__(self,inFile,jobName,mjcut,date,lumi=28):
        self.outDir = '/global/project/projectdirs/atlas/www/multijet/RPV/btamadio/bkgEstimation/'
        self.outDir+=date+'_'+jobName
        os.system('mkdir -p '+self.outDir)
        os.system('chmod a+rx '+self.outDir)
        self.inFile = ROOT.TFile.Open(inFile)
        self.MJcut = float(mjcut)
        self.jobName = jobName
        self.lumi=lumi
        print 'self.MJcut =',self.MJcut
        print 'self.jobName =',self.jobName
        print 'self.lumi =',self.lumi
        self.legs = {}
        self.cans = {}
        self.pad1s = {}
        self.pad2s = {}
        self.kHists = {}
        self.eHists = {}
        self.dHistsNom = {}
        self.dHistsShift_eta1_b0 = {}
        self.dHistsShift_eta2_b0 = {}
        self.dHistsShift_eta3_b0 = {}
        self.dHistsShift_eta4_b0 = {}
        self.dHistsShift_eta1_b1 = {}
        self.dHistsShift_eta2_b1 = {}
        self.dHistsShift_eta3_b1 = {}
        self.dHistsShift_eta4_b1 = {}
        self.dHistsUp = {}
        self.dHistsDown = {}
        self.rHistsPred = {}
        self.rHistsPredUp = {}
        self.rHistsPredDown = {}
        self.rHistsKin = {}
        self.yieldHistsNom = {}
        self.yieldHistsShift_eta1_b0 = {}
        self.yieldHistsShift_eta2_b0 = {}
        self.yieldHistsShift_eta3_b0 = {}
        self.yieldHistsShift_eta4_b0 = {}
        self.yieldHistsShift_eta1_b1 = {}
        self.yieldHistsShift_eta2_b1 = {}
        self.yieldHistsShift_eta3_b1 = {}
        self.yieldHistsShift_eta4_b1 = {}
    def getRegionLabel(self,region):
        lines = []
        if '3j' in region:
            lines.append('N_{jet} = 3')
        elif '4j' in region:
            lines.append('N_{jet} = 4')
        elif '5j' in region:
            lines.append('N_{jet} #geq 5')
        if 's0' in region:
            lines.append('N_{soft jet} = 0')
        elif 's1' in region:
            lines.append('N_{soft jet} #geq 1')
        if 'VR' in region:
            lines.append('|#Delta #eta| > 1.4')
        elif 'SR' in region:
            lines.append('|#Delta #eta| < 1.4')
        if 'b0' in region:
            lines.append('b-veto')
        elif 'b1' in region:
            lines.append('b-tag')
        if 'bM' in region:
            lines.append('b-matched')
        elif 'bU' in region:
            lines.append('non-b-matched')
        label = ''
        if len(lines) == 1:
            label = lines[0]
        elif len(lines) == 2:
            label = '#splitline{'+lines[0]+'}{'+lines[1]+'}'
        elif len(lines) == 3:
            label = '#splitline{#splitline{'+lines[0]+'}{'+lines[1]+'}}{'+lines[2]+'}'
        elif len(lines) == 4:
            label = '#splitline{#splitline{'+lines[0]+'}{'+lines[1]+'}}{#splitline{'+lines[2]+'}{'+lines[3]+'}}'
        elif len(lines) == 5:
            label = '#splitline{#splitline{#splitline{'+lines[0]+'}{'+lines[1]+'}}{#splitline{'+lines[2]+'}{'+lines[3]+'}}}{'+lines[4]+'}'
        return label
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
        # if 'bdt' in self.jobName:
        #     lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/BDT/b-match}{binning}')
        # if 'eta' in self.jobName:
        #     lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/b-match}{binning}')
        # if 'ichep' in self.jobName:
        #     lat.DrawLatexNDC(0.24,yLoc,'#splitline{ICHEP}{binning}')
        # if 'qg' in self.jobName:
        #     lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/qg-match}{binning}')
        if 'nsubjet' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'p_{T}/|#eta|/n_{subjet} binning')
        lat.DrawLatexNDC(0.24,yLoc-0.18,self.getRegionLabel(region))
        ROOT.ATLASLabel(0.225,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.225,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        elif 'sherpa' in self.jobName:
            lat.DrawLatexNDC(0.225,0.78,str(int(self.lumi))+' fb^{-1} Sherpa')
        elif 'data' in self.jobName:
            if 'PostICHEP' in self.jobName:
                lat.DrawLatexNDC(0.25,0.78,'#sqrt{s} = 13 TeV, '+str(self.lumi)+' fb^{-1}')
            elif 'ICHEP' in self.jobName:
                lat.DrawLatexNDC(0.25,0.78,'#sqrt{s} = 13 TeV, '+str(self.lumi)+' fb^{-1}')
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
                     'avgMass':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'avgMass_eta1':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'avgMass_eta2':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'avgMass_eta3':('jet p_{T} [TeV]','<m_{jet}> [TeV]'),
                     'avgMass_eta4':('jet p_{T} [TeV]','<m_{jet}> [TeV]')}
        canName = var+'_'+region
        self.cans[canName]=ROOT.TCanvas(canName,canName,800,800)
        self.cans[canName].cd()
        self.pad1s[canName] = ROOT.TPad(canName+'_p1',canName+'_p1',0,0.3,1,1.0)
        self.pad1s[canName].SetBottomMargin(0.01)
        self.pad1s[canName].Draw()
        self.pad1s[canName].cd()
        if not 'avgMass' in var:
            self.dHistsNom[canName] = self.inFile.Get('h_'+var+'_dressNom_'+region)
            if self.dHistsNom[canName].GetMaximum() > 0:
                self.pad1s[canName].SetLogy()
            self.dHistsUp[canName] = self.dHistsNom[canName].Clone('h_'+var+'_dressNom_'+region)
            self.dHistsDown[canName] = self.dHistsNom[canName].Clone('h_'+var+'_dressNom_'+region)
            self.dHistsUp[canName].SetDirectory(0)
            self.dHistsDown[canName].SetDirectory(0)
            self.dHistsShift_eta1_b0[canName] = self.inFile.Get('h_'+var+'_dressShift_eta1_b0_'+region)
            self.dHistsShift_eta2_b0[canName] = self.inFile.Get('h_'+var+'_dressShift_eta2_b0_'+region)
            self.dHistsShift_eta3_b0[canName] = self.inFile.Get('h_'+var+'_dressShift_eta3_b0_'+region)
            self.dHistsShift_eta4_b0[canName] = self.inFile.Get('h_'+var+'_dressShift_eta4_b0_'+region)
            self.dHistsShift_eta1_b1[canName] = self.inFile.Get('h_'+var+'_dressShift_eta1_b1_'+region)
            self.dHistsShift_eta2_b1[canName] = self.inFile.Get('h_'+var+'_dressShift_eta2_b1_'+region)
            self.dHistsShift_eta3_b1[canName] = self.inFile.Get('h_'+var+'_dressShift_eta3_b1_'+region)
            self.dHistsShift_eta4_b1[canName] = self.inFile.Get('h_'+var+'_dressShift_eta4_b1_'+region)
        else:
            self.dHistsNom[canName] = self.inFile.Get('h_'+var+'_dress_'+region)
        self.kHists[canName] = self.inFile.Get('h_'+var+'_kin_'+region)            
        dHistNom = self.dHistsNom[canName]
        kHist = self.kHists[canName]
        if 'avgMass' in var:
            #dHistNom = self.dHistsNom[canName].ProjectionX()
            kHist = self.kHists[canName].ProjectionX()
            kHist.SetMarkerSize(0.01)
        else:
            self.dHistsUp[canName].SetLineColor(ROOT.kGray+1)
            self.dHistsUp[canName].SetLineWidth(2)
            self.dHistsDown[canName].SetLineColor(ROOT.kGray+1)
            self.dHistsDown[canName].SetLineWidth(2)            
        dHistNom.SetLineColor(ROOT.kRed)
        dHistNom.SetLineColor(2)
        dHistNom.SetMarkerColor(2)
        dHistNom.SetLineWidth(2)
        kHist.SetMarkerColor(ROOT.kBlack)
        kHist.SetLineColor(ROOT.kBlack)
        kHist.SetLineWidth(2)
        kHist.SetMarkerStyle(20)
        if (var is not 'MJ') and not ('avgMass' in var):
           kHist.Rebin(10)
        self.eHists[canName] = dHistNom.Clone('eHist')
        eHist = self.eHists[canName]
        eHist.SetMarkerSize(0.001)
        eHist.SetFillColor(ROOT.kRed)
        eHist.SetFillStyle(3002)
        for bin in range(1,dHistNom.GetNbinsX()+1):
            errSyst = 0
            if not 'avgMass' in var:
                errSyst  = abs(self.dHistsShift_eta1_b0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta2_b0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta3_b0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta4_b0[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta1_b1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta2_b1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta3_b1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                errSyst += abs(self.dHistsShift_eta4_b1[canName].GetBinContent(bin) - dHistNom.GetBinContent(bin))
                self.dHistsUp[canName].SetBinContent( bin, dHistNom.GetBinContent(bin) + errSyst )
                self.dHistsDown[canName].SetBinContent( bin, dHistNom.GetBinContent(bin) - errSyst )
            errStat = eHist.GetBinError(bin)
            errTot = math.sqrt(errSyst*errSyst+errStat*errStat)
            eHist.SetBinError(bin,errTot)
        eHist.Draw('e2')
#        if kHist.GetMaximum() <= 0:
#            print 'Error, empty histogram. var = %s, region = %s'%(var,region)
        yMax = 10
        if kHist.GetMaximum() > 1:
            yMax = pow(10,math.ceil(math.log(kHist.GetMaximum(),10)))
        if (yMax-kHist.GetMaximum())/yMax < 0.4:
            yMax*=5
        lastBinCont = 0
        bin = kHist.GetNbinsX()
        while lastBinCont == 0 and bin > 1:
            lastBinCont = kHist.GetBinContent(bin)
            bin -=1
        yMin = 0
        if lastBinCont > 0:
            yMin = pow(10,math.floor(math.log(lastBinCont,10)))/2
        if 'avgMass' in var:
            eHist.SetMinimum(0.0)
            eHist.SetMaximum(0.25)
        else:
            eHist.SetMinimum(yMin)
            eHist.SetMaximum(yMax)
        dHistNom.Draw('hist same')
        #TODO: UNCOMMENT
        #draw systematic bands
        if not 'avgMass' in var:
            self.dHistsUp[canName].Draw('hist same')
            self.dHistsDown[canName].Draw('hist same')
        #blinding - add this as an option at some point
        blinded = False
#        if 'SR' in region and var is 'MJ' and 'data' in self.jobName and '3j' not in region and '4j' not in region:
#            blinded = True
        if blinded:
            for bin in range(kHist.FindBin(self.MJcut),kHist.GetNbinsX()+1):
                kHist.SetBinContent(bin,0)
                kHist.SetBinError(bin,0)
        if not 'avgMass' in var:
            kHist.SetBinErrorOption(1)
        kHist.Draw('same ep')
        eHist.GetXaxis().SetTitle(labelDict[var][0])
        eHist.GetYaxis().SetTitle(labelDict[var][1])
        lat = ROOT.TLatex()
        yLoc = 0.4
        if 'avgMass' in var:
            yLoc += 0.2
            if 'eta1' in var:
                lat.DrawLatexNDC(0.78,0.18,'|#eta| < 0.5')
            elif 'eta2' in var:
                lat.DrawLatexNDC(0.78,0.18,'0.5 < |#eta| < 1.0')
            elif 'eta3' in var:
                lat.DrawLatexNDC(0.78,0.18,'1.0 < |#eta| < 1.5')
            elif 'eta4' in var:
                lat.DrawLatexNDC(0.78,0.18,'1.5 < |#eta| < 2.0')
        if 'bdt' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/BDT/b-match}{binning}')
        if 'eta' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/b-match}{binning}')
        if 'ichep' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{ICHEP}{binning}')
        if 'qg' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'#splitline{p_{T}/|#eta|/qg-match}{binning}')
        if 'nsubjet' in self.jobName:
            lat.DrawLatexNDC(0.24,yLoc,'p_{T}/|#eta|/n_{subjet} binning')
        lat.DrawLatexNDC(0.24,yLoc-0.18,self.getRegionLabel(region))

        ROOT.ATLASLabel(0.35,0.85,'Internal',0.05,0.115,1)
        if 'pythia' in self.jobName:
            lat.DrawLatexNDC(0.35,0.78,str(int(self.lumi))+' fb^{-1} Pythia')
        if 'sherpa' in self.jobName:
            lat.DrawLatexNDC(0.35,0.78,str(int(self.lumi))+' fb^{-1} Sherpa')
        elif 'data' in self.jobName:
            if 'PostICHEP' in self.jobName:
                lat.DrawLatexNDC(0.25,0.78,'#sqrt{s} = 13 TeV, '+str(self.lumi)+' fb^{-1}')
            else:
                lat.DrawLatexNDC(0.25,0.78,'#sqrt{s} = 13 TeV, '+str(self.lumi)+' fb^{-1}')
        if 'avgMass' in var:
            self.legs[canName] = ROOT.TLegend(0.65,0.7,0.85,0.9)
        else:            
            self.legs[canName] = ROOT.TLegend(0.6,0.55,0.8,0.75)
        leg = self.legs[canName]
        leg.AddEntry(kHist,'Kinematic','LP')
        leg.AddEntry(eHist,'Prediction #pm 1#sigma','LF')
        if not 'avgMass' in var:
            leg.AddEntry(self.dHistsUp[canName],'Syst. #pm 1#sigma','L')
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
            yieldHistShift_eta1_b0 = self.inFile.Get('h_srYieldShift_eta1_b0_'+region)
            yieldHistShift_eta2_b0 = self.inFile.Get('h_srYieldShift_eta2_b0_'+region)
            yieldHistShift_eta3_b0 = self.inFile.Get('h_srYieldShift_eta3_b0_'+region)
            yieldHistShift_eta4_b0 = self.inFile.Get('h_srYieldShift_eta4_b0_'+region)
            yieldHistShift_eta1_b1 = self.inFile.Get('h_srYieldShift_eta1_b1_'+region)
            yieldHistShift_eta2_b1 = self.inFile.Get('h_srYieldShift_eta2_b1_'+region)
            yieldHistShift_eta3_b1 = self.inFile.Get('h_srYieldShift_eta3_b1_'+region)
            yieldHistShift_eta4_b1 = self.inFile.Get('h_srYieldShift_eta4_b1_'+region)
            nPredMean = yieldHistNom.GetMean()

            errStat = yieldHistNom.GetRMS()
            errSyst = (yieldHistShift_eta1_b0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta2_b0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta3_b0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta4_b0.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta1_b1.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta2_b1.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta3_b1.GetMean() - nPredMean)
            errSyst+= (yieldHistShift_eta4_b1.GetMean() - nPredMean)

            if 'pythia' in self.jobName or 'sherpa' in self.jobName:
                lat.DrawLatexNDC(0.6,0.82,'#splitline{n_{pred} = %.1f #pm %.1f #pm %.1f}{n_{obs} = %.1f #pm %.1f}' % (nPredMean,errStat,errSyst,nObs,errNobs))
            elif 'data' in self.jobName:
                if blinded:
                    lat.DrawLatexNDC(0.6,0.82,'n_{pred} = %.1f #pm %.1f #pm %.1f' % (nPredMean,errStat,errSyst))
                else:
                    lat.DrawLatexNDC(0.6,0.82,'#splitline{n_{pred} = %.1f #pm %.1f #pm %.1f}{n_{obs} = %i}' % (nPredMean,errStat,errSyst,nObs))
        self.cans[canName].cd()
        self.pad2s[canName] = ROOT.TPad(canName+'_p2',canName+'_p2',0,0.05,1,0.3)
        self.pad2s[canName].SetTopMargin(0)
        self.pad2s[canName].SetBottomMargin(0.2)
        self.pad2s[canName].SetGridy()
        self.pad2s[canName].Draw()
        self.pad2s[canName].cd()
        self.rHistsPred[canName] = eHist.Clone()
        if not 'avgMass' in var:
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
        if not 'avgMass' in var:
            self.rHistsPredUp[canName].Draw('hist same')
            self.rHistsPredDown[canName].Draw('hist same')
        rHistPred.GetYaxis().SetTitle('Kin/Pred')
        rHistPred.SetMinimum(0.0)
        rHistPred.SetMaximum(1.7)
        if 'avgMass' in var:
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
# lumi = 14.8
# mjcut = 0.6
# if 'pythia' in args.jobName or 'sherpa' in args.jobName:
#     lumi = 35
#     mjcut = 0.8
p=plotMaker(args.inFile,args.jobName,args.mjcut,args.date,args.lumi)
eventRegionList = ['3jb0','3jb1','3jb9',
                   '3js0b0','3js0b1','3js0b9',
                   '3js1b0','3js1b1','3js1b9',
                   '3jVRb0','3jVRb1','3jVRb9',
                   '3js0VRb0','3js0VRb1','3js0VRb9',
                   '3js1VRb0','3js1VRb1','3js1VRb9',
                   '3jSRb0','3jSRb1','3jSRb9',
                   '3js0SRb0','3js0SRb1','3js0SRb9',
                   '3js1SRb0','3js1SRb1','3js1SRb9',

                   '4jb0','4jb1','4jb9',
                   '4js0b0','4js0b1','4js0b9',
                   '4js1b0','4js1b1','4js1b9',
                   '4jVRb0','4jVRb1','4jVRb9',
                   '4js0VRb0','4js0VRb1','4js0VRb9',
                   '4js1VRb0','4js1VRb1','4js1VRb9',
                   '4jSRb0','4jSRb1','4jSRb9',
                   '4js0SRb0','4js0SRb1','4js0SRb9',
                   '4js1SRb0','4js1SRb1','4js1SRb9',

                   '5jb0','5jb1','5jb9',
                   '5js0b0','5js0b1','5js0b9',
                   '5js1b0','5js1b1','5js1b9',
                   '5jVRb0','5jVRb1','5jVRb9',
                   '5js0VRb0','5js0VRb1','5js0VRb9',
                   '5js1VRb0','5js1VRb1','5js1VRb9',
                   '5jSRb0','5jSRb1','5jSRb9',
                   '5js0SRb0','5js0SRb1','5js0SRb9',
                   '5js1SRb0','5js1SRb1','5js1SRb9']
jetRegionList = []
for region in eventRegionList:
    jetRegionList.append(region)
    jetRegionList.append(region+'bU')
    jetRegionList.append(region+'bM')
for region in eventRegionList:
    print region,'MJ'
    p.makePlot('MJ',region)
    p.makeYieldPlot(region)
for var in ['jetmass','jetmass1','jetmass2','jetmass3','jetmass4',
            'avgMass','avgMass_eta1','avgMass_eta2','avgMass_eta3','avgMass_eta4']:
    for region in jetRegionList:
        print region,var
        p.makePlot(var,region)
