import subprocess
from multiprocessing import Process
from logzero import logger
from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
from report_generation.comparator.report_comparator import ReportComparator

""" Runs all the methods 
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
        # TODO: Make this configuration acceptable from command line interface
        download_sbml(10, 0, -1)
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
            if command.split('/')[3].split('_')[1] == 'copasi':
                logger.debug(
                    f"Running {command.split('/')[3].split('_')[1]} simulations...")

            if command.split('/')[3].split('_')[1] == 'vcell':
                logger.debug(
                    f"Running {command.split('/')[3].split('_')[1]} simulations...")
            run.start()
            processes.append(run)
        
        for process in processes:
            process.join()

        logger.debug("Generating report...")
        ReportComparator().generate_report()
        logger.debug("Report generated...")

    except KeyboardInterrupt:
        logger.warning("Stopping with keyboard interruption...")
