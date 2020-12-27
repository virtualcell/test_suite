import pkg_utils
import os
import sys
import subprocess
import re
import setuptools


try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pkg_utils"],
        check=True, capture_output=True)
    match = re.search(r'\nVersion: (.*?)\n', result.stdout.decode(), re.DOTALL)
    assert match and tuple(match.group(1).split('.')) >= ('0', '0', '5')
except (subprocess.CalledProcessError, AssertionError):
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-U", "pkg_utils"],
        check=True)

name = 'vcell_test_suite'
dirname = os.path.dirname(__file__)
package_data = {
    name: [],
}

# get package metadata
md = pkg_utils.get_package_metadata(
    dirname, name, package_data_filename_patterns=package_data)

# install package
setuptools.setup(
    name=name,
    version=md.version,
    description=(
        "Compares resultant data between VCell and COPASI"),
    long_description=md.long_description,
    url="https://github.com/virtualcell/test_suite",
    download_url='https://github.com/virtualcell/test_suite',
    author='Gnaneswara Marupilla',
    author_email="marupilla@mail.com",
    license="MIT",
    keywords='systems biology modeling simulation',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    package_data=md.package_data,
    install_requires=md.install_requires,
    extras_require=md.extras_require,
    tests_require=md.tests_require,
    dependency_links=md.dependency_links,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)
