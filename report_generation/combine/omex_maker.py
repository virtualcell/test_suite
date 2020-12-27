from libcombine import *
from report_generation.combine.files_list import FilesList
from report_generation.config import Config

omex_path = Config.OMEX_FILE_PATH
sedml_doc_path = Config.SEDML_DOC_PATH
model_files_path = Config.MODEL_FILES_PATH
model_files = os.listdir(os.path.abspath(
    os.path.join(model_files_path)))

files_list = FilesList()

def create_omex_archive(sbml_name, sedml_name, simulator):
    archive = CombineArchive()

    archive.addFile(
        os.path.join(model_files_path, f"{sbml_name}.xml"),  # target file name
        sbml_name + '.xml',  # filename
        # look up identifier for SBML models
        KnownFormats.lookupFormat("sbml"),
        True  # mark file as master
    )
    archive.addFile(
        os.path.join(sedml_doc_path, simulator,
                     f"{sedml_name}.sedml"),  # target file name
        sedml_name + '.sedml',  # filename
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
    creator.setOrganization("UConn Health")

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
    out_file = os.path.abspath(os.path.join(
        omex_path, simulator, f"{sbml_name.split('.')[0]}.omex"))
    archive.writeToFile(out_file)

    print('Archive created:', out_file.split('/')[-1])

class GenOmex:
    def omex_gen_vcell():
        for sbml_file in files_list.sbml_file_list():
            for vcell_sedml_file in files_list.vcell_sedml_files_list():
                if sbml_file.split('.')[0] == vcell_sedml_file.split('.')[0]:
                    create_omex_archive(sbml_file, vcell_sedml_file, simulator='vcell')
                else:
                    continue

    def omex_gen_copasi():
        for sbml_file in files_list.sbml_file_list():
            for copasi_sedml_file in files_list.copasi_sedml_files_list():
                if sbml_file.split('.')[0] == copasi_sedml_file.split('.')[0]:
                    create_omex_archive(sbml_file, copasi_sedml_file, simulator='copasi')
                else:
                    continue

