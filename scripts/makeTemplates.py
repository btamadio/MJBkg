#!/usr/bin/env python
import argparse
from templateMaker import templateMaker
parser = argparse.ArgumentParser(add_help=False, description='make templates')
parser.add_argument('inFile')
parser.add_argument('jobName')
parser.add_argument('templateType')
parser.add_argument('jobNum')
args = parser.parse_args()
t = templateMaker(args.inFile,args.jobName,int(args.templateType),int(args.jobNum))
t.setupOutput()
t.loopAndFill()
print 'Done processing job number %i' % int(args.jobNum)
