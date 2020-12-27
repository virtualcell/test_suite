from report_generation.combine.omex_maker import GenOmex
from report_generation.sbml import download_sbml
from report_generation.sedml.sedml_maker import gen_sedml
import os
import subprocess

download_sbml()
gen_sedml()
omex = GenOmex()
omex.omex_gen_copasi()
omex.omex_gen_vcell()
