from setuptools import find_packages, setup

setup(
    name='cr-features',
    #packages=find_packages(include=['CalculatingFeatures']),
    package_dir = {'': 'CalculatingFeatures'},
    py_modules = ["helper_functions"],
    version='0.1.0',
    description='A library for calculating features suitable for context recognition',
    author='Matjaž Bostič, Vito Janko',
    license='MIT',
    install_requires=[],
)