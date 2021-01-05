from report_generation.combine import omex_maker
import unittest

class OmexMakerTestCase(unittest.TestCase):
    gen_archive = omex_maker.GenOmex(
        model_path='tests/fixtures',
        sedml_path='tests/fixtures',
        omex_path='tests/fixtures',
        simulators=['vcell', 'copasi']
    )
    def test_GenOmex(self):
        self.assertEqual(self.gen_archive.model_path, 'tests/fixtures')
        self.assertEqual(self.gen_archive.sedml_path, 'tests/fixtures')
        self.assertEqual(self.gen_archive.omex_path, 'tests/fixtures')
        self.assertEqual(self.gen_archive.simulators, ['vcell', 'copasi'])

    def test_create_omex_archive(self):
        
        create_archive = self.gen_archive.create_omex_archive(
            sbml_name='model_1.xml', sedml_name='sedml_doc', simulator='vcell')
        self.assertEqual(create_archive, True)
    
    def test_gen_omex(self):
        create_omex = self.gen_archive.gen_omex()
        self.assertEqual(create_omex, None)
