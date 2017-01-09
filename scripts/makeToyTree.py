#!/usr/bin/env python
import argparse,os,ROOT
from array import array
parser = argparse.ArgumentParser(add_help=False, description='make toy tree from master histogram')
parser.add_argument('inFile')
parser.add_argument('jobName')
parser.add_argument('jobNum')
args = parser.parse_args()
inFile = ROOT.TFile.Open(args.inFile)
outDir = '../output_resampling/'+args.jobName
os.system('mkdir -p '+outDir)
outFile = ROOT.TFile.Open(outDir+'/toyTree_'+str(args.jobNum)+'.root','RECREATE')
ptBinDict =[[0.44,0.498,0.575,0.696,2.0],
            [0.2,0.347,0.419,0.508,1.5],
            [0.2,0.256,0.8],
            [0.2,0.213,0.6]]
etaBinDict = [0.797, 0.823, 0.854, 0.859]
h_master = inFile.Get('h_master')
get_binary = lambda x, n: format(int(x),'b').zfill(n)
outTree = ROOT.TTree('miniTree','miniTree')
b_runNumber = array('i',[0])
b_mcChannelNumber = array('i',[0])
b_eventNumber=array('l',[0])
b_lumiBlock = array('i',[0])
b_mu=array('d',[0])
b_isMC = array('b',[0])
b_weight = array('d',[1])
b_njet = array('i',[4])
b_njet_soft = array('i',[0])
b_njet_ak4=array('i',[0])
b_nbjet_Fix60 = array('i',[0])
b_nbjet_Fix70 = array('i',[0])
b_nbjet_Fix77 = array('i',[0])
b_nbjet_Fix85 = array('i',[0])
b_nbjet_Flt60 = array('i',[0])
b_nbjet_Flt70 = array('i',[0])
b_nbjet_Flt77 = array('i',[0])
b_nbjet_Flt85 = array('i',[0])
b_jet_pt = ROOT.vector('double')()
b_jet_eta = ROOT.vector('double')()
b_jet_phi = ROOT.vector('double')()
b_jet_m = ROOT.vector('double')()
b_jet_bmatched_Fix60 = ROOT.vector('int')()
b_jet_bmatched_Fix70 = ROOT.vector('int')()
b_jet_bmatched_Fix77 = ROOT.vector('int')()
b_jet_bmatched_Fix85 = ROOT.vector('int')()
b_jet_bmatched_Flt60 = ROOT.vector('int')()
b_jet_bmatched_Flt70 = ROOT.vector('int')()
b_jet_bmatched_Flt77 = ROOT.vector('int')()
b_jet_bmatched_Flt85 = ROOT.vector('int')()
b_jet_NTrimSubjets = ROOT.vector('int')()
b_jet_qmatched = ROOT.vector('int')()
b_jet_gmatched = ROOT.vector('int')()
b_dEta = array('d',[0])
b_HT = array('d',[0])
b_MJ = array('d',[0])
b_MJ4 = array('d',[0])
bSF_60 = array('d',[1])
bSF_70 = array('d',[1])
bSF_77 = array('d',[1])
bSF_85 = array('d',[1])
outTree.Branch('runNumber',b_runNumber,'runNumber/I')
outTree.Branch('mcChannelNumber',b_mcChannelNumber,'mcChannelNumber/I')
outTree.Branch('eventNumber',b_eventNumber,'eventNumber/L')
outTree.Branch('lumiBlock',b_lumiBlock,'lumiBlock/I')
outTree.Branch('mu',b_mu,'mu/D')
outTree.Branch('isMC',b_isMC,'isMC/O')
outTree.Branch('weight',b_weight,'weight/D')
outTree.Branch('njet',b_njet,'njet/I')
outTree.Branch('njet_soft',b_njet_soft,'njet_soft/I')
outTree.Branch('njet_ak4',b_njet_ak4,'njet_ak4/I')
outTree.Branch('nbjet_Fix60',b_nbjet_Fix60,'nbjet_Fix60/I')
outTree.Branch('nbjet_Fix70',b_nbjet_Fix70,'nbjet_Fix70/I')
outTree.Branch('nbjet_Fix77',b_nbjet_Fix77,'nbjet_Fix77/I')
outTree.Branch('nbjet_Fix85',b_nbjet_Fix85,'nbjet_Fix85/I')
outTree.Branch('nbjet_Flt60',b_nbjet_Flt60,'nbjet_Fix60/I')
outTree.Branch('nbjet_Flt70',b_nbjet_Flt70,'nbjet_Fix70/I')
outTree.Branch('nbjet_Flt77',b_nbjet_Flt77,'nbjet_Fix77/I')
outTree.Branch('nbjet_Flt85',b_nbjet_Flt85,'nbjet_Fix85/I')
outTree.Branch('jet_pt',b_jet_pt)
outTree.Branch('jet_eta',b_jet_eta)
outTree.Branch('jet_phi',b_jet_phi)
outTree.Branch('jet_m',b_jet_m)
outTree.Branch('jet_bmatched_Fix60',b_jet_bmatched_Fix60)
outTree.Branch('jet_bmatched_Fix70',b_jet_bmatched_Fix70)
outTree.Branch('jet_bmatched_Fix77',b_jet_bmatched_Fix77)
outTree.Branch('jet_bmatched_Fix85',b_jet_bmatched_Fix85)
outTree.Branch('jet_bmatched_Flt60',b_jet_bmatched_Flt60)
outTree.Branch('jet_bmatched_Flt70',b_jet_bmatched_Flt70)
outTree.Branch('jet_bmatched_Flt77',b_jet_bmatched_Flt77)
outTree.Branch('jet_bmatched_Flt85',b_jet_bmatched_Flt85)
outTree.Branch('jet_NTrimSubjets',b_jet_NTrimSubjets)
outTree.Branch('jet_qmatched',b_jet_qmatched)
outTree.Branch('jet_gmatched',b_jet_gmatched)
outTree.Branch('dEta',b_dEta,'dEta/D')
outTree.Branch('HT',b_HT,'HT/D')
outTree.Branch('MJ',b_MJ,'MJ/D')
outTree.Branch('MJ4',b_MJ4,'MJ4/D')
outTree.Branch('bSF_60',bSF_60,'bSF_60/D')
outTree.Branch('bSF_70',bSF_70,'bSF_70/D')
outTree.Branch('bSF_77',bSF_77,'bSF_77/D')
outTree.Branch('bSF_85',bSF_85,'bSF_85/D')

rndm = ROOT.TRandom3(0)
totEvents = 0
totEventsRndm = 0
def getPt(binStr,jetNum):
    bin = int(binStr[3*jetNum:3*jetNum+2],2)
    if bin < len(ptBinDict[jetNum]) - 2:
        ptLow = ptBinDict[jetNum][bin]
        ptUp = ptBinDict[jetNum][bin+1]
        return rndm.Uniform(ptLow,ptUp)
    else:
        funcStr = 'exp(-5.96*x)'
        if jetNum==1:
            funcStr = 'exp(-3.8*x)'
        elif jetNum==2:
            funcStr = 'exp(-4.8*x)'
        elif jetNum==3:
            funcStr = 'exp(-9.3*x)'
        f0 = ROOT.TF1('f0',funcStr,ptBinDict[jetNum][bin],10)
        return f0.GetRandom()
def getEta(binStr,jetNum):
    bin = int(binStr[3*jetNum+2],2)
    if bin == 0:
        #first eta bin, always uniform distribution
        etaLow = 0.0
        etaUp = etaBinDict[jetNum]
        return rndm.Uniform(etaLow,etaUp)
    elif bin == 1:
        #second eta bin, use line
        lineStr = '-1739*x+4978'
        if jetNum > 2:
            lineStr = '-1304*x+4608'
        f2 = ROOT.TF1('f2',lineStr,etaBinDict[jetNum],2)
        return f2.GetRandom()
def getJetPts(binStr):
    counter = 0
    while True:
        counter+=1
        pt = [getPt(binStr,i) for i in range(4)]
        if pt[0] > pt[1] and pt[1] > pt[2] and pt[2] > pt[3]:
            return pt
        if counter > 999:
            print 'Warning: all 1000 sets of pt rejected'
            return [999,999,999,999]
entry = 0
for i in range(0,h_master.GetNbinsX()):
    binStr = get_binary(i,12)
    binCont = h_master.GetBinContent(i+1)
    nEvents = rndm.Poisson(binCont)
    for j in range(0,nEvents):
        entry+=1
        if entry % 1000 == 0:
            print 'Generating pseudo-event number %i' % entry
        b_jet_pt.clear()
        b_jet_eta.clear()
        b_jet_phi.clear()
        b_jet_m.clear()
        b_jet_bmatched_Fix60.clear()
        b_jet_bmatched_Fix70.clear()
        b_jet_bmatched_Fix77.clear()
        b_jet_bmatched_Fix85.clear()
        b_jet_bmatched_Flt60.clear()
        b_jet_bmatched_Flt70.clear()
        b_jet_bmatched_Flt77.clear()
        b_jet_bmatched_Flt85.clear()
        b_jet_NTrimSubjets.clear()
        b_jet_qmatched.clear()
        b_jet_gmatched.clear()
        jetPtList = getJetPts(binStr)
        for jetNum in range(0,4):
            b_jet_pt.push_back(jetPtList[jetNum])
            b_jet_eta.push_back(getEta(binStr,jetNum))
            b_jet_phi.push_back(0)
            b_jet_m.push_back(0)
            b_jet_bmatched_Fix60.push_back(0)
            b_jet_bmatched_Fix70.push_back(0)
            b_jet_bmatched_Fix77.push_back(0)
            b_jet_bmatched_Fix85.push_back(0)
            b_jet_bmatched_Flt60.push_back(0)
            b_jet_bmatched_Flt70.push_back(0)
            b_jet_bmatched_Flt77.push_back(0)
            b_jet_bmatched_Flt85.push_back(0)
            b_jet_NTrimSubjets.push_back(0)
            b_jet_qmatched.push_back(0)
            b_jet_gmatched.push_back(0)
        outTree.Fill()
outFile.cd()
outTree.Write()

