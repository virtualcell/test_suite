from libcombine import *

omex_path = os.path.abspath(os.path.join(
    'report_generation/files/omex_archives'))

sedml_doc_path = os.path.abspath(os.path.join(
    'report_generation', 'files', 'sedml_docs'))

model_files_path = os.path.abspath(os.path.join(
    'report_generation', 'files', 'bmdb_models'))

model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))


def createArchiveExample(sbml_name, sedml_name, simulator):
    archive = CombineArchive()

    archive.addFile(
        sbml_name,  # filename
        os.path.join(model_files_path, f"{sbml_name}"),  # target file name
        # look up identifier for SBML models
        KnownFormats.lookupFormat("sbml"),
        True  # mark file as master
    )
    archive.addFile(
        sedml_name,  # filename
        os.path.join(sedml_doc_path, simulator,
                     f"{sedml_name}"),  # target file name
        # look up identifier for SBML models
        KnownFormats.lookupFormat("sedml"),
        False  # mark file as master
    )

    # add metadata to the archive itself
    description = OmexDescription()
    description.setAbout("VCell Test Cases OMEX archives")
    description.setDescription("Test VCell against COPASI")
    description.setCreated(OmexDescription.getCurrentDateAndTime())

    creator = VCard()
    creator.setFamilyName("Marupilla")
    creator.setGivenName("Gnaneswara")
    creator.setEmail("marupilla@uchc.edu")
    creator.setOrganization("UConn")

    description.addCreator(creator)

    archive.addMetadata(".", description)

    # add metadata to the added file
    location = f'./{sbml_name}'
    description = OmexDescription()
    description.setAbout(location)
    description.setDescription("SBML model")
    description.setCreated(OmexDescription.getCurrentDateAndTime())
    archive.addMetadata(location, description)

    # write the archive
    out_file = os.path.join(omex_path, simulator, f"{sbml_name.split('.')[0]}.omex")
    archive.writeToFile(out_file)

    print('Archive created:', out_file.split('/')[-1])


vcell_sedml_file_list = []
copasi_sedml_file_list = []
sbml_file_list = []

for sbml_file in os.listdir(os.path.join(model_files_path)):
    if sbml_file.endswith('.xml'):
        sbml_file = sbml_file.split('.')[0]
        sbml_file_list.append(sbml_file)
    elif sbml_file.split('.')[1] != 'xml':
        print(f"{sbml_file} is not a model file\n")
    else:
        print(
            f"No model files found in the directory {os.path.join(os.path.join(model_files_path))}\n")

for sedml_file in os.listdir(os.path.join(sedml_doc_path, 'vcell')):
    if sedml_file.endswith('.sedml'):
        sedml_file = sedml_file.split('.')[0]
        vcell_sedml_file_list.append(sedml_file)
    else:
        print(f'No SED-ML documents found in the directory {os.path.join(sedml_doc_path, "vcell")}\n')

for sedml_file in os.listdir(os.path.join(sedml_doc_path, 'copasi')):
    if sedml_file.endswith('.sedml'):
        sedml_file = sedml_file.split('.')[0]
        copasi_sedml_file_list.append(sedml_file)
    else:
        print(f'No SED-ML found in the directory {os.path.join(sedml_doc_path, "copasi")}\n')

for sbml_file in sbml_file_list:
    for vcell_sedml_file in vcell_sedml_file_list:
        if sbml_file.split('.')[0] == vcell_sedml_file.split('.')[0]:
            createArchiveExample(sbml_file, vcell_sedml_file, 'vcell')
        else:
            continue

for sbml_file in sbml_file_list:
    for copasi_sedml_file in copasi_sedml_file_list:
        if sbml_file.split('.')[0] == copasi_sedml_file.split('.')[0]:
            createArchiveExample(sbml_file, copasi_sedml_file, 'copasi')
        else:
            continue
