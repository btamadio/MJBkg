#!/usr/bin/env python
import ROOT,sys,math,os,pprint
from controlDict import controlDict
class templateMaker:
    def __init__(self,inFileName,jobName,templateType,jobNum,nSplit=1000):
        self.nBins = 50
        self.xMin = -7
        self.xMax = 0
        self.jobName = jobName
        self.jobNum = jobNum
        self.templateType = templateType
        self.outDir = '../output_templates/'+self.jobName+'/'
        self.ptBins3 = controlDict[templateType]['ptBins3']
        self.ptBins4 = controlDict[templateType]['ptBins4']
        self.ptBins5 = controlDict[templateType]['ptBins5']
        self.yBins = controlDict[templateType]['yBins'] #this is either eta or BDT score, depending on template type
        self.inFile = ROOT.TFile.Open(inFileName)
        if not self.inFile:
            print 'File not found %s. Exiting' % inFileName
            sys.exit(1)
        self.miniTree = self.inFile.Get('miniTree')
        if not self.miniTree:
            print 'miniTree not found in file %s. Exiting.' % inFileName
            sys.exit(1)
        nEntries = self.miniTree.GetEntries()
        k =math.ceil(float(nEntries)/float(nSplit))
        self.eventStart = int(k*int(jobNum))
        self.eventEnd = int(min(nEntries,(int(jobNum)+1)*k))
        if self.eventStart >= nEntries:
            print 'No remainining entries. Exiting.'
            sys.exit(1)
        print 'ptBins3 = ',self.ptBins3
        print 'ptBins4 = ',self.ptBins4
        print 'ptBins5 = ',self.ptBins5
        print 'yBins   = ',self.yBins
        print 'nEntries = %i' % nEntries
        print 'eventStart = %i ' % self.eventStart
        print 'eventEnd = %i ' % self.eventEnd
    def setupOutput(self):
        os.system('mkdir -p '+self.outDir)
        outFileName = self.outDir+'output_'+str(self.jobNum)+'.root'
        self.outFile = ROOT.TFile.Open(outFileName,'RECREATE')
        print 'output file: ',outFileName
        self.histDict = {}
        if self.templateType == 0:
            #pt/eta/b-match binning
            for i in range(len(self.ptBins3)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b0_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_b1_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
        elif self.templateType == 1:
            #pt/bdt/b-match binning
            for i in range(len(self.ptBins3)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b0_ptBin'+str(i+1)+'_bdtBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_b1_ptBin'+str(i+1)+'_bdtBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
        elif self.templateType == 2:
            #ICHEP binning
            for i in range(len(self.ptBins3)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b0_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet3'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_b1_ptBin'+str(i+1)+'_bdtBin'+str(j+1)+'_njet3'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
            for i in range(len(self.ptBins4)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b0_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet4'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_b1_ptBin'+str(i+1)+'_bdtBin'+str(j+1)+'_njet4'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
            for i in range(len(self.ptBins5)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b9_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet5'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
        print 'Created %i template histograms' % len(self.histDict)
    def loopAndFill(self):
        for entry in range(self.eventStart,self.eventEnd):
            self.miniTree.GetEntry(entry)
            if self.miniTree.njet==3:
                #determine bin and fill appropriate histogram with log(m/pT) for that jet
                pass

t = templateMaker('../../bkgEstimation/samples/pythia_BDT_PtRatios/main_pythia_BDT_PtRatios.root','pythia_bdt',1,0)
t.setupOutput()
t.loopAndFill()
