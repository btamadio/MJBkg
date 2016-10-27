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
                    histName = 'templ_b1_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet3'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
            for i in range(len(self.ptBins4)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b0_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet4'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_b1_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet4'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
            for i in range(len(self.ptBins5)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_b9_ptBin'+str(i+1)+'_etaBin'+str(j+1)+'_njet5'
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
        elif self.templateType == 3:
            #pt/eta/q/g-match binning
            for i in range(len(self.ptBins3)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_q1_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_g1_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
        elif self.templateType == 4:
            #pt/eta/n_subjet
            for i in range(len(self.ptBins3)-1):
                for j in range(len(self.yBins)-1):
                    histName = 'templ_n1_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)
                    histName = 'templ_n2_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)        
                    histName = 'templ_n3_ptBin'+str(i+1)+'_etaBin'+str(j+1)
                    self.histDict[histName]=ROOT.TH1F(histName,histName,self.nBins,self.xMin,self.xMax)        
        print 'Created %i template histograms' % len(self.histDict)
    def loopAndFill(self):
        for entry in range(self.eventStart,self.eventEnd):
            self.miniTree.GetEntry(entry)
            if self.miniTree.njet==3:
                #determine bin and fill appropriate histogram with log(m/pT) for that jet
                for i in range(3):
                    histName = self.getHistName(self.miniTree.jet_pt.at(i),self.miniTree.jet_eta.at(i),self.miniTree.jet_bmatched_Fix70.at(i),self.miniTree.jet_qmatched.at(i),self.miniTree.jet_gmatched.at(i),self.miniTree.jet_NTrimSubjets.at(i),self.miniTree.BDTG,self.miniTree.njet_soft,self.miniTree.nbjet_Fix70,self.miniTree.dEta)
                    if self.miniTree.jet_m.at(i) <= 0:
                        print 'Warning: jet mass = %f' % self.miniTree.jet_m.at(i)
                        continue
                    if histName in self.histDict:
                        if '_b9_' in histName:
                            self.histDict[histName].Fill(math.log(self.miniTree.jet_m.at(i)/self.miniTree.jet_pt.at(i)),self.miniTree.weight)
                        else:
                            self.histDict[histName].Fill(math.log(self.miniTree.jet_m.at(i)/self.miniTree.jet_pt.at(i)),self.miniTree.weight*self.miniTree.bSF_70)
                    elif histName is not '':
                        print 'Error: histogram %s not found.' % histName
#                        pprint.pprint(self.histDict)
                        sys.exit(1)
        self.outFile.Write()
    def getHistName(self,pt,eta,bMatch,qMatch,gMatch,nSubjets,BDT,njet_soft,nbjet,dEta):
        if self.templateType == 0:
            #pT/eta/b-match binning
            ptBin = -1
            etaBin = -1
            if pt >= self.ptBins3[-1]:
                ptBin = len(self.ptBins3)-1
            for i in range(len(self.ptBins3)-1):
                if pt >= self.ptBins3[i] and pt < self.ptBins3[i+1]:
                    ptBin = i+1
                    break
            for i in range(len(self.yBins)-1):
                if abs(eta) >= self.yBins[i] and abs(eta) < self.yBins[i+1]:
                    etaBin = i+1
                    break
            #print 'pt = %f, ptBin = %i, |eta| = %f, etaBin = %i' % (pt,ptBin,abs(eta),etaBin) 
            histName = 'templ_b'+str(int(bMatch))+'_ptBin'+str(ptBin)+'_etaBin'+str(etaBin)
            if ptBin == -1: 
                print 'Error: pT bin not found!'
                print 'pT =',pt,'pT bins:',self.ptBins3
                sys.exit(1)
            if etaBin == -1:
                print 'Error: eta bin not found!'
                print 'eta =',eta,'eta bins:',self.yBins
                sys.exit(1)
            return histName
        elif self.templateType == 1:
            #pT/BDT/b-match binning
            ptBin = -1
            bdtBin = -1
            if pt >= self.ptBins3[-1]:
                ptBin = len(self.ptBins3)-1
            for i in range(len(self.ptBins3)-1):
                if pt >= self.ptBins3[i] and pt < self.ptBins3[i+1]:
                    ptBin = i+1
                    break
            for i in range(len(self.yBins)-1):
                if BDT >= self.yBins[i] and BDT < self.yBins[i+1]:
                    bdtBin = i+1
                    break
            histName = 'templ_b'+str(int(bMatch))+'_ptBin'+str(ptBin)+'_bdtBin'+str(bdtBin)
            if ptBin == -1: 
                print 'Error: pT bin not found!'
                print 'pT =',pt,'pT bins:',self.ptBins3
                sys.exit(1)
            if bdtBin == -1:
                print 'Error: BDT bin not found!'
                print 'BDT =',BDT,'BDT bins:',self.yBins
                sys.exit(1)
            #print 'pt = %f, ptBin = %i, BDTG = %f, bdtBin = %i, histName = %s' % (pt,ptBin,BDT,bdtBin,histName)             
            return histName
        elif self.templateType == 2:
            #pT/eta/b-tag/njet_soft binning
            ptBin = -1
            etaBin = -1
            njet = -1
            btag = -1
            if njet_soft == 0:
                ptBins = self.ptBins3
                njet=3
                if nbjet>0:
                    btag=1
                else:
                    btag=0
            if njet_soft == 1:
                if nbjet > 0:
                    if dEta < 1.4:
                        return ''
                    btag = 1
                else:
                    btag = 0
                ptBins = self.ptBins4
                njet = 4
            if njet_soft >= 2:
                ptBins = self.ptBins5
                njet = 5
                btag = 9
            if pt > ptBins[-1]:
                ptBin = len(ptBins)-1
            for i in range(len(ptBins)-1):
                if pt >= ptBins[i] and pt < ptBins[i+1]:
                    ptBin = i+1
                    break
            for i in range(len(self.yBins)-1):
                if abs(eta) >= self.yBins[i] and abs(eta) < self.yBins[i+1]:
                    etaBin = i+1
                    break
            if ptBin == -1: 
                print 'Error: pT bin not found!'
                print 'pT =',pt,'pT bins:',ptBins
                sys.exit(1)
            if etaBin == -1:
                print 'Error: eta bin not found!'
                print 'eta =',eta,'eta bins:',self.yBins
                sys.exit(1)            
            if btag == -1:
                print 'Error: b-tag status not found!'
                print 'nbjet =',nbjet
                sys.exit(1)            
            if njet == -1:
                print 'Error: njet not found!'
                print 'njet =',njet
                sys.exit(1)            
            histName = 'templ_b'+str(btag)+'_ptBin'+str(ptBin)+'_etaBin'+str(etaBin)+'_njet'+str(njet)
            #print 'pT = %f, pT bin = %i, |eta| = %f, eta bin = %i, btag = %i, njet_soft=%i, njet=%i' % (pt,ptBin,abs(eta),etaBin,btag,njet_soft,njet)
            return histName
        elif self.templateType == 3:
            #pT/eta/qg-match binning
            ptBin = -1
            etaBin = -1
            if pt >= self.ptBins3[-1]:
                ptBin = len(self.ptBins3)-1
            for i in range(len(self.ptBins3)-1):
                if pt >= self.ptBins3[i] and pt < self.ptBins3[i+1]:
                    ptBin = i+1
                    break
            for i in range(len(self.yBins)-1):
                if abs(eta) >= self.yBins[i] and abs(eta) < self.yBins[i+1]:
                    etaBin = i+1
                    break
            #print 'pt = %f, ptBin = %i, |eta| = %f, etaBin = %i' % (pt,ptBin,abs(eta),etaBin) 
            qgMatch = ''
            if qMatch == 1:
                qgMatch = 'q'
            elif gMatch == 1:
                qgMatch = 'g'
            histName = 'templ_'+qgMatch+'1_ptBin'+str(ptBin)+'_etaBin'+str(etaBin)
            if ptBin == -1: 
                print 'Error: pT bin not found!'
                print 'pT =',pt,'pT bins:',self.ptBins3
                sys.exit(1)
            if etaBin == -1:
                print 'Error: eta bin not found!'
                print 'eta =',eta,'eta bins:',self.yBins
                sys.exit(1)
            return histName
        elif self.templateType == 4:
            #pT/eta/n_subjet
            ptBin = -1
            etaBin = -1
            if pt >= self.ptBins3[-1]:
                ptBin = len(self.ptBins3)-1
            for i in range(len(self.ptBins3)-1):
                if pt >= self.ptBins3[i] and pt < self.ptBins3[i+1]:
                    ptBin = i+1
                    break
            for i in range(len(self.yBins)-1):
                if abs(eta) >= self.yBins[i] and abs(eta) < self.yBins[i+1]:
                    etaBin = i+1
                    break
            histName = 'templ_n'+str(min(3,nSubjets))+'_ptBin'+str(ptBin)+'_etaBin'+str(etaBin)
            if ptBin == -1: 
                print 'Error: pT bin not found!'
                print 'pT =',pt,'pT bins:',self.ptBins3
                sys.exit(1)
            if etaBin == -1:
                print 'Error: eta bin not found!'
                print 'eta =',eta,'eta bins:',self.yBins
                sys.exit(1)
            return histName
