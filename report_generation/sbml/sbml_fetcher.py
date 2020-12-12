import os
from .config import Config
import urllib
from bs4 import BeautifulSoup
import requests

model_files_path = Config.MODEL_FILES_PATH

sedml_doc_path = Config.SEDML_DOC_PATH

model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))

headers = Config.HEADERS

def create_model_list():
    models_to_exclude = [649, 694, 701]
    model_name_list = list()
    for i in range(1, 1000):
        if i in models_to_exclude:
            continue
        if i < 10:
            model_name_list.append("BIOMD" + "000000000" + f"{i}")
        elif i >= 10 and i < 100:
            model_name_list.append("BIOMD" + "00000000" + f"{i}")
        else:
            model_name_list.append("BIOMD" + "0000000" + f"{i}")
    return model_name_list


def soup_scraper(model, headers):
    model_files_url = f"https://www.ebi.ac.uk/biomodels/{model}#Files"
    req_content = requests.get(model_files_url, headers=headers).text
    soup = BeautifulSoup(req_content, 'lxml')
    preview_button_context = soup.find_all('a', id='previewButton1')
    preview_url = preview_button_context[0]['data-download-link']
    return preview_url

def download_sbml():
    for model in create_model_list():
        sbml_file_link = Config.BASE_URL + soup_scraper(model, headers=headers)
        urllib.request.urlretrieve(sbml_file_link, os.path.join(
                model_files_path, f'{model}.xml'))
        print(f'Downloaded {model}.xml')

    

if __name__ == "__main__":
   download_sbml()
