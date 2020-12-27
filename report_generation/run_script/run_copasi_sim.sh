#!/bin/bash
pwd
cd report_generation
cd files
cd omex_archives
cd copasi

for entry in `ls`
do
	 command="docker run --rm --tty  --mount type=bind,source=`pwd`,target=/root/in,readonly --mount type=bind,source=`pwd`/../../results/copasi,target=/root/out ghcr.io/biosimulators/copasi@sha256:dea16b66bdd5b80d0638729377e1e11377f8b6f6211a146701d8b90ed285c316 -i /root/in/${entry} -o /root/out &> `pwd`/../../logs/copasi/`echo ${entry} | cut -c 1-15`.txt"
	 echo "COPASI simulation started for `echo ${entry} | cut -c 1-15`"
	 eval $command;
done