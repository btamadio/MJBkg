#!/bin/bash
fileDir=$1
jobName=$2
templateFile=$3
mjCut=$4
lumi=$5
templateType=$6
#shopt -s expand_aliases
#source /common/atlas/scripts/setupATLAS.sh
#setupATLAS
lsetup root
#lsetup python
python runBkgPred.py ${fileDir} ${jobName} ${templateFile} ${mjCut} ${lumi} ${templateType}
