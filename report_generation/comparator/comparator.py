import os
import sys
from report_generation.config import Config
import libsbml
import pandas as pd


vcell_results_csv_dir = Config.VCELL_RESULTS_CSV_PATH

copasi_results_csv_dir = Config.COPASI_RESULTS_CSV_PATH

models_dir = Config.MODEL_FILES_PATH

reader = libsbml.SBMLReader()


def get_species(model):
    global reader

    sbml_model_file = reader.readSBMLFromFile(os.path.join(models_dir, model))
    sbml = sbml_model_file.getModel()

    specie_list = []
    for species_sbml in sbml.getListOfSpecies():
        species_id = species_sbml.getId()
        specie_list.append(species_id)
    return specie_list


def vcell_path(csv_name):
    model_name = csv_name.split('.csv')[0]
    path = os.path.join(vcell_results_csv_dir, model_name, csv_name)
    if not os.path.exists(path):
        return -1
    else:
        return path


def copasi_path(csv_name):
    model_name = csv_name.split('.csv')[0]
    path = os.path.join(copasi_results_csv_dir, model_name, csv_name)
    if not os.path.exists(path):
        return -1
    else:
        return path


models = os.listdir(models_dir)
models = sorted(models)
models.pop(0)
vcell_csvs = []
copasi_csvs = []

# Get all Vcell csv paths in list
for folder in os.listdir(vcell_results_csv_dir):
    if folder not in ['.DS_Store', 'empty_results.txt']:
        files = os.listdir(os.path.join(vcell_results_csv_dir, folder))
        if f'{folder}.csv' in files:
            vcell_csvs.append(f'{folder}.csv')

# Get all COPASI csv paths in list
for folder in os.listdir(copasi_results_csv_dir):
    if folder not in ['.DS_Store', 'empty_results.txt']:
        files = os.listdir(os.path.join(copasi_results_csv_dir, folder))
        if f'{folder}.csv' in files:
            copasi_csvs.append(f'{folder}.csv')

copasi_csvs = sorted(copasi_csvs)
vcell_csvs = sorted(vcell_csvs)

vcell_na_csv = []
copasi_na_csv = []

comparisons_done = 0
files_10e1 = []
files_10e4 = []
files_10e12 = []

unmatching_specie_models = []


def gen_report():
    for model in models:
        to_continue = False
        species = get_species(model)
        model_name = model.split('.xml')[0]

        copasi_csv_path = copasi_path(f'{model_name}.csv')
        vcell_csv_path = vcell_path(f'{model_name}.csv')

        if copasi_csv_path == -1:
            print(copasi_csv_path)
            copasi_na_csv.append(model_name)
            to_continue = True
        if vcell_csv_path == -1:
            print(vcell_csv_path)
            vcell_na_csv.append(model_name)
            to_continue = True
        if to_continue:
            continue

        ## Comparing copasi and vcell csvs
        try:
            d_copasi = pd.read_csv(copasi_csv_path)
            d_vcell = pd.read_csv(vcell_csv_path)
        except:
            error_type = str(sys.exc_info()[0]).split("'")[1]
            print(model_name, ":", error_type)
            if error_type == 'pandas.errors.EmptyDataError':
                print(f'Empty CSV: {model_name}')
            continue

        try:
            diff = abs(d_copasi[species] - d_vcell[species])

        except:
            error_type = str(sys.exc_info()[0]).split("'")[1]
            print(model_name, ":", error_type)
            if error_type == 'KeyError':
                unmatching_specie_models.append(model_name)
            continue

        if (diff > 0.1).any(True).sum() > 0:
            files_10e1.append(model_name)

        if (diff > 10e4).any(True).sum() > 0:
            files_10e1.append(model_name)

        if (diff > 10e12).any(True).sum() > 0:
            files_10e1.append(model_name)

        global comparisons_done
        comparisons_done = comparisons_done + 1


if __name__ == "__main__":
    gen_report()
