#!/bin/bash
kinematicFile=$1
templateFile=$2
jobName=$3
templateType=$4
jobNum=$5
signalNum=$6
signalLumi=$7

mkdir -p ../output_dressed/${jobName}
shopt -s expand_aliases
source /common/atlas/scripts/setupATLAS.sh
setupATLAS
lsetup root
../RunDresser ${kinematicFile} ${templateFile} ${jobName} ${templateType} ${jobNum} ${signalNum} ${signalLumi}
echo "Job complete!"