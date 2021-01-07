from report_generation.sbml import sbml_fetcher
import unittest

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

class SbmlFetcherTestCase(unittest.TestCase):
    sbml_fetcher = sbml_fetcher.SbmlFetcher(
        start=2,
        end=0,
        step=-1,
        base_url='https://www.ebi.ac.uk',
        headers=soup_header,
        model_files_path='tests/fixtures/test_download',
        exclude_models=[],
        css_class=''
    )

    def test_sbml_fetcher(self):
        self.assertEqual(self.sbml_fetcher.start, 2)
        self.assertEqual(self.sbml_fetcher.end, 0)
        self.assertEqual(self.sbml_fetcher.step, -1)
        self.assertEqual(self.sbml_fetcher.base_url, 'https://www.ebi.ac.uk')
        self.assertNotEqual(self.sbml_fetcher.headers, {})
        self.assertEqual(self.sbml_fetcher.model_files_path, 'tests/fixtures/test_download')
        self.assertEqual(self.sbml_fetcher.exclude_models, [])
        self.assertEqual(self.sbml_fetcher.css_class, '')

    def test_get_latest_pub_model(self):
        latest_model = self.sbml_fetcher.get_latest_pub_model()
        self.assertNotEqual(latest_model, 'model_number')
    
    def test_get_latest_pub_model_none(self):
        latest_model = self.sbml_fetcher.get_latest_pub_model()
        self.assertEqual(latest_model, -1)
    
    def test_create_model_list(self):
        model_list = self.sbml_fetcher.create_model_list()
        self.assertEqual(model_list, ['BIOMD0000000002', 'BIOMD0000000001'])
    
    def test_soup_scraper(self):
        url = self.sbml_fetcher.soup_scraper('BIOMD0000000002')
        self.assertEqual(url, '/biomodels/model/download/BIOMD0000000002.2?filename=BIOMD0000000002_url.xml')
    
    def test_download_sbml(self):
        download_list = self.sbml_fetcher.download_sbml()
        self.assertEqual(download_list, ['BIOMD0000000002', 'BIOMD0000000001'])
    
