#!/usr/bin/env python
regionsVR =   ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
               '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
               '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM']
regionsSR =  ['3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
              '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
              '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM']
date = '10_27'
jobName = 'pythia_compare'
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of response plots </H2> 
<TABLE border=3> 
"""
for i in range(len(regionsVR)):
    output+='<TR>'
    fName = '../'+date+'_'+jobName+'/prof1d_w_ratios_'+regionsVR[i]+'.png'
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">link</a>)</CENTER></TD>'
    fName = '../'+date+'_'+jobName+'/prof1d_w_ratios_'+regionsSR[i]+'.png'
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">link</a>)</CENTER></TD>'
    output+='</TR>'
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
