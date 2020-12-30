import os
from report_generation.config import Config
from logzero import logger

"""Gets file list for specified file type
parameters:
path: path to search
file_type: file type to search 
"""
def get_file_list(path, file_type = 'xml') -> list():
    files = os.listdir(os.path.join(path))
    if '.gitkeep' in files:
        files.remove('.gitkeep')

    if len(files) == 0:
        logger.error(
            f"No files found in the directory {os.path.join(os.path.join(path))}\n")
        return []
    
    _file_list = list()
    for file in files:
        if file.endswith(file_type):
            sbml_file = file.split('.')[0]
            _file_list.append(sbml_file)

    _file_list.sort()
    
    return _file_list


