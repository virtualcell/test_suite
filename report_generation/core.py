from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
import os
import subprocess

download_sbml()
print("Strating to generate SED-ML")
gen_sedml()
print("SED-ML generation finished")
omex = GenOmex()
omex.omex_gen_copasi()
omex.omex_gen_vcell()


list_files = subprocess.run(["./report_generation/run_script/run_copasi_sim.sh"])
print("The exit code was: %d" % list_files.returncode)
list_files = subprocess.run(["./report_generation/run_script/run_vcell_sim.sh"])
print("The exit code was: %d" % list_files.returncode)
