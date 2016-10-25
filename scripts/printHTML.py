#!/usr/bin/env python
variables = ['MJ','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
regions =   ['4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
             '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
             '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbU',
             '5jSRb0','5jSRb1','5jSRb9','5jVRbM','5jSRbM']
jobNames = ['data_eta','data_bdt','data_ichep']
date = '10_21'
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of template methods </H2> 
<TABLE border=3> 
"""
for var in variables:
    for region in regions:
        if var is 'MJ' and ('bM' in region or 'bU' in region):
            continue
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
