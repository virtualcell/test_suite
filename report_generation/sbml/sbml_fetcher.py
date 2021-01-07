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


#TODO: Consider a better scenario to determine the models to exclude instead harcoding 649, 694, 701

class SbmlFetcher:
    def __init__(self,
                 start=None,
                 end: int=0,
                 step: int=-1,
                 base_url: str=Config.BASE_URL,
                 search_model_url: str=Config.SEARCH_MODEL_URL,
                 headers: dict=Config.HEADERS,
                 model_files_path: str=Config.MODEL_FILES_PATH,
                 exclude_models: list=[649, 694, 701],
                 css_class='font-size: small; margin: -25px 0;'
                ):
        self.base_url = base_url
        self.search_model_url = search_model_url
        self.headers = headers
        self.model_files_path = model_files_path
        self.start = start
        self.end = end
        self.step = step
        self.exclude_models=exclude_models
        self.css_class = css_class
        self.latest_pub_model = None

    def get_latest_pub_model(self):
        get_content = requests.get(self.search_model_url, headers=self.headers).text
        soup = BeautifulSoup(get_content, 'lxml')
        model_finder = soup.find_all('span', style=self.css_class)
        _id = model_finder[0].text
        try:
            latest_pub_model = _id.split('|')[0].replace(' ', '').split(':')[1][-4:]
            return int(latest_pub_model)
        except IndexError:
            logger.info("Check the Config for URL")
        

    def create_model_list(self):
        models_to_exclude = self.exclude_models
        model_name_list = list()
        for model_num in range(self.start, self.end, self.step):
            if model_num in models_to_exclude:
                continue
            if model_num < 10:
                model_name_list.append(f"BIOMD000000000{model_num}")
            elif model_num >= 10 and model_num < 100:
                model_name_list.append(f"BIOMD00000000{model_num}")
            else:
                model_name_list.append(f"BIOMD0000000{model_num}")
        return model_name_list
    
    def soup_scraper(self, model):
        model_files_url = f"{self.base_url}/biomodels/{model}#Files"
        req_content = requests.get(model_files_url, headers=self.headers).text
        soup = BeautifulSoup(req_content, 'lxml')
        preview_button_context = soup.find_all('a', id='previewButton1')
        preview_url = preview_button_context[0]['data-download-link']
        return preview_url

    def download_sbml(self):
        if self.start is None:
            self.start = self.get_latest_pub_model()
        for model in self.create_model_list():
            try:
                sbml_file_link = self.base_url + \
                    self.soup_scraper(model)
                urllib.request.urlretrieve(sbml_file_link, os.path.join(
                        self.model_files_path, f'{model}.xml'))
                logger.info(f'Downloaded {model}.xml')
            except IndexError as IE:
                logger.info(f"{model}.xml is not published yet.")
                continue
            except:
                logger.error(f"Coudn't download the {model}")
                continue

        return self.create_model_list()

