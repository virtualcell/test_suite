""" SED-ML generator for SBML model files
:Author: Akhil Marupilla <marupilla@mail.com>
:Date: 2020-11-23
:Copyright: 2020, UConn Health
:License: MIT
"""

import os
import libsbml
import libsedml

model_files = os.listdir('BMDBmodels')


# NOTE: filename has to be without extension
def create_sedml(filename):
    
    # create the document
    doc = libsedml.SedDocument()
    doc.setLevel(1)
    doc.setVersion(1)

    # create a first model referencing an sbml file
    model = doc.createModel()
    model.setId(filename)
    model.setSource(f'BMDBmodels/{filename}.xml')
    model.setLanguage("urn:sedml:language:sbml")

    # create simulation
    tc = doc.createUniformTimeCourse()
    tc.setId(filename)
    tc.setInitialTime(0.0)
    tc.setOutputStartTime(0.0)
    tc.setOutputEndTime(10.0)
    tc.setNumberOfPoints(101)

    # need to set the correct KISAO Term
    """
         VCell testing use CVODE KISAOID: 0000019
         COPASI testing use LSODA KISAOID: 0000088
         for basic testing
    """
    alg = tc.createAlgorithm()
    alg.setKisaoID("KISAO:0000088")

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

    full_filepath = os.path.abspath(os.path.join('BMDBmodels', f'{filename}.xml'))

    reader = libsbml.SBMLReader()

    sbml_model_file = reader.readSBMLFromFile(full_filepath)
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
        var.setTarget(f"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id=&apos;{specie}&apos;]")
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
    libsedml.writeSedML(doc, f'sedmls/{filename}.sedml')


for sbml_model in model_files:
    if sbml_model.split('.')[1] == 'xml':
        model_name = sbml_model.split('.xml')[0]
        create_sedml(model_name)
