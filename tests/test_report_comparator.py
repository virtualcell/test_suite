import unittest
from report_generation.comparator.report_comparator import ReportComparator

class ReportComparatorTestCase(unittest.TestCase):
    report_comparator = ReportComparator(
            vcell_results_csv_dir='tests/fixtures/vcell/csv',
            copasi_results_csv_dir='tests/fixtures/copasi/csv',
            models_dir='tests/fixtures'
        )
    def test_report_comparator(self):
        self.assertEqual(self.report_comparator.vcell_results_csv_dir, 'tests/fixtures/vcell/csv')
        self.assertEqual(self.report_comparator.copasi_results_csv_dir, 'tests/fixtures/copasi/csv')
        self.assertEqual(self.report_comparator.models_dir, 'tests/fixtures')

    def test_get_species(self):
        species_list = self.report_comparator.get_species(model='BIOMD0000000001.xml')
        self.assertEqual(species_list, ['BLL', 'IL', 'AL', 'A', 'BL', 'B', 'DLL', 'D', 'ILL', 'DL', 'I', 'ALL'])

    def test_get_vcell_path_no_csv(self):
        csv_path = self.report_comparator.get_vcell_path(csv_name='BIOMD0000000001')
        self.assertEqual(csv_path, -1)
    
    def test_get_vcell_path(self):
        csv_path = self.report_comparator.get_vcell_path(csv_name='BIOMD0000000001.csv')
        self.assertEqual(csv_path, 'tests/fixtures/vcell/csv/BIOMD0000000001/BIOMD0000000001.csv')

    def test_get_copasi_path_no_csv(self):
        csv_path = self.report_comparator.get_copasi_path(csv_name='BIOMD0000000001')
        self.assertEqual(csv_path, -1)
    
    def test_get_copasi_path(self):
        csv_path = self.report_comparator.get_copasi_path(csv_name='BIOMD0000000001.csv')
        self.assertEqual(csv_path, 'tests/fixtures/copasi/csv/BIOMD0000000001/BIOMD0000000001.csv')
    
    def test_prepare_csv(self):
        prepare_path = self.report_comparator.prepare_csv()
        self.assertEqual(prepare_path, (['BIOMD0000000001.csv'], ['BIOMD0000000001.csv']))
    
    # def test_report_generation(self):
    #     report = self.report_comparator.generate_report(report_path='test/fixtures')
    #     self.assertEqual(report, None)
