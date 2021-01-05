""" SBML model downloader
:Author: Akhil Marupilla <marupilla@mail.com>
:Date: 2020-11-23
:Copyright: 2020, UConn Health
:License: MIT
"""

import os
from report_generation.config import Config
import urllib
from bs4 import BeautifulSoup
import requests
from logzero import logger

__all__ = [
    'create_model_list',
    'soup_scraper',
    'download_sbml'
]

#TODO: Consider a better scenario to determine the latest published model instead harcoding 1000
#TODO: Consider a better scenario to determine the models to exclude instead harcoding 649, 694, 701
def create_model_list(start=1, 
                    end=1000, 
                    step=1, 
                    exclude_models=[649, 694, 701]) -> list():
    """This is a function that creates model list

    Args:
        start (int, optional): int start point. Defaults to 1.
        end (int, optional): int end point. Defaults to 1000.
        step (int, optional): int step. Defaults to 1.
        exclude_models (list, optional): Models to exclude which are removed from BMDB. Defaults to [649, 694, 701].

    Returns:
        list: returns the list of model name.
    """
    models_to_exclude = exclude_models
    model_name_list = list()
    for model_num in range(start, end, step):
        if model_num in models_to_exclude:
            continue
        if model_num < 10:
            model_name_list.append(f"BIOMD000000000{model_num}")
        elif model_num >= 10 and model_num < 100:
            model_name_list.append(f"BIOMD00000000{model_num}")
        else:
            model_name_list.append(f"BIOMD0000000{model_num}")
    return model_name_list


def soup_scraper(model, headers=Config.HEADERS,
                 base_url=Config.BASE_URL) -> str:
    """Scrapes the preview URL of specific model

    Args:
        model (`str`): takes model name in the format BIOMD0000000001
        headers (`dict`): request headers for `https://www.ebi.ac.uk`. Defaults to Config.HEADERS.
        base_url (`str`): default base URL https://www.ebi.ac.uk. Defaults to Config.BASE_URL.

    Returns:
        str : returns the string of download URL
    """
    model_files_url = f"{base_url}/biomodels/{model}#Files"
    req_content = requests.get(model_files_url, headers=headers).text
    soup = BeautifulSoup(req_content, 'lxml')
    preview_button_context = soup.find_all('a', id='previewButton1')
    preview_url = preview_button_context[0]['data-download-link']
    return preview_url


def download_sbml(start,end, step,
                    base_url=Config.BASE_URL,
                    headers=Config.HEADERS,
                    model_files_path=Config.MODEL_FILES_PATH) -> list:
    """Downloads SBML files

    Args:
        start (int): Start point
        end (int): End point
        step (int): Step to run the loop
        base_url (`str`, optional): base URL https://www.ebi.ac.uk. Defaults to Config.BASE_URL.
        headers (`str`, optional): request headers for `https://www.ebi.ac.uk`. Defaults to Config.HEADERS.
        model_files_path (`str`, optional): path for SBML model files to download. Defaults to Config.MODEL_FILES_PATH.
    """
    for model in create_model_list(start, end, step):
        try:
            sbml_file_link = base_url + \
                soup_scraper(model, headers, base_url)
            urllib.request.urlretrieve(sbml_file_link, os.path.join(
                    model_files_path, f'{model}.xml'))
            logger.info(f'Downloaded {model}.xml')
        except IndexError as IE:
            logger.info(f"{model}.xml is not published yet.")
            continue
        except:
            logger.error(f"Coudn't download the {model}")
            continue

    return create_model_list(start, end, step)

