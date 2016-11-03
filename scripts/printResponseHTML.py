#!/usr/bin/env python
regions =   ['3js0','3js1','3js2','3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
             '4js0','4js1','4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
             '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
             '5j','5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbU',
             '5jSRb0','5jSRb1','5jSRb9','5jVRbM','5jSRbM']
#jobNames = ['pythia_eta_corr','pythia_bdt_corr','pythia_ichep_corr']
#jobNames = ['data_eta_corr','data_bdt_uncorr','data_ichep_uncorr']
jobNames = ['pythia_eta','pythia_bdt','pythia_ichep','pythia_qg','pythia_nsubjet']
date = '11_03'
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of response plots </H2> 
<TABLE border=3> 
"""
for region in regions:
    output+='<TR>'
    for i in range(len(jobNames)):
        jobName = jobNames[i]
        fName = '../'+date+'_'+jobName+'/'+region+'/plot_prof1d_'+region+'_'+jobName+'.png'
        output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">link</a>)</CENTER></TD>'
    output+='</TR>'
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
