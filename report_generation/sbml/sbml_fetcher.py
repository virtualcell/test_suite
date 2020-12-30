import os
from report_generation.config import Config
import urllib
from bs4 import BeautifulSoup
import requests
from logzero import logger



#TODO: Consider a better scenario to determine the latest published model instead harcoding 1000
#TODO: Consider a better scenario to determine the models to exclude instead harcoding 649, 694, 701
def create_model_list(start=1, end=1000, step=1, exclude_models=[649, 694, 701]):
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


def soup_scraper(model, headers, base_url):
    model_files_url = f"{base_url}/biomodels/{model}#Files"
    req_content = requests.get(model_files_url, headers=headers).text
    soup = BeautifulSoup(req_content, 'lxml')
    preview_button_context = soup.find_all('a', id='previewButton1')
    preview_url = preview_button_context[0]['data-download-link']
    return preview_url


def download_sbml(start, end, step, base_url=Config.BASE_URL, headers=Config.HEADERS, model_files_path=Config.MODEL_FILES_PATH):
    
    for model in create_model_list(start, end, step):
        try: 
            sbml_file_link = base_url + \
                soup_scraper(model, headers=headers)
            urllib.request.urlretrieve(sbml_file_link, os.path.join(
                    model_files_path, f'{model}.xml'))
            logger.info(f'Downloaded {model}.xml')
        except IndexError as IE:
            logger.info(f"{model}.xml is not published yet.")
            continue
        except:
            logger.error(f"Coudn't download the {model}")
            continue

