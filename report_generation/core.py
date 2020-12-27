from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
from report_generation.comparator.comparator import gen_report
import subprocess

download_sbml()

print("Starting to generate SED-ML")
gen_sedml()
print("SED-ML generation finished")

omex = GenOmex()
omex.omex_gen_copasi()
omex.omex_gen_vcell()


copasi_run = subprocess.run(["./report_generation/run_script/run_copasi_sim.sh"])
print("The exit code was: %d" % copasi_run.returncode)

vcell_run = subprocess.run(
    ["./report_generation/run_script/run_vcell_sim.sh"])
print("The exit code was: %d" % vcell_run.returncode)

gen_report()
