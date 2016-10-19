#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
def median(lst):
    quotient,remainder = divmod(len(lst),2)
    if remainder:
        return sorted(lst)[quotient]
    return sum(sorted(lst)[quotient-1:quotient+1])/2
def mean(lst):
    return sum(lst) / float(len(lst))
def std(lst):
    xbar = mean(lst)
    std = 0.0
    for entry in lst:
        std += (entry-xbar)*(entry-xbar)
    std /= float(len(lst)-1)
    return math.sqrt(std)
class bkgPredictor:
    def __init__(self,dressedFileNames,jobName,lumi=35):
        self.dressedFileNames = dressedFileNames
        self.jobName = jobName
        self.lumi = lumi
        self.MJbins = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.40,0.45,0.5,0.6,0.8,1.0,2.0]
        self.nMJbins = len(self.MJbins)-1
        self.MJbinArray = array.array('d',self.MJbins)
        self.nMassBins = 200
        self.massBinLow = 0.0
        self.massBinUp = 2.0
        self.mjCut = 800.0
        self.normRegion = (0.2,0.6)
        self.setupOutput()
        self.loopAndFill()

    def setupOutput(self):
        self.outFile = ROOT.TFile.Open('../output_prediction/'+self.jobName+'.root','RECREATE')
        self.regionList = ['4jVRb0','4jVRb1','4jVRb9','4jSRb0','4jSRb1','4jSRb9',
                           '5jVRb0','5jVRb1','5jVRb9','5jSRb0','5jSRb1','5jSRb9']
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
            i+=1
            f = ROOT.TFile.Open(fileName)
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
#        pprint.pprint(self.profDict_dressNom['4jSRb9']['MJ'])
        for regionName in self.regionList:
            for histType in self.histList:
                for bin in range(1,self.histDict_dressNom[regionName][histType].GetNbinsX()+1):
                    self.histDict_dressUp[regionName][histType].SetBinContent(bin,mean(self.profDict_dressUp[regionName][histType][bin-1]))
                    self.histDict_dressNom[regionName][histType].SetBinContent(bin,mean(self.profDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressDown[regionName][histType].SetBinContent(bin,mean(self.profDict_dressDown[regionName][histType][bin-1]))
                if histType is 'MJ':
                    kHist = self.histDict_kin[regionName][histType]
                    dHist = self.histDict_dressNom[regionName][histType]
                    #kinematic hist has already been scaled down
                    norm = kHist.Integral(kHist.FindBin(self.normRegion[0]),kHist.FindBin(self.normRegion[1])-1)/self.lumi
                    norm /= dHist.Integral(dHist.FindBin(self.normRegion[0]),dHist.FindBin(self.normRegion[1])-1)
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
    #     for name in self.regionList:
    #         for bin in range(1,self.histDict[name].GetNbinsX()+1):
    #             self.histDict[name].SetBinContent(bin,mean(self.profileDict[name][bin-1]))
    #         self.normDict[name] = (self.obsDict[name].Integral(self.obsDict[name].FindBin(self.normRegion[0]),self.obsDict[name].FindBin(self.normRegion[1]))) / (self.histDict[name].Integral(self.histDict[name].FindBin(self.normRegion[0]),self.histDict[name].FindBin(self.normRegion[1]))) 
    #         self.histDict[name].Scale(self.normDict[name])  
    # def calcErrors(self):
    #     for name in self.regionList:
    #         for bin in range(1,self.histDict[name].GetNbinsX()+1):
    #             self.histDict[name].SetBinError(bin,std(self.profileDict[name][bin-1]))
