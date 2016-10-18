#!/usr/bin/env python
import os,argparse
parser = argparse.ArgumentParser(add_help=False, description='make templates')
parser.add_argument('inFile')
parser.add_argument('jobName')
parser.add_argument('templateType')
args = parser.parse_args()

for i in range(0,1000):
    cmd = 'qsub run_template_job.sh '+args.inFile+' '+args.jobName+' '+args.templateType+' '+str(i)
#    print cmd
    os.system(cmd)
