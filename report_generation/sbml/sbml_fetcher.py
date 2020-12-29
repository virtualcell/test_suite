import os
from report_generation.config import Config
import urllib
from bs4 import BeautifulSoup
import requests
from logzero import logger

model_files_path = Config.MODEL_FILES_PATH

sedml_doc_path = Config.SEDML_DOC_PATH

model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))

headers = Config.HEADERS

def create_model_list(start=1, end=1000, step=1):
    models_to_exclude = [649, 694, 701]
    model_name_list = list()
    for model_num in range(start, end, step):
        if model_num in models_to_exclude:
            continue
        if model_num < 10:
            model_name_list.append("BIOMD" + "000000000" + f"{model_num}")
        elif model_num >= 10 and model_num < 100:
            model_name_list.append("BIOMD" + "00000000" + f"{model_num}")
        else:
            model_name_list.append("BIOMD" + "0000000" + f"{model_num}")
    return model_name_list


def soup_scraper(model, headers):
    model_files_url = f"https://www.ebi.ac.uk/biomodels/{model}#Files"
    req_content = requests.get(model_files_url, headers=headers).text
    soup = BeautifulSoup(req_content, 'lxml')
    preview_button_context = soup.find_all('a', id='previewButton1')
    preview_url = preview_button_context[0]['data-download-link']
    return preview_url

def download_sbml():
    #TODO: Consider a better scenario to determine the latest published model instead harcoding 1000
    for model in create_model_list(1000, 0, -1):
        try: 
            sbml_file_link = Config.BASE_URL + soup_scraper(model, headers=headers)
            urllib.request.urlretrieve(sbml_file_link, os.path.join(
                    model_files_path, f'{model}.xml'))
            logger.info(f'Downloaded {model}.xml')
        except IndexError as IE:
            logger.info(f"{model}.xml is not published yet.")
            continue

