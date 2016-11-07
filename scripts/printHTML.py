#!/usr/bin/env python
variables = ['MJ','jetmass','jetmass1','jetmass2','jetmass3','jetmass4','srYield']
regions =   ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
             '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
             '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbU',
             '5jSRb0','5jSRb1','5jSRb9','5jVRbM','5jSRbM']
jobNames = ['pythia_eta','pythia_bdt','pythia_ichep','pythia_qg','pythia_nsubjet']
date = '11_04'
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of template methods </H2> 
<TABLE border=3> 
"""
for var in variables:
    for region in regions:
        if (var is 'MJ' or var is 'srYield') and ('bM' in region or 'bU' in region):
            continue
        if var is 'jetmass4' and '3j' in region:
            continue
        output+='<TR>'
        for i in range(len(jobNames)):
            jobName = jobNames[i]
            fName = '../'+date+'_'+jobName+'/'+region+'/plot_'+var+'_'+region+'_'+jobName+'.png'
            height = '800'
            if var is 'srYield':
                height = '600'
            output+='<TD><CENTER><img src="'+fName+'" height="'+height+'" width="800"><BR>(<a href="'+fName+'">link</a>)</CENTER></TD>'
        output+='</TR>'
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
