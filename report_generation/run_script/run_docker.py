import os
import shlex
import time
import subprocess
import logzero
from logzero import logger
from report_generation.config import Config
import report_generation.combine.files_list as fl


def run_docker(image, version, in_dir, out_dir, omex_file):
    """[summary]

    Args:
        image ([type]): [description]
        version ([type]): [description]
        in_dir ([type]): [description]
        out_dir ([type]): [description]
        omex_file ([type]): [description]
    """
    if version.startswith("sha256"):
        command_line = f"docker run --tty --rm -v {in_dir}:/root/in \
            -v {out_dir}:/root/out {image}@{version} \
            -i /root/in/{omex_file} -o /root/out"
    else:
        command_line = f"docker run --tty --rm -v {in_dir}:/root/in \
                -v {out_dir}:/root/out {image}:{version} \
                -i /root/in/{omex_file} -o /root/out"
    
    command_line_args = shlex.split(command_line)
    run = subprocess.Popen(
        command_line_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def check_io():
        """[summary]
        """
        while True:
            
            output = run.stdout.read().decode()
            # output = run.stdout.readline().decode()
            simulator_name = image.split('/')[-1]
            if output:
                logger.info(
                    f"Simulation running for {omex_file} with {simulator_name} BioSimulator")
                logger.info(output)
                logzero.logfile(f'{simulator_name}_log.log')
                # print(output)
                time.sleep(1)
            else:
                break
    
    while run.poll() is None:
        """[summary]
        """
        check_io()

#TODO: Remove this hardcoding
image_copasi = "ghcr.io/biosimulators/biosimulators_copasi/copasi"
version_copasi = "sha256:dea16b66bdd5b80d0638729377e1e11377f8b6f6211a146701d8b90ed285c316"
in_dir_copasi = os.path.join(Config.OMEX_FILE_PATH, 'copasi')
out_dir_copasi = Config.COPASI_RESULTS_CSV_PATH
omex_list_copasi = []
for omex in fl.get_file_list(in_dir_copasi, 'omex'):
    omex_list_copasi.append(omex+'.omex')

image_vcell = "ghcr.io/biosimulators/vcell"
version_vcell = "7.3.0.07"
in_dir_vcell = os.path.join(Config.OMEX_FILE_PATH, 'vcell')
out_dir_vcell = Config.COPASI_RESULTS_CSV_PATH
omex_list_vcell = []
for omex in fl.get_file_list(in_dir_vcell, 'omex'):
    omex_list_vcell.append(omex + '.omex')

def run_sim():
    for omex in omex_list_copasi:
        run_docker(image_copasi, version_copasi, in_dir_copasi, out_dir_copasi, omex_file=omex)
    for omex in omex_list_vcell:
        run_docker(image_vcell, version_vcell, in_dir_vcell, out_dir_vcell, omex_file=omex)


if __name__ == "__main__":
    try:
        run_sim()
    except KeyboardInterrupt:
        logger.warning("Stopping...")

