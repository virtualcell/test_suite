#!/bin/bash

pwd
cd report_generation
cd files
cd omex_archives
cd vcell

for entry in `ls`
do
	 command="docker run --rm --tty  --mount type=bind,source=`pwd`,target=/root/in,readonly --mount type=bind,source=`pwd`/../../results/vcell,target=/root/out ghcr.io/biosimulators/vcell:7.3.0.07 -i /root/in/${entry} -o /root/out &> `pwd`/../../logs/vcell/`echo ${entry} | cut -c 1-15`.txt"
	 echo "VCell simulation started for `echo ${entry} | cut -c 1-15`"
	 eval $command;
done