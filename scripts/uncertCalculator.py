#!/usr/bin/env python
import ROOT,math
class uncertCalculator:
    def __init__(self,inFileName):
        self.inFile = ROOT.TFile.Open(inFileName)
        self.etaList = ['eta1','eta2','eta3','eta4']
        self.regionList = ['4js1VRb9bU','4js1VRb9bM']
        self.hKin = {}
        self.hDress = {}
        self.kinProf = {}
        self.dressProf = {}
        self.kinErr = {}
        self.corrections = {}
        self.errors = {}
    def mean(self,lst):
        if len(lst) < 1:
            return 0
        return sum(lst) / float(len(lst))
    def std(self,lst):
        if len(lst) < 2:
            return 0
        xbar = 1.0
        std = 0.0
        for entry in lst:
            std += (entry-xbar)*(entry-xbar)
        std /= float(len(lst)-1)
        return math.sqrt(std)
    def calcUncert(self):
        for eta in self.etaList:
            for region in self.regionList:
                key = eta+'_'+region
                self.hKin[key] = self.inFile.Get('h_avgMass_'+eta+'_kin_'+region)
                self.hDress[key] = self.inFile.Get('h_avgMass_'+eta+'_dress_'+region)
                self.kinProf[key] = []
                self.dressProf[key] = []
                self.kinErr[key]=[]
                for bin in range(1,self.hKin[key].GetNbinsX()+1):
                    self.kinProf[key].append(self.hKin[key].GetBinContent(bin))
                    self.kinErr[key].append(self.hKin[key].GetBinError(bin))
                    self.dressProf[key].append(self.hDress[key].GetBinContent(bin))
        uncertList = []
        for region in self.regionList:
            for eta in self.etaList:
                key = eta+'_'+region
                self.corrections[key] = []
                self.errors[key] = []
                for i in range(len(self.dressProf[key])):
#                    corr = self.dressProf[key][i]/self.kinProf[key][i]
                    corr = self.kinProf[key][i]/self.dressProf[key][i]
                    err = self.kinErr[key][i]/self.dressProf[key][i]
                    self.corrections[key].append(corr)
                    self.errors[key].append(err)
                uncertList.append(self.std(self.corrections[key]))
        return( tuple(uncertList))
