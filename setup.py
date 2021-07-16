from setuptools import setup, find_packages
from os import popen

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with popen('git describe') as s:
     version= s.read().strip()


setup(
    name='funwavetvdtools',
    version=version,
    description='Tools for preprocessing and postprocessing data for FUNWAVE-TVD',
    long_description=readme,
    author='Michael-Angelo Y.-H. Lam',
    author_email='michaelangelo.yh.lam@gmail.com',
    url='https://github.com/mayhl/FUNWAVE-TVD-Python-Tools',
    license=license,
    package_dir = {'': "funwavetvdtools" },
    packages=find_packages(where="funwavetvdtools")
)

