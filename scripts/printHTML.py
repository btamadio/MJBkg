#!/usr/bin/env python
#variables = ['MJ','avgMass','avgMass_eta1','avgMass_eta2','avgMass_eta3','avgMass_eta4','srYield','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
#variables = ['MJ','avgMass','avgMass_cen','avgMass_for','srYield','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
variables = ['MJ','prof1d','prof1d_cen','prof1d_for','srYield','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
regions =   ['3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '3jSRb0','3jSRb1','3jSRb9','3jSRbU','3jSRbM',
             '3js0','3js1','3js2',
             '3jVRb0','3jVRb1','3jVRb9','3jVRbU','3jVRbM',
             '4jVRb0','4jVRb1','4jVRb9','4jVRbU','4jVRbM',
             '4jSRb0','4jSRb1','4jSRb9','4jSRbU','4jSRbM',
             '4js0','4js1',
             '5jVRb0','5jVRb1','5jVRb9','5jVRbU','5jVRbM',
             '5jSRb0','5jSRb1','5jSRb9','5jSRbU','5jSRbM',
             '5j']
jobNames = ['pythia_ichep']
dates=['11_14']

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
#        if 'avgMass' in var:
#            if region in ['5j','5jbU','5jbM','5jSRb0','5jSRb1','5jSRb9']:
#                continue
        output+='<TR>'
        for i in range(len(jobNames)):
            jobName = jobNames[i]
            fName = '../'+dates[i]+'_'+jobName+'/'+region+'/plot_'+var+'_'+region+'_'+jobName+'.png'
            height = '800'
            if var is 'srYield':
                height = '600'
            label = var+'_'+region
            output+='<TD><CENTER><img src="'+fName+'" height="'+height+'" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'
        output+='</TR>'
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
