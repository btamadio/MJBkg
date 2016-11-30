#!/bin/bash
inFile=$1
jobName=$2
templateType=$3
jobNum=$4
signalLumi=$5
signalNum=$6
shopt -s expand_aliases
source /common/atlas/scripts/setupATLAS.sh
setupATLAS
lsetup root
./makeTemplates.py ${inFile} ${jobName} ${templateType} ${jobNum} ${signalLumi} ${signalNum}