import docker
import os
from report_generation.config import Config

client = docker.from_env()
image = client.images.pull('ghcr.io/biosimulators/vcell:7.3.0.07')
print(image.id)
# print(client.images.list())
try:
    print(client.containers.run('ghcr.io/biosimulators/vcell', command='-v'))
except docker.errors.ContainerError as ce:
    print('something...')



def run_image(_image, _version, hash):
    client = docker.from_env()
    omex_path = os.path.join(Config.OMEX_FILE_PATH, _image)
    container = client.containers.run(image=_image, version=_version, volumes={})
    pass
