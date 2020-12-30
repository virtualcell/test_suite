from report_generation.sbml import sbml_fetcher
from libcombine import *
from report_generation.combine.files_list import get_file_list
from report_generation.config import Config
from logzero import logger


class GenOmex:
    def __init__(self, 
                model_path=Config.MODEL_FILES_PATH, 
                sedml_path=Config.SEDML_DOC_PATH, 
                omex_path=Config.OMEX_FILE_PATH,
                simulators = ['vcell','copasi']) -> None:
        self.sbml_files_list = get_file_list(model_path)


        self.model_path = model_path
        self.sedml_path = sedml_path
        self.omex_path = omex_path

        self.simulators = []
        # TODO: Add more simulators once supported, this loops is a failsafe mechanism
        for simulator  in simulators:
            if simulator in ['vcell', 'copasi']:
                self.simulators.append(simulator)

        # Getting sedml files list for each simulator
        self.simulator_sedml_list_map = dict()
        for simulator in self.simulators:
            self.simulator_sedml_list_map[simulator] = get_file_list(os.path.join(sedml_path, simulator), 'sedml')
        

    def create_omex_archive(self, sbml_name,
                            sedml_name,
                            simulator='vcell',
                            ) -> None:
    
        archive = CombineArchive()

        archive.addFile(
            os.path.join(self.model_path,
                        f"{sbml_name}.xml"),  # target file name
            sbml_name + '.xml',  # filename
            # look up identifier for SBML models
            KnownFormats.lookupFormat("sbml"),
            True  # mark file as master
        )
        archive.addFile(
            os.path.join(self.sedml_path, simulator,
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
        out_file = os.path.join(
            self.omex_path, simulator, f"{sbml_name.split('.')[0]}.omex")
        archive.writeToFile(out_file)
        out_file_name = out_file.split('/')[-1]
        logger.info(f'Archive created: {out_file_name}')


    def gen_omex(self):
        for simulator, files in self.simulator_sedml_list_map.items():
            for sbml, sedml in zip(self.sbml_files_list, files):
                self.create_omex_archive(sbml, sedml, simulator=simulator)
