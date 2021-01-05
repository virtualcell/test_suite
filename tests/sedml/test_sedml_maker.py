from report_generation.sedml import sedml_maker
import unittest


class SedmlMaker(unittest.TestCase):
    def test_create_vcell_sedml(self):
        create_sedml = sedml_maker.create_sedml(sbml_name='model_1',
                                                simulator='vcell', initial_time=0,
                                                report_output_end=10,
                                                no_of_time_points=101,
                                                model_files_path='tests/fixtures',
                                                sedml_doc_path='tests/fixtures')
        self.assertEqual(create_sedml, 1)
    

    
    def test_create_copasi_sedml(self):
        create_sedml = sedml_maker.create_sedml(sbml_name='model_1',
                                                simulator='copasi', initial_time=0,
                                                report_output_end=10,
                                                no_of_time_points=101,
                                                model_files_path='tests/fixtures',
                                                sedml_doc_path='tests/fixtures')
        self.assertEqual(create_sedml, 1)
# sbml_model, 'copasi', initial_time=0.0, report_output_start=0.0,
#         report_output_end = 10, no_of_time_points = 101, model_files_path = Config.MODEL_FILES_PATH, sedml_doc_path = Config.SEDML_DOC_PATH

    # def test_gen_sedml(self):
    #     generate_sedml = sedml_maker.gen_sedml('model_1', initial_time=0.0, report_output_start=0.0,
    #                                                    report_output_end = 10, no_of_time_points = 101,
    #         model_file_path='tests/fixtures', sedml_doc_path='tests/fixtures', simulator='copasi')
    #     self.assertEqual(generate_sedml, ([],[]))
