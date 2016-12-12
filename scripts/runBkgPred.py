#!/usr/bin/env python
import ROOT,os,array,pprint, math,time,glob,sys,argparse
from bkgPredictor import bkgPredictor

parser = argparse.ArgumentParser(add_help=False, description='run bkg prediction')
parser.add_argument('fileDir')
parser.add_argument('jobName')
parser.add_argument('templateFile')
parser.add_argument('mjCut')
parser.add_argument('lumi')
parser.add_argument('templateType')
args = parser.parse_args()

filesList = sorted(glob.glob(args.fileDir+'/*'))

p = bkgPredictor(filesList,args.jobName,args.templateFile,float(args.mjCut),float(args.lumi),int(args.templateType))
p.getResponse()
p.loopAndFill()
#for i in range(len(jobNameList)):
#    print 'running job %s ' % jobNameList[i]
#    p = bkgPredictor(filesList[i],jobNameList[i],templateFileList[i],mjCutList[i],lumiList[i],templateTypeList[i])
#    p.getResponse()
#    p.loopAndFill()
# jobNameList = ['data_ICHEP_uncorrected',
#                'pythia_uncorrected',
#                'SignalInjection_dataICHEP_403566_uncorrected',
#                'data_PostICHEP_uncorrected',
#                'data_ICHEP_nsubjet',
#                'SignalInjection_dataICHEP_403566_nsubjet']
# filesList = [sorted(glob.glob('../output_dressed/data_ICHEP_uncorrected/*.root')),
#              sorted(glob.glob('../output_dressed/pythia_uncorrected/*.root')),
#              sorted(glob.glob('../output_dressed/SignalInjection_dataICHEP_403566_uncorrected/*.root')),
#              sorted(glob.glob('../output_dressed/data_PostICHEP_uncorrected/*.root')),
#              sorted(glob.glob('../output_dressed/data_ICHEP_nsubjet/*.root')),
#              sorted(glob.glob('../output_dressed/SignalInjection_dataICHEP_403566_nsubjet/*.root'))]
# templateFileList = ['../output_templates/data_ICHEP.root',
#                     '../output_templates/pythia.root',
#                     '../output_templates/SignalInjection_dataICHEP_403566.root',
#                     '../output_templates/data_PostICHEP.root',
#                     '../output_templates/data_ICHEP_nsubjet.root',
#                     '../output_templates/SignalInjection_dataICHEP_403566_nsubjet.root']
# templateTypeList = [0,0,0,0,4,4]
# lumiList = [1,36.45,1,1,1,1]
# mjCutList = [.6,.8,.6,.6,.6,.6]
