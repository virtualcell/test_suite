from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
from report_generation.comparator.comparator import gen_report
import subprocess
from logzero import logger

logger.debug("Download starting...")
download_sbml()
logger.debug("Download finished...\n\n")

logger.debug("Starting to generate SED-ML documents...")
gen_sedml()
logger.debug("SED-ML generation finished...\n\n")

logger.debug("Creating OMEX archives...")
omex = GenOmex()
omex.omex_gen_copasi()
omex.omex_gen_vcell()
logger.debug("Archive generation finished...\n\n")


logger.debug("Running COPASI simulations...")
copasi_run = subprocess.run(["./report_generation/run_script/run_copasi_sim.sh"])
logger.info("The exit code was: %d" % copasi_run.returncode)
logger.debug("COPASI simulations finished...\n\n")


logger.debug("Running VCell simulations...")
vcell_run = subprocess.run(
    ["./report_generation/run_script/run_vcell_sim.sh"])
logger.info("The exit code was: %d" % vcell_run.returncode)
logger.debug("VCell simulations finished...\n\n")

logger.debug("Generating report...")
gen_report()
logger.debug("Report generated...")
