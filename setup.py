from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pycrypt2',
    version='1.0.0',
    description='An automated classical cryptanalysis tool written in Python',
    long_description=readme,
    author='James Tan',
    url='https://github.com/JamesT44/pycrypt2',
    license=license,
    packages=find_packages()
)
