from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
from report_generation.comparator.report_comparator import ReportComparator
import subprocess
from logzero import logger

""" Runs all the methods 
"""

try:
    logger.debug("Download starting...")
    # TODO: Make this configuration acceptable from command line interface
    download_sbml(1000, 0, -1)
    logger.debug("Download finished...\n\n")

    logger.debug("Starting to generate SED-ML documents...")
    gen_sedml()
    logger.debug("SED-ML generation finished...\n\n")

    logger.debug("Creating OMEX archives...")
    omex = GenOmex()
    omex.gen_omex()
    logger.debug("Archive generation finished...\n\n")

    # TODO: Replace with run_docker.py
    logger.debug("Running COPASI simulations...")
    copasi_run = subprocess.run(
        ["./report_generation/run_script/run_copasi_sim.sh"])
    logger.info("The exit code was: %d" % copasi_run.returncode)
    logger.debug("COPASI simulations finished...\n\n")

    logger.debug("Running VCell simulations...")
    vcell_run = subprocess.run(
        ["./report_generation/run_script/run_vcell_sim.sh"])
    logger.info("The exit code was: %d" % vcell_run.returncode)
    logger.debug("VCell simulations finished...\n\n")

    logger.debug("Generating report...")
    ReportComparator().generate_report()
    logger.debug("Report generated...")

except KeyboardInterrupt:
    logger.warning("Stopping with keyboard interruption...")
