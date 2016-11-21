#!/usr/bin/env python
variables = ['prof1d_cen','prof1d_for','MJ','srYield','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
regions =   ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
             '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
             '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
             '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbU',
             '5jSRb0','5jSRb1','5jSRb9','5jVRbM','5jSRbM']
jobNames = ['data_ICHEP','data_ICHEP']
dates = ['11_17','11_18']
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Pre-correction and Post-correction plots </H2> 
<TABLE border=3> 
"""
for var in variables:
    for region in regions:
        output+='<TR>'
        if (var is 'MJ' or var is 'srYield') and ('bM' in region or 'bU' in region):
            continue
        if var is 'jetmass4' and '3j' in region:
            continue
        for i in range(len(jobNames)):
            jobName = jobNames[i]
            fName = '../'+dates[i]+'_'+jobName+'/'+region+'/plot_'+var+'_'+region+'_'+jobName+'.png'
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
