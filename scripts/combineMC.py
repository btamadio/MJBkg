#!/usr/bin/env python
import os
for i in range(0,100):
    cmd = 'hadd ../output_dressed/combined_pythia_herwig/combined_pythia_herwig_'+str(i)+'.root '
    cmd += '../output_dressed/pythia_scaleHalf/pythia_scaleHalf_'+str(i)+'.root '
    cmd += '../output_dressed/herwig_scaleHalf/herwig_scaleHalf_'+str(i)+'.root'
    os.system(cmd)
