from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cr-features',
    packages=find_packages(include=['CalculatingFeatures']),
    #package_dir = {'': 'CalculatingFeatures'},
    #py_modules = ["helper_functions"],
    version='0.1.1',
    description='A library for calculating features suitable for context recognition',
    author='Matjaž Bostič, Vito Janko',
    author_email="vito.janko@ijs.si",
    long_description="long_description",
    long_description_content_type="text/markdown",
    license='MIT',
    install_requires=[],
)