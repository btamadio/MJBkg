#!/usr/bin/env python
import argparse,ROOT,os,math
from pointDict import pointDict
class optimizer:
    def __init__(self,inFileSig,inFileBkg,outFile):
        self.sigFile = ROOT.TFile.Open(inFileSig)
        self.bkgFile = ROOT.TFile.Open(inFileBkg)
        self.outFile = ROOT.TFile.Open(outFile,'RECREATE')
        self.significancePlots = {}
        self.h_sig = {}
        self.minMJ = 0.25
        self.maxMJ = 1.0
        self.minDeta = 0.2
        self.maxDeta = 2.5
        self.mjHist = ROOT.TH2F('h_mj','h_mj',13,650,1950,9,-50,1750)
        self.dEtaHist = ROOT.TH2F('h_dEta','h_dEta',13,650,1950,9,-50,1750)
        for dsid in pointDict:
            if dsid > 403604:
                continue
            print 'processing dsid %i'%dsid
            self.makeSignificancePlot(dsid)
            self.outFile.cd()
            self.significancePlots[dsid].Write()
            (mj,dEta) = self.getOptimalCuts(dsid)
            mG = pointDict[dsid][0]
            mX = pointDict[dsid][1]
            xBin = self.mjHist.GetXaxis().FindBin(mG)
            yBin = self.mjHist.GetYaxis().FindBin(mX)
            self.mjHist.SetBinContent(xBin,yBin,mj)
            self.dEtaHist.SetBinContent(xBin,yBin,dEta)
        self.mjHist.Write()
        self.dEtaHist.Write()
    def makeSignificancePlot(self,dsid):
        self.h_sig[dsid] = self.sigFile.Get('hist_'+str(dsid))
        self.h_bkg = self.bkgFile.Get('hist_1')
        if dsid in self.significancePlots:
            print 'Significance plot already made for dsid %i'% dsid
        nBinsX = (self.maxMJ - self.minMJ) * 20 + 1
        nBinsY = (self.maxDeta - self.minDeta) * 10 + 1
        self.significancePlots[dsid] = ROOT.TH2F('h_sig_'+str(dsid),
                                                 'h_sig_'+str(dsid),
                                                 int(nBinsX),
                                                 self.minMJ-.025,
                                                 self.maxMJ+.025,
                                                 int(nBinsY),
                                                 self.minDeta-.05,
                                                 self.maxDeta+.05)
        for mj in range(int(self.minMJ*100),int(self.maxMJ*100),5):
            mj /= 100.
            for dEta in range(int(self.minDeta*10),int(self.maxDeta*10)):
                dEta /= 10.
                xBin1 = self.h_bkg.GetXaxis().FindBin(mj)
                xBin2 = self.h_bkg.GetNbinsX()+1
                yBin1 = 1
                yBin2 = self.h_bkg.GetYaxis().FindBin(dEta)-1
                n_sig = self.h_sig[dsid].Integral(xBin1,xBin2,yBin1,yBin2)
                n_bkg = self.h_bkg.Integral(xBin1,xBin2,yBin1,yBin2)
                signi = math.sqrt(2*((n_sig+n_bkg)*math.log(1+n_sig/n_bkg)-n_sig))
                fillBinX = self.significancePlots[dsid].GetXaxis().FindBin(mj)
                fillBinY = self.significancePlots[dsid].GetYaxis().FindBin(dEta)
#                print mj,dEta,fillBinX,fillBinY#n_sig,n_bkg,signi
                self.significancePlots[dsid].SetBinContent(fillBinX,fillBinY,signi)
    def getOptimalCuts(self,dsid):
        xBinMax = ROOT.Long(0)
        yBinMax = ROOT.Long(0)
        zBinMax = ROOT.Long(0)
        self.significancePlots[dsid].GetMaximumBin(xBinMax,yBinMax,zBinMax)
        mj = self.significancePlots[dsid].GetXaxis().GetBinCenter(xBinMax)
        dEta = self.significancePlots[dsid].GetYaxis().GetBinCenter(yBinMax)
        return(mj,dEta)
parser = argparse.ArgumentParser(add_help=False, description='optimize SR')
parser.add_argument('inFile_sig')
parser.add_argument('inFile_bkg')
parser.add_argument('outFile')
args = parser.parse_args()
optim = optimizer(args.inFile_sig,args.inFile_bkg,args.outFile)
###optim.makeSignificancePlot(403594)
