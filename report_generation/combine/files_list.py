import os
from report_generation.config import Config

omex_path = Config.OMEX_FILE_PATH
sedml_doc_path = Config.SEDML_DOC_PATH
model_files_path = Config.MODEL_FILES_PATH
model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))


class FilesList:
    """[summary]
    """

    def sbml_file_list(self, path=model_files_path):
        sbml_file_list = list()
        for sbml_file in os.listdir(os.path.join(path)):
            if sbml_file.endswith('.xml'):
                sbml_file = sbml_file.split('.')[0]
                sbml_file_list.append(sbml_file)
            elif sbml_file.split('.')[1] != 'xml':
                print(f"{sbml_file} is not a model file\n")
            else:
                print(
                    f"No model files found in the directory {os.path.join(os.path.join(model_files_path))}\n")
        return sbml_file_list

    def vcell_sedml_files_list(self):
        vcell_sedml_file_list = list()
        for sedml_file in os.listdir(os.path.join(sedml_doc_path, 'vcell')):
            if sedml_file.endswith('.sedml'):
                sedml_file = sedml_file.split('.')[0]
                vcell_sedml_file_list.append(sedml_file)
            else:
                print(
                    f'No SED-ML documents found in the directory {os.path.join(sedml_doc_path, "vcell")}\n')
        return vcell_sedml_file_list

    def copasi_sedml_files_list(self):
        copasi_sedml_file_list = list()
        for sedml_file in os.listdir(os.path.join(sedml_doc_path, 'copasi')):
            if sedml_file.endswith('.sedml'):
                sedml_file = sedml_file.split('.')[0]
                copasi_sedml_file_list.append(sedml_file)
            else:
                print(
                    f'No SED-ML found in the directory {os.path.join(sedml_doc_path, "copasi")}\n')
        return copasi_sedml_file_list
