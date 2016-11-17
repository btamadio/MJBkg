#!/usr/bin/env python
import argparse,ROOT,os,math,glob
parser = argparse.ArgumentParser(add_help=False, description='make plots')
parser.add_argument('inDir')
args = parser.parse_args()
inFileList = [ROOT.TFile.Open(fileName) for fileName in glob.glob(args.inDir+'/*')]
eventNum = 271150
