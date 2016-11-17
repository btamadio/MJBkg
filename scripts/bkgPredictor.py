#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys
from controlDict import controlDict
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
    return math.sqrt(std)
class bkgPredictor:
    def __init__(self,dressedFileNames,jobName,lumi=35,templateType=0):
        self.dressedFileNames = dressedFileNames
        self.nToys = len(self.dressedFileNames)
        self.jobName = jobName
        self.lumi = lumi
        self.MJcut = 0.8
        self.templateType = templateType
        self.MJbins = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.40,0.45,0.5,0.6,0.8,1.0,2.0]
        self.nMJbins = len(self.MJbins)-1
        self.MJbinArray = array.array('d',self.MJbins)
        self.nMassBins = 20
        self.massBinLow = 0.0
        self.massBinUp = 2.0
        self.normRegion = (0.2,0.6)
        self.setupOutput()
        #self.loopAndFill()
    def setupOutput(self):
        outFileName = '../output_prediction/'+self.jobName+'.root'
        if os.path.isfile(outFileName):
            self.outFile = ROOT.TFile.Open(outFileName,'RECREATE')
        else:
            self.outFile = ROOT.TFile.Open(outFileName,'CREATE')
        self.regionList = ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM','3js0','3js1','3js2',
                           '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM','4js0','4js1',
                           '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
                           '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
                           '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM','5j',
                           '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM']
        self.histList   = ['jetmass','jetmass1','jetmass2','jetmass3','jetmass4','MJ']
        #The histograms are accessed by calling histDict[regionName][histType]
        #For example, to get the kinematic leading jet mass histogram for jets in the region 4jSRb1:
        #histDict_kin['4jSRb1']['jetmass1']
        self.histDict_kin = {}
        self.histDict_dressUp = {}
        self.histDict_dressNom = {}
        self.histDict_dressDown = {}
        #this is the same as histDict_dressNom, only the errors reflect MC statistical uncertainty.
        self.histDict_dressNom_MCstat = {}
        #These are the lists of bin contents for all toys
        self.listDict_dressNom = {}
        self.listDict_dressUp = {}
        self.listDict_dressDown = {}
        #List of sumw2 for each bin for all toys
        self.sumw2Dict = {}
        
        
        #profile histograms for response plots
        self.prof1Dict_kin = {}
        self.prof1Dict_cen_kin = {}
        self.prof1Dict_for_kin = {}
        self.prof1Dict_dress = {}
        self.prof1Dict_cen_dress = {}
        self.prof1Dict_for_dress = {}
        #list of signal region yields, for calculating stat. uncertainty
        self.srYield_listDict = {}
        self.srYield_histDict = {}
        
        for regionName in self.regionList:
            self.srYield_listDict[regionName] = []
            self.histDict_kin[regionName] = {}
            self.histDict_dressUp[regionName] = {}
            self.histDict_dressNom[regionName] = {}
            self.histDict_dressDown[regionName] = {}
            self.histDict_dressNom_MCstat[regionName] = {}
            self.listDict_dressUp[regionName] = {}
            self.listDict_dressNom[regionName] = {}
            self.listDict_dressDown[regionName] = {}
            self.sumw2Dict[regionName] = {}

            for histType in self.histList:
                self.listDict_dressUp[regionName][histType] = []
                self.listDict_dressNom[regionName][histType] = []
                self.listDict_dressDown[regionName][histType] = []
                self.sumw2Dict[regionName][histType] = []
                histName_kin = 'h_'+histType+'_kin_'+regionName
                histName_dressUp = 'h_'+histType+'_dressUp_'+regionName
                histName_dressNom = 'h_'+histType+'_dressNom_'+regionName
                histName_dressDown = 'h_'+histType+'_dressDown_'+regionName
                if histType is 'MJ':
                    for i in range(self.nMJbins):
                        self.listDict_dressUp[regionName][histType].append([])
                        self.listDict_dressNom[regionName][histType].append([])
                        self.listDict_dressDown[regionName][histType].append([])
                        self.sumw2Dict[regionName][histType].append([])
#                        self.histDict_kin[regionName][histType] = f.Get(histName).Clone()
                    self.histDict_dressUp[regionName][histType] = ROOT.TH1F(histName_dressUp,histName_dressUp,self.nMJbins,self.MJbinArray)
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMJbins,self.MJbinArray)
                    self.histDict_dressDown[regionName][histType] = ROOT.TH1F(histName_dressDown,histName_dressDown,self.nMJbins,self.MJbinArray)
                    self.histDict_dressNom_MCstat[regionName][histType] = ROOT.TH1F(histName_dressNom+'_MCstat',histName_dressNom+'_MCstat',self.nMJbins,self.MJbinArray)
                else:
                    #For individual jet mass plots, binning depends on pT order
                    xUp = 1.2
                    if histType is 'jetmass3':
                        xUp = 0.6
                    elif histType is 'jetmass4':
                        xUp = 0.4
                    for i in range(self.nMassBins):
                        self.listDict_dressUp[regionName][histType].append([])
                        self.listDict_dressNom[regionName][histType].append([])
                        self.listDict_dressDown[regionName][histType].append([])
                        self.sumw2Dict[regionName][histType].append([])
                    self.histDict_dressUp[regionName][histType] = ROOT.TH1F(histName_dressUp,histName_dressUp,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressDown[regionName][histType] = ROOT.TH1F(histName_dressDown,histName_dressDown,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressNom_MCstat[regionName][histType] = ROOT.TH1F(histName_dressNom+'_MCstat',histName_dressNom+'_MCstat',self.nMassBins,self.massBinLow,xUp)

    def getResponse(self):
        f=ROOT.TFile.Open(self.dressedFileNames[0])
        for regionName in self.regionList:
            self.prof1Dict_kin[regionName] = f.Get('h_prof1d_kin_'+regionName)

            self.prof1Dict_cen_kin[regionName] = f.Get('h_prof1d_cen_kin_'+regionName)
            self.prof1Dict_for_kin[regionName] = f.Get('h_prof1d_for_kin_'+regionName)

            self.prof1Dict_dress[regionName] = f.Get('h_prof1d_dress_'+regionName)
            self.prof1Dict_cen_dress[regionName] = f.Get('h_prof1d_cen_dress_'+regionName)
            self.prof1Dict_for_dress[regionName] = f.Get('h_prof1d_for_dress_'+regionName)

            self.prof1Dict_kin[regionName].SetDirectory(0)
            self.prof1Dict_cen_kin[regionName].SetDirectory(0)
            self.prof1Dict_for_kin[regionName].SetDirectory(0)
            self.prof1Dict_dress[regionName].SetDirectory(0)
            self.prof1Dict_cen_dress[regionName].SetDirectory(0)
            self.prof1Dict_for_dress[regionName].SetDirectory(0)

        for i in range(1,len(self.dressedFileNames)):
            fi = ROOT.TFile.Open(self.dressedFileNames[i])
            for regionName in self.regionList:
                self.prof1Dict_dress[regionName].Add(fi.Get('h_prof1d_dress_'+regionName))
                self.prof1Dict_cen_dress[regionName].Add(fi.Get('h_prof1d_cen_dress_'+regionName))
                self.prof1Dict_for_dress[regionName].Add(fi.Get('h_prof1d_for_dress_'+regionName))
        self.outFile.cd()
        for regionName in self.regionList:
            self.prof1Dict_kin[regionName].Write()
            self.prof1Dict_cen_kin[regionName].Write()
            self.prof1Dict_for_kin[regionName].Write()
            self.prof1Dict_dress[regionName].Write()
            self.prof1Dict_cen_dress[regionName].Write()
            self.prof1Dict_for_dress[regionName].Write()

            
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
                    else:
                        h_dressUp.Rebin(10)
                        h_dressNom.Rebin(10)
                        h_dressDown.Rebin(10)
                    for bin in range(1,h_dressNom.GetNbinsX()+1):
                        self.listDict_dressUp[regionName][histType][bin-1].append(h_dressUp.GetBinContent(bin))
                        self.listDict_dressNom[regionName][histType][bin-1].append(h_dressNom.GetBinContent(bin))
                        self.listDict_dressDown[regionName][histType][bin-1].append(h_dressDown.GetBinContent(bin))
                        self.sumw2Dict[regionName][histType][bin-1].append(h_dressNom.GetBinError(bin))
                    if histType == 'MJ':
                        self.srYield_listDict[regionName].append(h_dressNom.Integral(h_dressNom.FindBin(self.MJcut),h_dressNom.FindBin(h_dressNom.GetNbinsX())+1))
        for regionName in self.regionList:
            for histType in self.histList:
                for bin in range(1,self.histDict_dressNom[regionName][histType].GetNbinsX()+1):
                    self.histDict_dressUp[regionName][histType].SetBinContent(bin,mean(self.listDict_dressUp[regionName][histType][bin-1]))
                    self.histDict_dressNom[regionName][histType].SetBinContent(bin,mean(self.listDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressDown[regionName][histType].SetBinContent(bin,mean(self.listDict_dressDown[regionName][histType][bin-1]))
                    self.histDict_dressNom_MCstat[regionName][histType].SetBinContent(bin,mean(self.listDict_dressNom[regionName][histType][bin-1]))

                    self.histDict_dressUp[regionName][histType].SetBinError(bin,err(self.listDict_dressUp[regionName][histType][bin-1]))
                    self.histDict_dressNom[regionName][histType].SetBinError(bin,err(self.listDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressDown[regionName][histType].SetBinError(bin,err(self.listDict_dressDown[regionName][histType][bin-1]))
                    self.histDict_dressNom_MCstat[regionName][histType].SetBinError(bin,mean(self.sumw2Dict[regionName][histType][bin-1]))

                if histType is 'MJ':
                    kHist = self.histDict_kin[regionName][histType]
                    dHist = self.histDict_dressNom[regionName][histType]
                    #kinematic hist has already been scaled down
                    norm = kHist.Integral(kHist.FindBin(self.normRegion[0]),kHist.FindBin(self.normRegion[1])-1)/self.lumi
                    denom = dHist.Integral(dHist.FindBin(self.normRegion[0]),dHist.FindBin(self.normRegion[1])-1)
                    if denom != 0:
                        norm /= denom
                    print 'regionName = %s, norm = %f' % (regionName,norm)
                    cen = mean(self.srYield_listDict[regionName])
                    
                    xMin = norm*self.lumi*(cen-3*err(self.srYield_listDict[regionName]))
                    xMax = norm*self.lumi*(cen+3*err(self.srYield_listDict[regionName]))
                    self.srYield_histDict[regionName] = ROOT.TH1F('h_srYield_'+regionName,'signal yield',20,xMin,xMax)
                    for entry in self.srYield_listDict[regionName]:
                        self.srYield_histDict[regionName].Fill(entry*norm*self.lumi)
                    self.histDict_dressUp[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressNom[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressDown[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressNom_MCstat[regionName][histType].Scale(norm*self.lumi)
                else:
                    self.histDict_dressUp[regionName][histType].Scale(self.lumi)
                    self.histDict_dressNom[regionName][histType].Scale(self.lumi)
                    self.histDict_dressDown[regionName][histType].Scale(self.lumi)
                    self.histDict_dressNom_MCstat[regionName][histType].Scale(self.lumi)
                self.outFile.cd()
                self.histDict_dressUp[regionName][histType].Write()
                self.histDict_dressNom[regionName][histType].Write()
                self.histDict_dressDown[regionName][histType].Write()
                self.histDict_dressNom_MCstat[regionName][histType].Write()
            self.srYield_histDict[regionName].Write()
