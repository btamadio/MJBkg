#!/bin/bash
kinematicFile=$1
templateFile=$2
jobName=$3
templateType=$4
jobNum=$5

mkdir -p ../output_dressed/${jobName}
shopt -s expand_aliases
source /common/atlas/scripts/setupATLAS.sh
setupATLAS
lsetup root
../RunDresser ${kinematicFile} ${templateFile} ${jobName} ${templateType} ${jobNum}
echo "Job complete!"