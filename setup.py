#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Template Processor

Template Processor (TP), created as a part of "Model-Based Execution Platform 
for Space Applications" project (contract 4000146882/24/NL/KK) financed by 
the European Space Agency.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='template-processor',
    version='0.0.1',
    description='Template processing engine for TASTE Document Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='N7 Space',
    author_email='mkurowski@n7space.com',
    url='https://github.com/n7space/template-processor',
    license='European Space Agency Public License (ESA-PL) Permissive – v2.3',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "mako==1.3.10",
        "python-docx==1.2.0",
        "beautifulsoup4==4.12.3",
        "markdown2==2.5.4"
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'template-processor=templateprocessor.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'License :: ESA-PL Permissive v2.3',
        'Operating System :: Linux'
    ],
    zip_safe=False,
)
