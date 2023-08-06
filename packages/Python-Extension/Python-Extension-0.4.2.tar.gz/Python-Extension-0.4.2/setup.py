from setuptools import *

setup(
    name = 'Python-Extension',
    version = '0.4.2',
    description = 'Python extension functions',
    license = 'GPL',
    author = 'Yile Wang',
    packages = find_packages(),
    python_requires = '>=3.10',
    module_requires = ['python-docx>=0.8'],
    include_package_data = True
    )
