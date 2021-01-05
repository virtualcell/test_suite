from report_generation.sbml import sbml_fetcher
import unittest

class SbmlFetcher(unittest.TestCase):
    def test_create_model_list(self):
        model_list = sbml_fetcher.create_model_list(1, 2, 1, exclude_models=[])
        self.assertEqual(model_list, ['BIOMD0000000001'])
    
    def test_soup_scraper(self):
        soup_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.ebi.ac.uk",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        soup_base_url = 'https://www.ebi.ac.uk'
        url = sbml_fetcher.soup_scraper(
            model='BIOMD0000000001', headers=soup_header, base_url=soup_base_url)
        self.assertEqual(
            url, '/biomodels/model/download/BIOMD0000000001.2?filename=BIOMD0000000001_url.xml')

    def test_download_sbml(self):
        download_model = sbml_fetcher.download_sbml(2, 1, -1, model_files_path='tests/fixtures/models')
        self.assertEqual(download_model, ['BIOMD0000000002'])
