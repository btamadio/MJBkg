#!/usr/bin/env python
variables = ['MJ','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
regions =   ['4jVRb0','4jVRb1','4jVRb9','4jSRb0','4jSRb1','4jSRb9',
             '5jVRb0','5jVRb1','5jVRb9','5jSRb0','5jSRb1','5jSRb9']
jobNames = ['pythia_eta_delta05','pythia_bdt_delta05','pythia_ichep_delta05']
date = '10_19'
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of template methods </H2> 
<TABLE border=3> 
"""
for var in variables:
    for region in regions:
        output+='<TR>'
        for jobName in jobNames:
            fName = '../'+date+'_'+jobName+'/'+region+'/plot_'+var+'_SR_cut_800gev_'+region+'_'+jobName+'.png'
            output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">link</a>)</CENTER></TD>'
        output+='</TR>'
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
