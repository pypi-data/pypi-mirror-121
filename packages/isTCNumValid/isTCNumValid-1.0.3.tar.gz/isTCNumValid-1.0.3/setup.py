#!/usr/bin python3
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='isTCNumValid',
    version='1.0.3',
    license='MIT',
    author="Cagatay URESIN",
    author_email='cagatayuresin@gmail.com',
    description="A module can say a TCNum is valid or not according to offical TCNum algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_dir={'': 'src'},
    url='https://github.com/cagatayuresin/isTCNumValid',
    keywords='tc, turkey, turkish, citizen, number',
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         ],
)