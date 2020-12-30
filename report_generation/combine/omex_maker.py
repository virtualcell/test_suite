from report_generation.sbml import sbml_fetcher
from libcombine import *
from report_generation.combine.files_list import get_file_list
from report_generation.config import Config
from logzero import logger


def create_omex_archive(sbml_name, sedml_name, simulator='vcell') -> None:
    """Creates the OMEX archive

    Args:
        sbml_name (string): The SBML model name in XML format
        sedml_name (string): The SED-ML doc with .sedml extension
        simulator (string): Simulator name currently supporting VCell and COPASI only(default='vcell')
    """
    archive = CombineArchive()

    archive.addFile(
        os.path.join(Config.MODEL_FILES_PATH,
                     f"{sbml_name}.xml"),  # target file name
        sbml_name + '.xml',  # filename
        # look up identifier for SBML models
        KnownFormats.lookupFormat("sbml"),
        True  # mark file as master
    )
    archive.addFile(
        os.path.join(Config.SEDML_DOC_PATH, simulator,
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
        Config.OMEX_FILE_PATH, simulator, f"{sbml_name.split('.')[0]}.omex"))
    archive.writeToFile(out_file)
    out_file_name = out_file.split('/')[-1]
    logger.info(f'Archive created: {out_file_name}')



class GenOmex:
    def __init__(self, model_path = Config.MODEL_FILES_PATH, sedml_path = Config.SEDML_DOC_PATH) -> None:
        self.sbml_files_list = get_file_list(model_path)
        self.vcell_sedml_files = get_file_list(
            os.path.join(sedml_path, 'vcell'), 'sedml')
        self.copasi_sedml_files = get_file_list(
            os.path.join(sedml_path, 'copasi'), 'sedml')

    def gen_omex(self):
        for sbml, sedml in zip(self.sbml_files_list, self.vcell_sedml_files):
            create_omex_archive(sbml, sedml, simulator='vcell')

        for sbml, sedml in zip(self.sbml_files_list, self.copasi_sedml_files):
            create_omex_archive(sbml, sedml, simulator='copasi')

