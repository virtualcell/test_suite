""" SED-ML generator for SBML model files
:Author: Akhil Marupilla <marupilla@mail.com>
:Date: 2020-11-23
:Copyright: 2020, UConn Health
:License: MIT
"""

import os
from report_generation.config import Config
import libsbml
import libsedml


model_files_path = Config.MODEL_FILES_PATH

sedml_doc_path = Config.SEDML_DOC_PATH

model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))


# NOTE: filename has to be without extension
def create_sedml(filename, simulator, 
    initial_time=0.0, report_output_start=0.0, 
    report_output_end=10, no_of_time_points=101):

    # create the document
    doc = libsedml.SedDocument()
    doc.setLevel(1)
    doc.setVersion(1)

    # create a first model referencing an sbml file
    model = doc.createModel()
    model.setId(filename)
    model.setSource(f'{filename}.xml')
    model.setLanguage("urn:sedml:language:sbml")

    # create simulation
    # Hardcoding timepoints to its minimum
    tc = doc.createUniformTimeCourse()
    tc.setId(filename)
    tc.setInitialTime(float(initial_time))
    tc.setOutputStartTime(float(report_output_start))
    tc.setOutputEndTime(float(report_output_end))
    tc.setNumberOfPoints(int(no_of_time_points))

    # need to set the correct KISAO Term
    """
         VCell testing use CVODE KISAOID: 0000019
         COPASI testing use LSODA KISAOID: 0000088
         for basic testing
    """
    alg = tc.createAlgorithm()
    if simulator == 'copasi':
        alg.setKisaoID(f'KISAO:0000088')
    elif simulator == 'vcell':
        alg.setKisaoID(f'KISAO:0000019')
    else:
        print(f"{simulator} is still not supported to generate the SED-ML")

    # create a task that uses the simulation and the model above
    task = doc.createTask()
    task.setId(filename)
    task.setName(filename)
    task.setModelReference(filename)
    task.setSimulationReference(filename)

    # add a DataGenerator to hold the output for time
    dg = doc.createDataGenerator()
    dg.setId("time")
    dg.setName("time")
    var = dg.createVariable()
    var.setId("time")
    var.setName("time")
    var.setTaskReference(filename)
    var.setSymbol("urn:sedml:symbol:time")
    dg.setMath(libsedml.parseFormula("time"))

    full_sbml_path = os.path.join(model_files_path, f'{filename}.xml')

    reader = libsbml.SBMLReader()

    sbml_model_file = reader.readSBMLFromFile(full_sbml_path)
    sbml = sbml_model_file.getModel()

    specie_list = []
    for species_sbml in sbml.getListOfSpecies():
        species_id = species_sbml.getId()
        specie_list.append(species_id)

    # adding a DataGenerator to hold the output for all species from the model
    for specie in specie_list:
        # and  for species
        dg = doc.createDataGenerator()
        dg.setId(f'{specie}')
        dg.setName(f'{specie}')
        var = dg.createVariable()
        var.setId(f'{specie}')
        var.setName(f'{specie}')
        var.setTaskReference(filename)
        var.setTarget(
            f"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=&apos;{specie}&apos;]")
        dg.setMath(libsedml.parseFormula(f"{specie}"))

    # add a report
    report = doc.createReport()
    report.setId(filename)
    report.setName(filename)
    set = report.createDataSet()
    set.setId("time")
    set.setLabel("time")
    set.setDataReference("time")

    for specie in specie_list:
        set = report.createDataSet()
        set.setId(f'{specie}')
        set.setLabel(f'{specie}')
        set.setDataReference(f'{specie}')

    # write the document
    libsedml.writeSedML(doc, os.path.join(sedml_doc_path, simulator, f'{filename}.sedml'))
    print(f"SED-ML Document created for {simulator} with filename {filename}.sedml")

def gen_sedml():
    for sbml_model in model_files:
        if sbml_model.split('.')[1] == 'xml':
            model_name = sbml_model.split('.xml')[0]
            create_sedml(model_name, 'vcell')
            create_sedml(model_name, 'copasi')
        elif sbml_model.split('.')[1] != 'xml':
            print(f"{sbml_model} is not a model file\n")
        else:
            print(f"No SBML files found in the directory {os.path.join(model_files_path)}\n")

