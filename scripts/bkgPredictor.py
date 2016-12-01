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
    def __init__(self,dressedFileNames,jobName,templateFileName,mjcut,lumi=35,templateType=0):
        self.templateFile = ROOT.TFile.Open(templateFileName)
        if not self.templateFile:
            print 'Template file not found %s' % templateFileName
        self.dressedFileNames = dressedFileNames
        self.nToys = len(self.dressedFileNames)
        self.jobName = jobName
        self.lumi = lumi
        self.MJcut = mjcut
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
    def setProfileErrors(self,hist,regionName,etaBin):
        if (not 'bM' in regionName) and (not 'bU' in regionName) and not ('b0' in regionName):
            for bin in range(1,hist.GetNbinsX()+1):
                hist.SetBinError(bin,1E-10)
            return
        templateName = 'templ_b'
        if 'bM' in regionName:
            templateName+='1'
        else:
            templateName+='0'
        for bin in range(1,hist.GetNbinsX()+1):
            thisTemplateName = templateName+'_ptBin'+str(bin)+'_etaBin'+str(etaBin)
            thisTemplate = self.templateFile.Get(thisTemplateName)
            binError = thisTemplate.GetRMS() / math.sqrt(thisTemplate.Integral())
            binError *= hist.GetBinContent(bin)
            hist.SetBinError(bin,binError)
    def setupOutput(self):
        outFileName = '../output_prediction/'+self.jobName+'.root'
        if os.path.isfile(outFileName):
            self.outFile = ROOT.TFile.Open(outFileName,'RECREATE')
        else:
            self.outFile = ROOT.TFile.Open(outFileName,'CREATE')
        self.regionList = ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
                           '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
                           '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
                           '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
                           '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM',
                           '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM',
                           '3js0','3js1','3js2','3js0bM','3js1bM','3js2bM','3js0bU','3js1bU','3js2bU',
                           '4js0','4js1','4js0bM','4js1bM','4js0bU','4js1bU',
                           '5j','5jbM','5jbU']
        self.histList   = ['jetmass','jetmass1','jetmass2','jetmass3','jetmass4','MJ']
        #The histograms are accessed by calling histDict[regionName][histType]
        #For example, to get the kinematic leading jet mass histogram for jets in the region 4jSRb1:
        #histDict_kin['4jSRb1']['jetmass1']
        self.histDict_kin = {}
        self.histDict_dressNom = {}
        self.histDict_dressShift_eta1_b0 = {}
        self.histDict_dressShift_eta2_b0 = {}
        self.histDict_dressShift_eta3_b0 = {}
        self.histDict_dressShift_eta4_b0 = {}
        self.histDict_dressShift_eta1_b1 = {}
        self.histDict_dressShift_eta2_b1 = {}
        self.histDict_dressShift_eta3_b1 = {}
        self.histDict_dressShift_eta4_b1 = {}

        #These are the lists of bin contents for all toys
        self.listDict_dressNom = {}
        self.listDict_dressShift_eta1_b0 = {}
        self.listDict_dressShift_eta2_b0 = {}
        self.listDict_dressShift_eta3_b0 = {}
        self.listDict_dressShift_eta4_b0 = {}

        self.listDict_dressShift_eta1_b1 = {}
        self.listDict_dressShift_eta2_b1 = {}
        self.listDict_dressShift_eta3_b1 = {}
        self.listDict_dressShift_eta4_b1 = {}

        #profile histograms for response plots
        self.prof1Dict_kin = {}
        self.prof1Dict_eta1_kin = {}
        self.prof1Dict_eta2_kin = {}
        self.prof1Dict_eta3_kin = {}
        self.prof1Dict_eta4_kin = {}

        self.prof1Dict_dress = {}
        self.prof1Dict_eta1_dress = {}
        self.prof1Dict_eta2_dress = {}
        self.prof1Dict_eta3_dress = {}
        self.prof1Dict_eta4_dress = {}

        self.prof1ListDict_kin = {}
        self.prof1ListDict_eta1_kin = {}
        self.prof1ListDict_eta2_kin = {}
        self.prof1ListDict_eta3_kin = {}
        self.prof1ListDict_eta4_kin = {}

        self.prof1ListDict_dress = {}
        self.prof1ListDict_eta1_dress = {}
        self.prof1ListDict_eta2_dress = {}
        self.prof1ListDict_eta3_dress = {}
        self.prof1ListDict_eta4_dress = {}

        #list of signal region yields, for calculating uncertainty
        self.srYieldNom_listDict = {}
        self.srYieldShift_eta1_b0_listDict = {}
        self.srYieldShift_eta2_b0_listDict = {}
        self.srYieldShift_eta3_b0_listDict = {}
        self.srYieldShift_eta4_b0_listDict = {}
        self.srYieldShift_eta1_b1_listDict = {}
        self.srYieldShift_eta2_b1_listDict = {}
        self.srYieldShift_eta3_b1_listDict = {}
        self.srYieldShift_eta4_b1_listDict = {}

        self.srYieldNom_histDict = {}
        self.srYieldShift_eta1_b0_histDict = {}
        self.srYieldShift_eta2_b0_histDict = {}
        self.srYieldShift_eta3_b0_histDict = {}
        self.srYieldShift_eta4_b0_histDict = {}
        self.srYieldShift_eta1_b1_histDict = {}
        self.srYieldShift_eta2_b1_histDict = {}
        self.srYieldShift_eta3_b1_histDict = {}
        self.srYieldShift_eta4_b1_histDict = {}

        for regionName in self.regionList:
            self.srYieldNom_listDict[regionName] = []
            self.srYieldShift_eta1_b0_listDict[regionName] = []
            self.srYieldShift_eta2_b0_listDict[regionName] = []
            self.srYieldShift_eta3_b0_listDict[regionName] = []
            self.srYieldShift_eta4_b0_listDict[regionName] = []
            self.srYieldShift_eta1_b1_listDict[regionName] = []
            self.srYieldShift_eta2_b1_listDict[regionName] = []
            self.srYieldShift_eta3_b1_listDict[regionName] = []
            self.srYieldShift_eta4_b1_listDict[regionName] = []

            self.histDict_kin[regionName] = {}

            self.histDict_dressNom[regionName] = {}
            self.histDict_dressShift_eta1_b0[regionName] = {}
            self.histDict_dressShift_eta2_b0[regionName] = {}
            self.histDict_dressShift_eta3_b0[regionName] = {}
            self.histDict_dressShift_eta4_b0[regionName] = {}
            self.histDict_dressShift_eta1_b1[regionName] = {}
            self.histDict_dressShift_eta2_b1[regionName] = {}
            self.histDict_dressShift_eta3_b1[regionName] = {}
            self.histDict_dressShift_eta4_b1[regionName] = {}

            self.listDict_dressNom[regionName] = {}
            self.listDict_dressShift_eta1_b0[regionName] = {}
            self.listDict_dressShift_eta2_b0[regionName] = {}
            self.listDict_dressShift_eta3_b0[regionName] = {}
            self.listDict_dressShift_eta4_b0[regionName] = {}
            self.listDict_dressShift_eta1_b1[regionName] = {}
            self.listDict_dressShift_eta2_b1[regionName] = {}
            self.listDict_dressShift_eta3_b1[regionName] = {}
            self.listDict_dressShift_eta4_b1[regionName] = {}

            for histType in self.histList:
                self.listDict_dressNom[regionName][histType] = []
                self.listDict_dressShift_eta1_b0[regionName][histType] = []
                self.listDict_dressShift_eta2_b0[regionName][histType] = []
                self.listDict_dressShift_eta3_b0[regionName][histType] = []
                self.listDict_dressShift_eta4_b0[regionName][histType] = []
                self.listDict_dressShift_eta1_b1[regionName][histType] = []
                self.listDict_dressShift_eta2_b1[regionName][histType] = []
                self.listDict_dressShift_eta3_b1[regionName][histType] = []
                self.listDict_dressShift_eta4_b1[regionName][histType] = []

                histName_kin = 'h_'+histType+'_kin_'+regionName
                histName_dressNom = 'h_'+histType+'_dressNom_'+regionName
                histName_dressShift_eta1_b0 = 'h_'+histType+'_dressShift_eta1_b0_'+regionName
                histName_dressShift_eta2_b0 = 'h_'+histType+'_dressShift_eta2_b0_'+regionName
                histName_dressShift_eta3_b0 = 'h_'+histType+'_dressShift_eta3_b0_'+regionName
                histName_dressShift_eta4_b0 = 'h_'+histType+'_dressShift_eta4_b0_'+regionName
                histName_dressShift_eta1_b1 = 'h_'+histType+'_dressShift_eta1_b1_'+regionName
                histName_dressShift_eta2_b1 = 'h_'+histType+'_dressShift_eta2_b1_'+regionName
                histName_dressShift_eta3_b1 = 'h_'+histType+'_dressShift_eta3_b1_'+regionName
                histName_dressShift_eta4_b1 = 'h_'+histType+'_dressShift_eta4_b1_'+regionName

                if histType is 'MJ':
                    for i in range(self.nMJbins):
                        self.listDict_dressNom[regionName][histType].append([])
                        self.listDict_dressShift_eta1_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta2_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta3_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta4_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta1_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta2_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta3_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta4_b1[regionName][histType].append([])
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta1_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta1_b0,histName_dressShift_eta1_b0,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta2_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta2_b0,histName_dressShift_eta2_b0,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta3_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta3_b0,histName_dressShift_eta3_b0,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta4_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta4_b0,histName_dressShift_eta4_b0,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta1_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta1_b1,histName_dressShift_eta1_b1,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta2_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta2_b1,histName_dressShift_eta2_b1,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta3_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta3_b1,histName_dressShift_eta3_b1,self.nMJbins,self.MJbinArray)
                    self.histDict_dressShift_eta4_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta4_b1,histName_dressShift_eta4_b1,self.nMJbins,self.MJbinArray)
                else:
                    #For individual jet mass plots, binning depends on pT order
                    xUp = 1.2
                    if histType is 'jetmass3':
                        xUp = 0.6
                    elif histType is 'jetmass4':
                        xUp = 0.4
                    for i in range(self.nMassBins):
                        self.listDict_dressNom[regionName][histType].append([])
                        self.listDict_dressShift_eta1_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta2_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta3_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta4_b0[regionName][histType].append([])
                        self.listDict_dressShift_eta1_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta2_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta3_b1[regionName][histType].append([])
                        self.listDict_dressShift_eta4_b1[regionName][histType].append([])
                    self.histDict_dressNom[regionName][histType] = ROOT.TH1F(histName_dressNom,histName_dressNom,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta1_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta1_b0,histName_dressShift_eta1_b0,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta2_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta2_b0,histName_dressShift_eta2_b0,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta3_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta3_b0,histName_dressShift_eta3_b0,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta4_b0[regionName][histType] = ROOT.TH1F(histName_dressShift_eta4_b0,histName_dressShift_eta4_b0,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta1_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta1_b1,histName_dressShift_eta1_b1,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta2_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta2_b1,histName_dressShift_eta2_b1,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta3_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta3_b1,histName_dressShift_eta3_b1,self.nMassBins,self.massBinLow,xUp)
                    self.histDict_dressShift_eta4_b1[regionName][histType] = ROOT.TH1F(histName_dressShift_eta4_b1,histName_dressShift_eta4_b1,self.nMassBins,self.massBinLow,xUp)
    def getResponse(self):
        f=ROOT.TFile.Open(self.dressedFileNames[0])
        for regionName in self.regionList:
            self.prof1ListDict_dress[regionName] = []
            self.prof1ListDict_eta1_dress[regionName] = []
            self.prof1ListDict_eta2_dress[regionName] = []
            self.prof1ListDict_eta3_dress[regionName] = []
            self.prof1ListDict_eta4_dress[regionName] = []

            self.prof1Dict_kin[regionName] = f.Get('h_prof1d_kin_'+regionName)
            self.prof1Dict_eta1_kin[regionName] = f.Get('h_prof1d_eta1_kin_'+regionName)
            self.prof1Dict_eta2_kin[regionName] = f.Get('h_prof1d_eta2_kin_'+regionName)
            self.prof1Dict_eta3_kin[regionName] = f.Get('h_prof1d_eta3_kin_'+regionName)
            self.prof1Dict_eta4_kin[regionName] = f.Get('h_prof1d_eta4_kin_'+regionName)

            h = f.Get('h_prof1d_dress_'+regionName)
            nBins = h.GetNbinsX()
            binArray = []
            for bin in range(1,nBins+1):
                binArray.append(h.GetBinLowEdge(bin))
            binArray.append(h.GetXaxis().GetBinUpEdge(bin))
            self.prof1Dict_dress[regionName] = ROOT.TH1F('h_avgMass_dress_'+regionName,'h_avgMass_dress_'+regionName,nBins,array.array('d',binArray))
            self.prof1Dict_eta1_dress[regionName] = ROOT.TH1F('h_avgMass_eta1_dress_'+regionName,'h_avgMass_eta1_dress_'+regionName,nBins,array.array('d',binArray))
            self.prof1Dict_eta2_dress[regionName] = ROOT.TH1F('h_avgMass_eta2_dress_'+regionName,'h_avgMass_eta2_dress_'+regionName,nBins,array.array('d',binArray))
            self.prof1Dict_eta3_dress[regionName] = ROOT.TH1F('h_avgMass_eta3_dress_'+regionName,'h_avgMass_eta3_dress_'+regionName,nBins,array.array('d',binArray))
            self.prof1Dict_eta4_dress[regionName] = ROOT.TH1F('h_avgMass_eta4_dress_'+regionName,'h_avgMass_eta4_dress_'+regionName,nBins,array.array('d',binArray))

            self.prof1Dict_kin[regionName].SetDirectory(0)
            self.prof1Dict_eta1_kin[regionName].SetDirectory(0)
            self.prof1Dict_eta2_kin[regionName].SetDirectory(0)
            self.prof1Dict_eta3_kin[regionName].SetDirectory(0)
            self.prof1Dict_eta4_kin[regionName].SetDirectory(0)

            self.prof1Dict_kin[regionName].SetName('h_avgMass_kin_'+regionName)
            self.prof1Dict_eta1_kin[regionName].SetName('h_avgMass_eta1_kin_'+regionName)
            self.prof1Dict_eta2_kin[regionName].SetName('h_avgMass_eta2_kin_'+regionName)
            self.prof1Dict_eta3_kin[regionName].SetName('h_avgMass_eta3_kin_'+regionName)
            self.prof1Dict_eta4_kin[regionName].SetName('h_avgMass_eta4_kin_'+regionName)

            for i in range(0,self.prof1Dict_kin[regionName].GetNbinsX()):
                self.prof1ListDict_dress[regionName].append([])
                self.prof1ListDict_eta1_dress[regionName].append([])
                self.prof1ListDict_eta2_dress[regionName].append([])
                self.prof1ListDict_eta3_dress[regionName].append([])
                self.prof1ListDict_eta4_dress[regionName].append([])
        for i in range(1,len(self.dressedFileNames)):
            fi = ROOT.TFile.Open(self.dressedFileNames[i])
            for regionName in self.regionList:
                hDress = fi.Get('h_prof1d_dress_'+regionName).Clone('hDress')
                hDress_eta1 = fi.Get('h_prof1d_eta1_dress_'+regionName).Clone('hDress_eta1')
                hDress_eta2 = fi.Get('h_prof1d_eta2_dress_'+regionName).Clone('hDress_eta2')
                hDress_eta3 = fi.Get('h_prof1d_eta3_dress_'+regionName).Clone('hDress_eta3')
                hDress_eta4 = fi.Get('h_prof1d_eta4_dress_'+regionName).Clone('hDress_eta4')
                for bin in range(1,hDress.GetNbinsX()+1):
                    self.prof1ListDict_dress[regionName][bin-1].append(hDress.GetBinContent(bin))
                    self.prof1ListDict_eta1_dress[regionName][bin-1].append(hDress_eta1.GetBinContent(bin))
                    self.prof1ListDict_eta2_dress[regionName][bin-1].append(hDress_eta2.GetBinContent(bin))
                    self.prof1ListDict_eta3_dress[regionName][bin-1].append(hDress_eta3.GetBinContent(bin))
                    self.prof1ListDict_eta4_dress[regionName][bin-1].append(hDress_eta4.GetBinContent(bin))
        for regionName in self.regionList:
            for bin in range(1,self.prof1Dict_dress[regionName].GetNbinsX()+1):
                self.prof1Dict_dress[regionName].SetBinContent(bin,mean(self.prof1ListDict_dress[regionName][bin-1]))
                self.prof1Dict_dress[regionName].SetBinError(bin,1E-12)
                self.prof1Dict_eta1_dress[regionName].SetBinContent(bin,mean(self.prof1ListDict_eta1_dress[regionName][bin-1]))
                self.prof1Dict_eta2_dress[regionName].SetBinContent(bin,mean(self.prof1ListDict_eta2_dress[regionName][bin-1]))
                self.prof1Dict_eta3_dress[regionName].SetBinContent(bin,mean(self.prof1ListDict_eta3_dress[regionName][bin-1]))
                self.prof1Dict_eta4_dress[regionName].SetBinContent(bin,mean(self.prof1ListDict_eta4_dress[regionName][bin-1]))

            self.setProfileErrors(self.prof1Dict_eta1_dress[regionName],regionName,1)
            self.setProfileErrors(self.prof1Dict_eta2_dress[regionName],regionName,2)
            self.setProfileErrors(self.prof1Dict_eta3_dress[regionName],regionName,3)
            self.setProfileErrors(self.prof1Dict_eta4_dress[regionName],regionName,4)
#                self.prof1Dict_dress[regionName].SetBinError(bin,err(self.prof1ListDict_dress[regionName][bin-1]))
#                self.prof1Dict_eta1_dress[regionName].SetBinError(bin,err(self.prof1ListDict_eta1_dress[regionName][bin-1]))
#                self.prof1Dict_eta2_dress[regionName].SetBinError(bin,err(self.prof1ListDict_eta2_dress[regionName][bin-1]))
#                self.prof1Dict_eta3_dress[regionName].SetBinError(bin,err(self.prof1ListDict_eta3_dress[regionName][bin-1]))
#                self.prof1Dict_eta4_dress[regionName].SetBinError(bin,err(self.prof1ListDict_eta4_dress[regionName][bin-1]))
        self.outFile.cd()
        for regionName in self.regionList:
            self.prof1Dict_kin[regionName].Write()
            self.prof1Dict_eta1_kin[regionName].Write()
            self.prof1Dict_eta2_kin[regionName].Write()
            self.prof1Dict_eta3_kin[regionName].Write()
            self.prof1Dict_eta4_kin[regionName].Write()
            self.prof1Dict_dress[regionName].Write()
            self.prof1Dict_eta1_dress[regionName].Write()
            self.prof1Dict_eta2_dress[regionName].Write()
            self.prof1Dict_eta3_dress[regionName].Write()
            self.prof1Dict_eta4_dress[regionName].Write()
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
            print 'processing file %s' % fileName
            f = ROOT.TFile.Open(fileName)
            if not f:
                continue
            i+=1
            for regionName in self.regionList:
                for histType in self.histList:
#                    print regionName,histType
                    h_dressNom = f.Get('h_'+histType+'_dressNom_'+regionName)
                    h_dressShift_eta1_b0 = f.Get('h_'+histType+'_dressShift_eta1_b0_'+regionName)
                    h_dressShift_eta2_b0 = f.Get('h_'+histType+'_dressShift_eta2_b0_'+regionName)
                    h_dressShift_eta3_b0 = f.Get('h_'+histType+'_dressShift_eta3_b0_'+regionName)
                    h_dressShift_eta4_b0 = f.Get('h_'+histType+'_dressShift_eta4_b0_'+regionName)
                    h_dressShift_eta1_b1 = f.Get('h_'+histType+'_dressShift_eta1_b1_'+regionName)
                    h_dressShift_eta2_b1 = f.Get('h_'+histType+'_dressShift_eta2_b1_'+regionName)
                    h_dressShift_eta3_b1 = f.Get('h_'+histType+'_dressShift_eta3_b1_'+regionName)
                    h_dressShift_eta4_b1 = f.Get('h_'+histType+'_dressShift_eta4_b1_'+regionName)
                    if histType == 'MJ':
                        h_dressNom = h_dressNom.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta1_b0 = h_dressShift_eta1_b0.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta2_b0 = h_dressShift_eta2_b0.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta3_b0 = h_dressShift_eta3_b0.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta4_b0 = h_dressShift_eta4_b0.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta1_b1 = h_dressShift_eta1_b1.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta2_b1 = h_dressShift_eta2_b1.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta3_b1 = h_dressShift_eta3_b1.Rebin(self.nMJbins,'',self.MJbinArray)
                        h_dressShift_eta4_b1 = h_dressShift_eta4_b1.Rebin(self.nMJbins,'',self.MJbinArray)
                    else:
                        h_dressNom.Rebin(10)
                        h_dressShift_eta1_b0.Rebin(10)
                        h_dressShift_eta2_b0.Rebin(10)
                        h_dressShift_eta3_b0.Rebin(10)
                        h_dressShift_eta4_b0.Rebin(10)
                        h_dressShift_eta1_b1.Rebin(10)
                        h_dressShift_eta2_b1.Rebin(10)
                        h_dressShift_eta3_b1.Rebin(10)
                        h_dressShift_eta4_b1.Rebin(10)
                    for bin in range(1,h_dressNom.GetNbinsX()+1):
                        self.listDict_dressNom[regionName][histType][bin-1].append(h_dressNom.GetBinContent(bin))
                        self.listDict_dressShift_eta1_b0[regionName][histType][bin-1].append(h_dressShift_eta1_b0.GetBinContent(bin))
                        self.listDict_dressShift_eta2_b0[regionName][histType][bin-1].append(h_dressShift_eta2_b0.GetBinContent(bin))
                        self.listDict_dressShift_eta3_b0[regionName][histType][bin-1].append(h_dressShift_eta3_b0.GetBinContent(bin))
                        self.listDict_dressShift_eta4_b0[regionName][histType][bin-1].append(h_dressShift_eta4_b0.GetBinContent(bin))
                        self.listDict_dressShift_eta1_b1[regionName][histType][bin-1].append(h_dressShift_eta1_b1.GetBinContent(bin))
                        self.listDict_dressShift_eta2_b1[regionName][histType][bin-1].append(h_dressShift_eta2_b1.GetBinContent(bin))
                        self.listDict_dressShift_eta3_b1[regionName][histType][bin-1].append(h_dressShift_eta3_b1.GetBinContent(bin))
                        self.listDict_dressShift_eta4_b1[regionName][histType][bin-1].append(h_dressShift_eta4_b1.GetBinContent(bin))
                    if histType == 'MJ':
                        self.srYieldNom_listDict[regionName].append(h_dressNom.Integral(h_dressNom.FindBin(self.MJcut),h_dressNom.GetNbinsX()+1))
                        self.srYieldShift_eta1_b0_listDict[regionName].append(h_dressShift_eta1_b0.Integral(h_dressShift_eta1_b0.FindBin(self.MJcut),h_dressShift_eta1_b0.GetNbinsX()+1))
                        self.srYieldShift_eta2_b0_listDict[regionName].append(h_dressShift_eta2_b0.Integral(h_dressShift_eta2_b0.FindBin(self.MJcut),h_dressShift_eta2_b0.GetNbinsX()+1))
                        self.srYieldShift_eta3_b0_listDict[regionName].append(h_dressShift_eta3_b0.Integral(h_dressShift_eta3_b0.FindBin(self.MJcut),h_dressShift_eta3_b0.GetNbinsX()+1))
                        self.srYieldShift_eta4_b0_listDict[regionName].append(h_dressShift_eta4_b0.Integral(h_dressShift_eta4_b0.FindBin(self.MJcut),h_dressShift_eta4_b0.GetNbinsX()+1))
                        self.srYieldShift_eta1_b1_listDict[regionName].append(h_dressShift_eta1_b1.Integral(h_dressShift_eta1_b1.FindBin(self.MJcut),h_dressShift_eta1_b1.GetNbinsX()+1))
                        self.srYieldShift_eta2_b1_listDict[regionName].append(h_dressShift_eta2_b1.Integral(h_dressShift_eta2_b1.FindBin(self.MJcut),h_dressShift_eta2_b1.GetNbinsX()+1))
                        self.srYieldShift_eta3_b1_listDict[regionName].append(h_dressShift_eta3_b1.Integral(h_dressShift_eta3_b1.FindBin(self.MJcut),h_dressShift_eta3_b1.GetNbinsX()+1))
                        self.srYieldShift_eta4_b1_listDict[regionName].append(h_dressShift_eta4_b1.Integral(h_dressShift_eta4_b1.FindBin(self.MJcut),h_dressShift_eta4_b1.GetNbinsX()+1))

        for regionName in self.regionList:
            for histType in self.histList:
                for bin in range(1,self.histDict_dressNom[regionName][histType].GetNbinsX()+1):
                    self.histDict_dressNom[regionName][histType].SetBinContent(bin,mean(self.listDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta1_b0[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta1_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta2_b0[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta2_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta3_b0[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta3_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta4_b0[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta4_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta1_b1[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta1_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta2_b1[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta2_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta3_b1[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta3_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta4_b1[regionName][histType].SetBinContent(bin,mean(self.listDict_dressShift_eta4_b1[regionName][histType][bin-1]))

                    self.histDict_dressNom[regionName][histType].SetBinError(bin,err(self.listDict_dressNom[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta1_b0[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta1_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta2_b0[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta2_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta3_b0[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta3_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta4_b0[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta4_b0[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta1_b1[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta1_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta2_b1[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta2_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta3_b1[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta3_b1[regionName][histType][bin-1]))
                    self.histDict_dressShift_eta4_b1[regionName][histType].SetBinError(bin,err(self.listDict_dressShift_eta4_b1[regionName][histType][bin-1]))
                if histType is 'MJ':
                    kHist = self.histDict_kin[regionName][histType]
                    dHist = self.histDict_dressNom[regionName][histType]
                    #kinematic hist has already been scaled down
                    norm = kHist.Integral(kHist.FindBin(self.normRegion[0]),kHist.FindBin(self.normRegion[1])-1)/self.lumi
                    denom = dHist.Integral(dHist.FindBin(self.normRegion[0]),dHist.FindBin(self.normRegion[1])-1)
                    if denom != 0:
                        norm /= denom
                    else:
                        norm = 0
                    print 'regionName = %s, norm = %f' % (regionName,norm)
                    cen = mean(self.srYieldNom_listDict[regionName])
                    xMin = norm*self.lumi*(cen-10*err(self.srYieldNom_listDict[regionName]))
                    xMax = norm*self.lumi*(cen+10*err(self.srYieldNom_listDict[regionName]))
                    self.srYieldNom_histDict[regionName] = ROOT.TH1F('h_srYieldNom_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta1_b0_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta1_b0_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta2_b0_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta2_b0_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta3_b0_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta3_b0_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta4_b0_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta4_b0_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta1_b1_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta1_b1_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta2_b1_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta2_b1_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta3_b1_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta3_b1_'+regionName,'signal yield',20,xMin,xMax)
                    self.srYieldShift_eta4_b1_histDict[regionName] = ROOT.TH1F('h_srYieldShift_eta4_b1_'+regionName,'signal yield',20,xMin,xMax)
                    for i in range(len(self.srYieldNom_listDict[regionName])):
                        self.srYieldNom_histDict[regionName].Fill(self.srYieldNom_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta1_b0_histDict[regionName].Fill(self.srYieldShift_eta1_b0_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta2_b0_histDict[regionName].Fill(self.srYieldShift_eta2_b0_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta3_b0_histDict[regionName].Fill(self.srYieldShift_eta3_b0_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta4_b0_histDict[regionName].Fill(self.srYieldShift_eta4_b0_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta1_b1_histDict[regionName].Fill(self.srYieldShift_eta1_b1_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta2_b1_histDict[regionName].Fill(self.srYieldShift_eta2_b1_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta3_b1_histDict[regionName].Fill(self.srYieldShift_eta3_b1_listDict[regionName][i]*norm*self.lumi)
                        self.srYieldShift_eta4_b1_histDict[regionName].Fill(self.srYieldShift_eta4_b1_listDict[regionName][i]*norm*self.lumi)
                    self.histDict_dressNom[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta1_b0[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta2_b0[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta3_b0[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta4_b0[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta1_b1[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta2_b1[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta3_b1[regionName][histType].Scale(norm*self.lumi)
                    self.histDict_dressShift_eta4_b1[regionName][histType].Scale(norm*self.lumi)
                else:
                    self.histDict_dressNom[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta1_b0[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta2_b0[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta3_b0[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta4_b0[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta1_b1[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta2_b1[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta3_b1[regionName][histType].Scale(self.lumi)
                    self.histDict_dressShift_eta4_b1[regionName][histType].Scale(self.lumi)
                self.outFile.cd()
                self.histDict_dressNom[regionName][histType].Write()
                self.histDict_dressShift_eta1_b0[regionName][histType].Write()
                self.histDict_dressShift_eta2_b0[regionName][histType].Write()
                self.histDict_dressShift_eta3_b0[regionName][histType].Write()
                self.histDict_dressShift_eta4_b0[regionName][histType].Write()
                self.histDict_dressShift_eta1_b1[regionName][histType].Write()
                self.histDict_dressShift_eta2_b1[regionName][histType].Write()
                self.histDict_dressShift_eta3_b1[regionName][histType].Write()
                self.histDict_dressShift_eta4_b1[regionName][histType].Write()
            self.srYieldNom_histDict[regionName].Write()
            self.srYieldShift_eta1_b0_histDict[regionName].Write()
            self.srYieldShift_eta2_b0_histDict[regionName].Write()
            self.srYieldShift_eta3_b0_histDict[regionName].Write()
            self.srYieldShift_eta4_b0_histDict[regionName].Write()
            self.srYieldShift_eta1_b1_histDict[regionName].Write()
            self.srYieldShift_eta2_b1_histDict[regionName].Write()
            self.srYieldShift_eta3_b1_histDict[regionName].Write()
            self.srYieldShift_eta4_b1_histDict[regionName].Write()
