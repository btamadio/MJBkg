#!/usr/bin/env python
import argparse,ROOT,os,math

class histMaker:
    def __init__(self,inFileName,outFileName,scaleFact,isBkg=False):
        self.inFile = ROOT.TFile.Open(inFileName)
        self.outFile = ROOT.TFile.Open(outFileName,'RECREATE')
        self.tree = self.inFile.Get('miniTree')
        self.histDict = {}
        self.lumi = 36.45
        self.scaleFact = 0.87
        self.isBkg = isBkg
    def loop(self):
        nEntries = self.tree.GetEntries()
        print 'Processing %i entries' % nEntries
        for entry in range(nEntries):
            self.tree.GetEntry(entry)
            if entry % 100000 == 0:
                print 'Processing entry %i' % entry
            if self.tree.njet < 5 or self.tree.nbjet_Fix70 < 1:
                continue
            dsid = self.tree.mcChannelNumber
            if self.isBkg:
                dsid = 1
            if not dsid in self.histDict:
                self.histDict[dsid] = ROOT.TH2F('hist_'+str(dsid),'hist_'+str(dsid),300,0,3,400,0,4)
            self.histDict[dsid].Fill(self.tree.MJ,self.tree.dEta,self.lumi*self.scaleFact*self.tree.weight*self.tree.bSF_70)
        self.outFile.cd()
        for dsid in sorted(self.histDict):
            self.histDict[dsid].Write()
    

parser = argparse.ArgumentParser(add_help=False, description='optimize SR')
parser.add_argument('inFile_sig')
parser.add_argument('inFile_bkg')
parser.add_argument('outFile_sig')
parser.add_argument('outFile_bkg')
args = parser.parse_args()
h_sig=histMaker(args.inFile_sig,args.outFile_sig,1)
h_sig.loop()
h_bkg=histMaker(args.inFile_bkg,args.outFile_bkg,0.87,True)
h_bkg.loop()
