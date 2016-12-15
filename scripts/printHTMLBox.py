#!/usr/bin/env python
import argparse
var = 'avgMass'
regions1 = ['4js0VR','4js0SR','4js0',
            '4js1VR','4js1SR','4js1',
            '5jVR','5jSR','5j']
regions2 = ['b9','b9bU','b9bM','b0','b1','b1bU','b1bM']
regLabelDict = {'b9':'b-inclusive',
                'b9bU':'b-inclusive, non-b-matched',
                'b9bM':'b-inclusive, b-matched',
                'b0':'b-veto',
                'b1':'b-tag',
                'b1bU':'b-tag, non-b-matched',
                'b1bM':'b-tag, b-matched'}
parser = argparse.ArgumentParser(add_help=False, description='make html')
parser.add_argument('jobName')
parser.add_argument('date')
args=parser.parse_args()
jobName = args.jobName
date = args.date
output = """<HTML>
<HEAD> </HEAD>
<BODY> 
<CENTER><H2 style="color:red"><font size="18">"""
output+=jobName
output+="""</font></H2> 
<TABLE border=3> 
"""
for reg2 in regions2:
    output+="""
<THEAD>
<TR>
<TH colspan="3"><font size = "18">"""
    output+=regLabelDict[reg2]
    output+="""</font></TH>
</TR>
"""
    output+="""<TR>
<TH><font size="18">dEta > 1.4</font></TH>
<TH><font size="18">dEta < 1.4</font></TH>
<TH><font size="18">inclusive</font></TH>
</TR></THEAD>
"""
    output+='<TR>'
    fName = '../'+date+'_'+jobName+'/'+regions1[0]+reg2+'/plot_'+var+'_'+regions1[0]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[0]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[1]+reg2+'/plot_'+var+'_'+regions1[1]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[1]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[2]+reg2+'/plot_'+var+'_'+regions1[2]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[2]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'
    
    output+='</TR>'

    output+='<TR>'
    fName = '../'+date+'_'+jobName+'/'+regions1[3]+reg2+'/plot_'+var+'_'+regions1[3]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[3]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[4]+reg2+'/plot_'+var+'_'+regions1[4]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[4]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[5]+reg2+'/plot_'+var+'_'+regions1[5]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[5]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'
    
    output+='</TR>'

    output+='<TR>'
    fName = '../'+date+'_'+jobName+'/'+regions1[6]+reg2+'/plot_'+var+'_'+regions1[6]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[6]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[7]+reg2+'/plot_'+var+'_'+regions1[7]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[7]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'

    fName = '../'+date+'_'+jobName+'/'+regions1[8]+reg2+'/plot_'+var+'_'+regions1[8]+reg2+'_'+jobName+'.png'
    label = var+'_'+regions1[8]+reg2
    output+='<TD><CENTER><img src="'+fName+'" height="800" width="800"><BR>(<a href="'+fName+'">'+label+'</a>)</CENTER></TD>'
    
    output+="""</TR>"""
output+="""
</TABLE></CENTER> 
</BODY> 
</HTML>"""

print output
