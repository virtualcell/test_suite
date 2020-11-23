# helper functions to convert COPASI results files into the VCell .ida format

import os
import re

# COPASI results files are comma separated by default -> delimitor = ','


def cps_results_to_ida(filename, delim=",", outdir="./cps_results_ida"):
    # output file is .ida file format
    out_filename = re.search(r"(\\w*)(\.txt)", filename).group(1) + ".ida"
    out_filepath = outdir + "/" + out_filename

    infile = open(filename)
    outfile = open(out_filepath, "w")

    variables = infile.readline().strip().replace(" ", "").split(
        delim)      # remove all whitespace and split on delimitor
    for var in variables:
        if var == "time":
            var = "t"     # vcell ida files represent time by 't' whereas copasi uses 'time'
        outfile.write(var + ":")  # header line is delimited by ":"
    outfile.write("\n")

    for line in infile:
        dataline = line.strip().replace(" ", "").split(delim)
        for d in dataline:
            outfile.write(d + "\t")     # .ida files are tab delimited
        outfile.write("\n")

    infile.close()
    outfile.close()


def cps_dir_to_ida(dirpath="./cps_results"):
    for filename in os.listdir(dirpath):
        filepath = dirpath + "/" + filename
        cps_results_to_ida(filepath)
