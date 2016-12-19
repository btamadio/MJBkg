#!/usr/bin/env python
import argparse,os,ROOT
parser = argparse.ArgumentParser(add_help=False, description='make master histogram for resampling')
parser.add_argument('inFile')
parser.add_argument('jobName')
args = parser.parse_args()
outDir = '../output_resampling/'
os.system('mkdir -p '+outDir)
outFileName = outDir+args.jobName+'.root'
outFile = ROOT.TFile.Open(outFileName,'RECREATE')
outHist = ROOT.TH1F('h_master','h_master',4096,-0.5,4095.5)
print 'output file: ',outFileName
ptBinDict =[[0.498,0.575,0.696],
            [0.347,0.419,0.508],
            [0.256,0.299,0.359],
            [0.213,0.232,0.266]]
etaBinDict = [0.797, 0.823, 0.854, 0.859]
def getBin(pt,eta,num):
    ptBins = ptBinDict[num]
    etaBin = etaBinDict[num]
    outStr = ''
    if pt < ptBins[0]:
        outStr = '00'
    elif pt < ptBins[1]:
        outStr = '01'
    elif pt < ptBins[2]:
        outStr = '10'
    else:
        outStr = '11'
    if abs(eta) < etaBin:
        outStr+='0'
    else:
        outStr+='1'
    return outStr
inFile = ROOT.TFile.Open(args.inFile)
t = inFile.Get('miniTree')
nEntries = t.GetEntries()

for entry in range(nEntries):
    t.GetEntry(entry)
    if entry %10000 == 0:
        print 'Processing entry %i ' % entry
    if t.njet != 4:
        continue
    binCode = ''
    for i in range(0,4):
        binCode+=getBin(t.jet_pt.at(i),t.jet_eta.at(i),i)
    outHist.Fill(int(binCode,2))
outFile.cd()
outHist.Write()
