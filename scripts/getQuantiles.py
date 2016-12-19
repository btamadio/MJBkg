#!/usr/bin/env python
import argparse,ROOT,os,math,glob,pprint,array
parser = argparse.ArgumentParser(add_help=False, description='get correction factors and uncertainties')
parser.add_argument('inFileName')
args = parser.parse_args()
f=ROOT.TFile.Open(args.inFileName)
t=f.Get('miniTree')

h0 = ROOT.TH1F('h0','h0',1000,0.44,2.5)
h1 = ROOT.TH1F('h1','h1',1000,.2,2.5)
h2 = ROOT.TH1F('h2','h2',1000,.2,1.5)
h3 = ROOT.TH1F('h3','h3',1000,.2,1.5)

e0 = ROOT.TH1F('e0','e0',1000,0.0,2.0)
e1 = ROOT.TH1F('e1','e1',1000,0.0,2.0)
e2 = ROOT.TH1F('e2','e2',1000,0.0,2.0)
e3 = ROOT.TH1F('e3','e3',1000,0.0,2.0)

t.Draw('jet_pt[0]>>h0','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_pt[1]>>h1','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_pt[2]>>h2','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_pt[3]>>h3','njet == 4 && nbjet_Fix70 == 0','goff')

t.Draw('jet_eta[0]>>e0','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_eta[1]>>e1','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_eta[2]>>e2','njet == 4 && nbjet_Fix70 == 0','goff')
t.Draw('jet_eta[3]>>e3','njet == 4 && nbjet_Fix70 == 0','goff')

q0 = array.array('d',[0,0,0,0,0])
q1 = array.array('d',[0,0,0,0,0])
q2 = array.array('d',[0,0,0,0,0])
q3 = array.array('d',[0,0,0,0,0])

qe0 = array.array('d',[0,0,0,0,0])
qe1 = array.array('d',[0,0,0,0,0])
qe2 = array.array('d',[0,0,0,0,0])
qe3 = array.array('d',[0,0,0,0,0])

probs = array.array('d',[0,0.25,0.5,0.75,1.0])
eprobs = array.array('d',[0,0.5,1.0])

h0.GetQuantiles(5,q0,probs)
h1.GetQuantiles(5,q1,probs)
h2.GetQuantiles(5,q2,probs)
h3.GetQuantiles(5,q3,probs)

e0.GetQuantiles(3,qe0,eprobs)
e1.GetQuantiles(3,qe1,eprobs)
e2.GetQuantiles(3,qe2,eprobs)
e3.GetQuantiles(3,qe3,eprobs)



print q0
print q1
print q2
print q3

print qe0
print qe1
print qe2
print qe3
