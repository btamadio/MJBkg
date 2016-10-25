#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
def median(lst):
    quotient,remainder = divmod(len(lst),2)
    if remainder:
        return sorted(lst)[quotient]
    return sum(sorted(lst)[quotient-1:quotient+1])/2
def mean(lst):
    return sum(lst) / float(len(lst))
def err(lst):
    xbar = mean(lst)
    std = 0.0
    for entry in lst:
        std += (entry-xbar)*(entry-xbar)
    std /= float(len(lst)-1)
    return math.sqrt(std)/math.sqrt(len(lst))
class bkgPredictor:
    def __init__(self,dressedFileNames,jobName,lumi=35,templateType=0):
        self.dressedFileNames = dressedFileNames
        self.nToys = len(self.dressedFileNames)
        self.jobName = jobName
        self.lumi = lumi
        self.templateType = templateType
        self.MJbins = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.40,0.45,0.5,0.6,0.8,1.0,2.0]
        self.nMJbins = len(self.MJbins)-1
        self.MJbinArray = array.array('d',self.MJbins)
        self.nMassBins = 200
        self.massBinLow = 0.0
        self.massBinUp = 2.0
        self.normRegion = (0.2,0.6)
        self.setupOutput()
        #self.loopAndFill()
    def setupOutput(self):
        outFileName = '../output_prediction/'+self.jobName+'.root'
        if os.path.isfile(outFileName):
            self.outFile = ROOT.TFile.Open(outFileName,'UPDATE')
        else:
            self.outFile = ROOT.TFile.Open(outFileName,'CREATE')
        self.regionList = ['4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
                           '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
                           '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM',
                           '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM']
        self.histList   = ['jetmass','jetmass1','jetmass2','jetmass3','jetmass4','MJ']
        #The histograms are accessed by calling histDict[regionName][histType]
        #For example, to get the kinematic leading jet mass histogram for jets in the region 4jSRb1:
        #histDict_kin['4jSRb1']['jetmass1']
        self.histDict_kin = {}
        self.histDict_dressUp = {}
        self.histDict_dressNom = {}
        self.histDict_dressDown = {}
        self.profDict_dressNom = {}
        self.profDict_dressUp = {}
        self.profDict_dressDown = {}
        for regionName in self.regionList:
            self.histDict_kin[regionName] = {}
            self.histDict_dressUp[regionName] = {}
            self.histDict_dressNom[regionName] = {}
            self.histDict_dressDown[regionName] = {}
            self.profDict_dressUp[regionName] = {}
            self.profDict_dressNom[regionName] = {}
            self.profDict_dressDown[regionName] = {}
            for histType in self.histList:
                self.profDict_dressUp[regionName][histType] = []
                self.profDict_dressNom[regionName][histType] = []
                self.profDict_dressDown[regionName][histType] = []
                histName_kin = 'h_'+histType+'_kin_'+regionName
                histName_dressUp = 'h_'+histType+'_dressUp_'+regionName
                histName_dressNom = 'h_'+histType+'_dressNom_'+regionName
                histName_dressDown = 'h_'+histType+'_dressDown_'+regionName
                if histType is 'MJ':
                    for i in range(self.nMJbins):
                        self.profDict_dressUp[regionName][histType].append([])
                        self.profDict_dressNom[regionName][histType].append([])
                        self.profDict_dressDown[regionName][histType].append([])
                    self.histDict_dressUp[regionName][histType] = ROOT.TH1F(histName_dressUp,histName_dressUp,self.nMJbins,self.MJbinArray)
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMJbins,self.MJbinArray)
                    self.histDict_dressDown[regionName][histType] = ROOT.TH1F(histName_dressDown,histName_dressDown,self.nMJbins,self.MJbinArray)
                else:
                    for i in range(self.nMassBins):
                        self.profDict_dressUp[regionName][histType].append([])
                        self.profDict_dressNom[regionName][histType].append([])
                        self.profDict_dressDown[regionName][histType].append([])
                    self.histDict_dressUp[regionName][histType] = ROOT.TH1F(histName_dressUp,histName_dressUp,self.nMassBins,self.massBinLow,self.massBinUp)
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMassBins,self.massBinLow,self.massBinUp)
                    self.histDict_dressDown[regionName][histType] = ROOT.TH1F(histName_dressDown,histName_dressDown,self.nMassBins,self.massBinLow,self.massBinUp)
    def plotResponse(self):
        f = ROOT.TFile.Open(self.dressedFileNames[0])
        t = f.Get('miniTree')

        nBinsX = 4
        xLow = 0
        xUp = 2.0

        nBinsY = 10
        yLow = -0.7
        yUp = 0.5
        
        nBinsZ = 20
        zLow = 0.0
        zUp = 2.0

        if self.templateType == 0:
            print 'template type 0: pT vs. eta'
            self.hist3D_dress = ROOT.TH3F('h_jetmass_dress_3D','h_dress',nBinsX,xLow,xUp,nBinsY,yLow,yUp,nBinsZ,zLow,zUp)
            self.hist3D_kin = ROOT.TH3F('h_jetmass_kin_3D','h_kin',nBinsX,xLow,xUp,nBinsY,yLow,yUp,nBinsZ,zLow,zUp)
            t.Draw('jet_m_dressed_nom:log10(jet_pt):abs(jet_eta)>>h_jetmass_dress_3D','njet>=4','goff')
            t.Draw('jet_m:log10(jet_pt):abs(jet_eta)>>h_jetmass_kin_3D','njet>=4','goff')
        elif self.templateType == 1:
            print 'template type 1: pT vs. BDT'
            self.hist3D_dress = ROOT.TH3F('h_jetmass_dress_3D','h_jetmass_dress_3D',nBinsX,xLow,xUp,nBinsY,yLow,yUp,nBinsZ,zLow,zUp)
            self.hist3D_kin = ROOT.TH3F('h_jetmass_kin_3D','h_jetmass_kin_3D',nBinsX,xLow,xUp,nBinsY,yLow,yUp,nBinsZ,zLow,zUp)
            t.Draw('jet_m_dressed_nom:log(jet_pt):BDTG>>h_jetmass_dress_3D','njet>=4','goff')            
            t.Draw('jet_m:log(jet_pt):BDTG>>h_jetmass_kin_3D','njet>=4','goff')            
        self.outFile.cd()
        self.hist3D_dress.Write()
        self.hist3D_kin.Write()
    def loopAndFill(self):
        #loop over pseudoexperiment files and fill prediction histograms
        #first we just copy the kinematic histogram over from the input file, rebinning the MJ histogram
        f = ROOT.TFile.Open(self.dressedFileNames[0])
        for regionName in self.regionList:
            for histType in self.histList:
                histName = 'h_'+histType+'_kin_'+regionName
                self.histDict_kin[regionName][histType] = f.Get(histName).Clone()
                if histType == 'MJ':
                    self.histDict_kin[regionName][histType] = self.histDict_kin[regionName][histType].Rebin(self.nMJbins,histName,self.MJbinArray)
                self.outFile.cd()
                self.histDict_kin[regionName][histType].Scale(self.lumi)
                self.histDict_kin[regionName][histType].Write()
        i=0
        for fileName in self.dressedFileNames:
            if i > 100:
                continue
            if i%100 == 0:
                print 'processing toy number %i' % i
            f = ROOT.TFile.Open(fileName)
            if not f:
                continue
            i+=1
            for regionName in self.regionList:
                for histType in self.histList:
                    h_dressUp = f.Get('h_'+histType+'_dressUp_'+regionName)
                    h_dressNom = f.Get('h_'+histType+'_dressNom_'+regionName)
                    h_dressDown = f.Get('h_'+histType+'_dressDown_'+regionName)
                    if histType == 'MJ':
                        h_dressUp = h_dressUp.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressNom = h_dressNom.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressDown = h_dressDown.Rebin(self.nMJbins,'',self.MJbinArray)
                    for bin in range(1,h_dressNom.GetNbinsX()+1):
                        self.profDict_dressUp[regionName][histType][bin-1].append(h_dressUp.GetBinContent(bin))
                        self.profDict_dressNom[regionName][histType][bin-1].append(h_dressNom.GetBinContent(bin))
                        self.profDict_dressDown[regionName][histType][bin-1].append(h_dressDown.GetBinContent(bin))

        for regionName in self.regionList:
            for histType in self.histList:
                for bin in range(1,self.histDict_dressNom[regionName][histType].GetNbinsX()+1):
                    self.histDict_dressUp[regionName][histType].SetBinContent(bin,mean(self.profDict_dressUp[regionName][histType][bin-1]))
                    self.histDict_dressUp[regionName][histType].SetBinError(bin,err(self.profDict_dressUp[regionName][histType][bin-1]))

                    self.histDict_dressNom[regionName][histType].SetBinContent(bin,mean(self.profDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressNom[regionName][histType].SetBinError(bin,err(self.profDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressDown[regionName][histType].SetBinContent(bin,mean(self.profDict_dressDown[regionName][histType][bin-1]))
                    self.histDict_dressDown[regionName][histType].SetBinError(bin,err(self.profDict_dressDown[regionName][histType][bin-1]))
                if histType is 'MJ':
                    kHist = self.histDict_kin[regionName][histType]
                    dHist = self.histDict_dressNom[regionName][histType]
                    #kinematic hist has already been scaled down
                    norm = kHist.Integral(kHist.FindBin(self.normRegion[0]),kHist.FindBin(self.normRegion[1])-1)/self.lumi
                    denom = dHist.Integral(dHist.FindBin(self.normRegion[0]),dHist.FindBin(self.normRegion[1])-1)
                    if denom != 0:
                        norm /= denom
                    print 'regionName = %s, norm = %f' % (regionName,norm)
                    self.histDict_dressUp[regionName][histType].Scale(2*norm*self.lumi)
                    self.histDict_dressNom[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressDown[regionName][histType].Scale(2*norm*self.lumi)
                else:
                    self.histDict_dressUp[regionName][histType].Scale(2*self.lumi)
                    self.histDict_dressNom[regionName][histType].Scale(self.lumi)
                    self.histDict_dressDown[regionName][histType].Scale(2*self.lumi)
                self.outFile.cd()
                self.histDict_dressUp[regionName][histType].Write()
                self.histDict_dressNom[regionName][histType].Write()
                self.histDict_dressDown[regionName][histType].Write()
