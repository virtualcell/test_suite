from setuptools import setup
import setuptools

setup(
    name='vcell_automation',
    version='0.0.1',
    description='Test suite comparing the results across',
    url='https://github.com/virtualcell',
    author='Gnaneswara Marupilla',
    author_email='marupilla@mail.com',
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
    ],
)
