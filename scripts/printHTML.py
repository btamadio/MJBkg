#!/usr/bin/env python
variables = ['MJ','avgMass','avgMass_eta1','avgMass_eta2','avgMass_eta3','avgMass_eta4','srYield','jetmass','jetmass1','jetmass2','jetmass3','jetmass4']
eventRegionList = ['3jb0','3jb1','3jb9',
                   '3js0b0','3js0b1','3js0b9',
                   '3js1b0','3js1b1','3js1b9',
                   '3jVRb0','3jVRb1','3jVRb9',
                   '3js0VRb0','3js0VRb1','3js0VRb9',
                   '3js1VRb0','3js1VRb1','3js1VRb9',
                   '3jSRb0','3jSRb1','3jSRb9',
                   '3js0SRb0','3js0SRb1','3js0SRb9',
                   '3js1SRb0','3js1SRb1','3js1SRb9',

                   '4jb0','4jb1','4jb9',
                   '4js0b0','4js0b1','4js0b9',
                   '4js1b0','4js1b1','4js1b9',
                   '4jVRb0','4jVRb1','4jVRb9',
                   '4js0VRb0','4js0VRb1','4js0VRb9',
                   '4js1VRb0','4js1VRb1','4js1VRb9',
                   '4jSRb0','4jSRb1','4jSRb9',
                   '4js0SRb0','4js0SRb1','4js0SRb9',
                   '4js1SRb0','4js1SRb1','4js1SRb9',

                   '5jb0','5jb1','5jb9',
                   '5js0b0','5js0b1','5js0b9',
                   '5js1b0','5js1b1','5js1b9',
                   '5jVRb0','5jVRb1','5jVRb9',
                   '5js0VRb0','5js0VRb1','5js0VRb9',
                   '5js1VRb0','5js1VRb1','5js1VRb9',
                   '5jSRb0','5jSRb1','5jSRb9',
                   '5js0SRb0','5js0SRb1','5js0SRb9',
                   '5js1SRb0','5js1SRb1','5js1SRb9']
jetRegionList = []
for region in eventRegionList:
    jetRegionList.append(region)
    jetRegionList.append(region+'bU')
    jetRegionList.append(region+'bM')
jobNames = ['data_ICHEP_withUncert']
dates=['12_15']

output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red">Comparison of template methods </H2> 
<TABLE border=3> 
"""
for var in variables:
    for region in jetRegionList:
        if (var is 'MJ' or var is 'srYield') and ('bM' in region or 'bU' in region):
            continue
        if var is 'jetmass4' and '3j' in region:
            continue
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
