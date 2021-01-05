""" Files list from a directory

:Author: Akhil Marupilla <marupilla@mail.com>
:Date: 2020-11-23
:Copyright: 2020, UConn Health
:License: MIT
"""

import os
from logzero import logger


def get_file_list(path, file_type = 'xml') -> list():
    """This is a function which lists all the files in the specific directory

    Args:
        path (`str`): path of the directory
        file_type (`str`, optional): file extension type. Defaults to XML.

    Returns:
        list: returns the list of files
    """
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


