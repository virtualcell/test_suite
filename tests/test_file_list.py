import unittest
from report_generation.utils.files_list import get_file_list


class FileListTestCase(unittest.TestCase):
    def test_get_model_list(self):
        sbml_list = get_file_list(path='tests/fixtures', file_type='xml')
        self.assertEqual(sbml_list, ['BIOMD0000000001', 'model_1'])
    
    def test_get_model(self):
        sbml_name = get_file_list(path='tests/fixtures', file_type='xml')
        self.assertNotEqual(sbml_name, 'model_1')
    
    def test_get_empty_list(self):
        empty_list = get_file_list(path='tests/fixtures/empty')
        self.assertEqual(empty_list, list())
    
    def test_get_sedml_list(self):
        sedml_list = get_file_list(path='tests/fixtures', file_type='sedml')
        self.assertEqual(sedml_list, ['sedml_doc'])
    
    def test_get_omex_list(self):
        omex_list = get_file_list(path='tests/fixtures', file_type='omex')
        self.assertEqual(omex_list, [])
    

    
