#!/usr/bin/env python
import argparse,ROOT,os,sys
parser = argparse.ArgumentParser(add_help=False, description='compare event counts')
parser.add_argument('input1')
parser.add_argument('input2')
args = parser.parse_args()
cutflow1 = {}
cutflow2 = {}
file1 = ROOT.TFile.Open(args.input1)
file2 = ROOT.TFile.Open(args.input2)
tree1 = file1.Get('miniTree')
tree2 = file2.Get('miniTree')
nEntries = tree1.GetEntries()
print 'File 1 has %i entries'%nEntries
for entry in range(nEntries):
    if entry % 10000 == 0:
        print 'Processing entry %i'%entry
    tree1.GetEntry(entry)
    dsid = tree1.runNumber
    if dsid in cutflow1:
        cutflow1[dsid]+=1
    else:
        cutflow1[dsid]=1
nEntries = tree2.GetEntries()
print 'File 2 has %i entries'%nEntries
for entry in range(nEntries):
    tree2.GetEntry(entry)
    dsid=tree2.runNumber
    if dsid in cutflow2:
        cutflow2[dsid]+=1
    else:
        cutflow2[dsid]=1
for dsid in sorted(cutflow2):
    print dsid,cutflow1[dsid],cutflow2[dsid],cutflow2[dsid]-cutflow1[dsid]
