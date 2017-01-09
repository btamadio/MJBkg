#!/usr/bin/env python
import os
dsids = range(403605,403615)
count = 0
for dsid in dsids:
    cmd = './submitTemplateJobs.py ../../bkgEstimation/samples/SignalInjection_RPV6/main_SignalInjection_RPV6.root '
    cmd += 'SignalInjection_dataICHEP_'+str(dsid)
    cmd += ' 0 '
    cmd += ' 14.8 '
    cmd += str(dsid)
    if not dsid in [403605,403607,403609,403611]:
        os.system(cmd)
        count+=100
print count,'jobs submitted'
