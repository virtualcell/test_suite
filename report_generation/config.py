import os

__all__ = ['Config']

class Config:
    """Config file
    """
    BASE_URL = 'https://www.ebi.ac.uk'
    BASE_DIR = os.path.dirname(__file__)
    BASE_FILES_PATH = os.path.join(BASE_DIR, 'files')

    HEADERS = {
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

    MODEL_FILES_PATH = os.path.join(BASE_FILES_PATH, 'bmdb_models')
    
    SEDML_DOC_PATH = os.path.join(BASE_FILES_PATH, 'sedml_docs')
    
    OMEX_FILE_PATH = os.path.join(BASE_FILES_PATH, 'omex_archives')
    
    VCELL_RESULTS_CSV_PATH = os.path.join(BASE_FILES_PATH, 'results', 'vcell')
    
    COPASI_RESULTS_CSV_PATH = os.path.join(BASE_FILES_PATH, 'results', 'copasi')

