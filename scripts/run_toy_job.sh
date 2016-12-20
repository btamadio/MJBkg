#!/bin/bash
masterFile=$1
jobName=$2
index=$3
shopt -s expand_aliases
source /common/atlas/scripts/setupATLAS.sh
setupATLAS
lsetup root
./makeToyTree.py ${masterFile} ${jobName} ${index}
echo "Job complete!"