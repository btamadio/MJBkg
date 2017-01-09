#!/usr/bin/env python
import glob,sys#,argparse
from bkgPredictor import bkgPredictor

# parser = argparse.ArgumentParser(add_help=False, description='run bkg prediction')
# parser.add_argument('fileDir')
# parser.add_argument('jobName')
# parser.add_argument('templateFile')
# parser.add_argument('mjCut')
# parser.add_argument('lumi')
# parser.add_argument('templateType')
# args = parser.parse_args()

#filesList = sorted(glob.glob(args.fileDir+'/*'))
# p = bkgPredictor(filesList,args.jobName,args.templateFile,float(args.mjCut),float(args.lumi),int(args.templateType))
# p.getResponse()
# p.loopAndFill()

filesList = sorted(glob.glob(sys.argv[1]+'/*'))
jobName = sys.argv[2]
templateFile = sys.argv[3]
mjCut = float(sys.argv[4])
lumi = float(sys.argv[5])
templateType = int(sys.argv[6])

p = bkgPredictor(filesList,jobName,templateFile,mjCut,lumi,templateType)
#TODO: uncomment
p.getResponse()
p.loopAndFill()

