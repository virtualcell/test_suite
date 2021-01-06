import subprocess
from multiprocessing import Process
from logzero import logger
import fire
from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
from report_generation.comparator.report_comparator import ReportComparator

""" Runs all the methods

    Usage:
        NAME
        core.py - Downloads SBML files
        SYNOPSIS
            core.py START END STEP <flags>
        DESCRIPTION
            Downloads SBML files
        POSITIONAL ARGUMENTS
            START
                Start point
            END
                End point
            STEP
                Step to run the loop
        FLAGS
            --base_url=BASE_URL
                base URL https://www.ebi.ac.uk. Defaults to Config.BASE_URL.
            --headers=HEADERS
                request headers for `https://www.ebi.ac.uk`. Defaults to Config.HEADERS.
            --model_files_path=MODEL_FILES_PATH
                path for SBML model files to download. Defaults to Config.MODEL_FILES_PATH.
        NOTES
            You can also use flags syntax for POSITIONAL ARGUMENTS
"""

def run_sim(sh_path:str) -> int:
    """Runs the command

    Args:
        sh_path (str): input command

    Returns:
        int: return code for the command stdout
    """
    sim = subprocess.run([sh_path])
    return sim.returncode

if __name__ == '__main__':
    try:
        logger.debug("Download starting...")
        fire.Fire(download_sbml)
        logger.debug("Download finished...\n\n")

        logger.debug("Starting to generate SED-ML documents...")
        gen_sedml()
        logger.debug("SED-ML generation finished...\n\n")

        logger.debug("Creating OMEX archives...")
        omex = GenOmex()
        omex.gen_omex()
        logger.debug("Archive generation finished...\n\n")

        # TODO: Replace with run_docker.py
        command_list = [
            "./report_generation/run_script/run_copasi_sim.sh",
            "./report_generation/run_script/run_vcell_sim.sh"
            ]
        processes = []
        for command in command_list:
            run = Process(target=run_sim, args=[command])
            simulator = command.split('/')[3].split('_')[1]
            if simulator == 'copasi':
                logger.debug(
                    f"Running {simulator} simulations...")

            if simulator == 'vcell':
                logger.debug(
                    f"Running {simulator} simulations...")
            run.start()
            processes.append(run)
        
        for process in processes:
            process.join()

        logger.debug("Generating report...")
        ReportComparator().generate_report()
        logger.debug("Report generated...")

    except KeyboardInterrupt:
        logger.warning("Stopping with keyboard interruption...")
