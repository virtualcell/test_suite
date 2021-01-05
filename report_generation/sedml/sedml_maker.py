""" SED-ML generator for SBML model files
:Author: Akhil Marupilla <marupilla@mail.com>
:Date: 2020-11-23
:Copyright: 2020, UConn Health
:License: MIT
"""

import os
from report_generation.config import Config
from report_generation.combine.files_list import get_file_list
import libsbml
import libsedml
from logzero import logger

__all__ = [
    'create_sedml',
    'gen_sedml'
]

# NOTE: sbml_name has to be without extension
def create_sedml(sbml_name, simulator, 
                 initial_time=0.0, report_output_start=0.0, 
                 report_output_end=10, no_of_time_points=101, 
                 model_files_path=Config.MODEL_FILES_PATH,
                 sedml_doc_path=Config.SEDML_DOC_PATH) -> int:
    """This is a function which creates SED-ML file

    Args:
        sbml_name (`str`): SBML name without extension
        simulator (`str`): simulator name
        initial_time (float, optional): initial timepoint. Defaults to 0.0.
        report_output_start (float, optional): report output start timepoint. Defaults to 0.0.
        report_output_end (int, optional): report output end timepoint. Defaults to 10.
        no_of_time_points (int, optional): Number of timepoint. Defaults to 101.
        model_files_path (`str`, optional): path to SBML model files. Defaults to Config.MODEL_FILES_PATH.
        sedml_doc_path (`str`, optional): path to SED-ML doc files. Defaults to Config.SEDML_DOC_PATH.
    """
    # create the document
    doc = libsedml.SedDocument()
    doc.setLevel(1)
    doc.setVersion(1)

    # create a first model referencing an sbml file
    model = doc.createModel()
    model.setId(sbml_name)
    model.setSource(f'{sbml_name}.xml')
    model.setLanguage("urn:sedml:language:sbml")

    # create simulation
    tc = doc.createUniformTimeCourse()
    tc.setId(sbml_name)
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
        logger.warning(
            f"{simulator} is not supported to generate the SED-ML, falling back to VCell(CVODE KISAO:0000019)")
        alg.setKisaoID(f'KISAO:0000019')

    # create a task that uses the simulation and the model above
    task = doc.createTask()
    task.setId(sbml_name)
    task.setName(sbml_name)
    task.setModelReference(sbml_name)
    task.setSimulationReference(sbml_name)

    # add a DataGenerator to hold the output for time
    dg = doc.createDataGenerator()
    dg.setId("time")
    dg.setName("time")
    var = dg.createVariable()
    var.setId("time")
    var.setName("time")
    var.setTaskReference(sbml_name)
    var.setSymbol("urn:sedml:symbol:time")
    dg.setMath(libsedml.parseFormula("time"))

    full_sbml_path = os.path.join(model_files_path, f'{sbml_name}.xml')

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
        var.setTaskReference(sbml_name)
        var.setTarget(
            f"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=&apos;{specie}&apos;]")
        dg.setMath(libsedml.parseFormula(f"{specie}"))

    # add a report
    report = doc.createReport()
    report.setId(sbml_name)
    report.setName(sbml_name)
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
    is_sedml_created = libsedml.writeSedML(doc, os.path.join(sedml_doc_path, simulator, f'{sbml_name}.sedml'))
    logger.info(
        f"SED-ML Document created for {simulator} with filename {sbml_name}.sedml")
    print("is_sedml_created: ", is_sedml_created)
    return is_sedml_created


def gen_sedml(simulator='vcell', initial_time=0.0, 
              report_output_start=0.0,
              report_output_end=10, no_of_time_points=101, 
              model_file_path=Config.MODEL_FILES_PATH, 
              sedml_doc_path= Config.SEDML_DOC_PATH) -> tuple:
    """This is a function that generates SED-ML

    Args:
        model_file_path (`str`, optional): path to SBML model files. Defaults to Config.MODEL_FILES_PATH.
    """
    vcell = []
    copasi = []
    for sbml_model in get_file_list(model_file_path, 'xml'):
        vcell.append(create_sedml(
            sbml_model, 'vcell', initial_time=0.0, report_output_start=0.0,
            report_output_end=10, no_of_time_points=101, model_files_path=Config.MODEL_FILES_PATH, sedml_doc_path=Config.SEDML_DOC_PATH))
        copasi.append(create_sedml(
            sbml_model, 'copasi', initial_time=0.0, report_output_start=0.0,
            report_output_end=10, no_of_time_points=101, model_files_path=Config.MODEL_FILES_PATH, sedml_doc_path=Config.SEDML_DOC_PATH))
    print('vcell, copasi: -->', vcell, copasi)
    return (vcell, copasi)
