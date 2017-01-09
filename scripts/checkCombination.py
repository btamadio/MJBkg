#!/usr/bin/env python
import glob,ROOT
fileList = glob.glob('../output_dressed/combined_pythia_herwig/*.root')
for fileName in fileList:
    f = ROOT.TFile.Open(fileName)
    num = fileName.split('_')[-1].split('.')[0]
    h = f.Get('h_MJ_kin_5jSRb1')
    print num,h.Integral()
