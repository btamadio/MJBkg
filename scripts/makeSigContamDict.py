#!/usr/bin/env python
import argparse,ROOT,os,math,pprint
parser = argparse.ArgumentParser(add_help=False, description='make signal contamination plots')
parser.add_argument('inFile')
args = parser.parse_args()
lumi = 35
mjCut = 0.8
bDict = {'4jVRb0':(128.5),
         '4jVRb1':(46.5),
         '4jSRb0':(299.1),
         '4jSRb1':(104.3),
         '5jVRb0':(7.5),
         '5jVRb1':(3.0),
         '5jSRb0':(16.4),
         '5jSRb1':(7.6)}
yieldDict = {}
f = ROOT.TFile.Open(args.inFile)
t = f.Get('miniTree')
nEntries = t.GetEntries()

for entry in range(nEntries):
#    if entry % 10000 == 0:
#        print 'processing entry %i' % entry
    t.GetEntry(entry)
    dsid = t.mcChannelNumber
    if not dsid in yieldDict:
        yieldDict[dsid] = {'4jVRb0':0.0,
                           '4jVRb1':0.0,
                           '4jSRb0':0.0,
                           '4jSRb1':0.0,
                           '5jVRb0':0.0,
                           '5jVRb1':0.0,
                           '5jSRb0':0.0,
                           '5jSRb1':0.0}
    if t.MJ < mjCut:
        continue
    if t.njet == 4:
        if t.dEta > 1.0:
            if t.nbjet_Fix70 == 0:
                yieldDict[dsid]['4jVRb0'] += t.weight*lumi / math.sqrt(bDict['4jVRb0'])
            else:
                yieldDict[dsid]['4jVRb1'] += t.weight*t.bSF_70*lumi / math.sqrt(bDict['4jVRb1'])
        else:
            if t.nbjet_Fix70 == 0:
                yieldDict[dsid]['4jSRb0'] += t.weight*lumi / math.sqrt(bDict['4jSRb0'])
            else:
                yieldDict[dsid]['4jSRb1'] += t.weight*t.bSF_70*lumi /  math.sqrt(bDict['4jSRb1'])
    elif t.njet >= 5:
        if t.dEta > 1.0:
            if t.nbjet_Fix70 == 0:
                yieldDict[dsid]['5jVRb0'] += t.weight*lumi / math.sqrt(bDict['5jVRb0'])
            else:
                yieldDict[dsid]['5jVRb1'] += t.weight*t.bSF_70*lumi / math.sqrt(bDict['5jVRb1'])
        else:
            if t.nbjet_Fix70 == 0:
                yieldDict[dsid]['5jSRb0'] += t.weight*lumi / math.sqrt(bDict['5jSRb0'])
            else:
                yieldDict[dsid]['5jSRb1'] += t.weight*t.bSF_70*lumi / math.sqrt(bDict['5jSRb1'])
pprint.pprint(yieldDict)
