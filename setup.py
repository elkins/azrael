#!/usr/bin/env python3
"""
Setup script for Azrael - Distributed Physics Simulation Engine

Installation:
    pip install -e .              # Development install
    pip install .                 # Regular install
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
def read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

# Read requirements from requirements.txt
def read_requirements():
    here = os.path.abspath(os.path.dirname(__file__))
    req_file = os.path.join(here, 'requirements.txt')
    with open(req_file, encoding='utf-8') as f:
        return [line.strip() for line in f
                if line.strip() and not line.startswith('#')]

setup(
    name='azrael',
    version='0.1.0',
    description='Distributed physics simulation engine for space robotics and multi-agent RL',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Oliver Nagy (original), George Elkins (modernization)',
    author_email='',
    url='https://github.com/elkins/azrael',
    project_urls={
        'Bug Reports': 'https://github.com/elkins/azrael/issues',
        'Source': 'https://github.com/elkins/azrael',
        'Documentation': 'https://github.com/elkins/azrael/tree/master/docs',
    },

    # Package discovery
    packages=find_packages(exclude=['demos', 'docs', 'tests']),

    # Python version requirement
    python_requires='>=3.10',

    # Dependencies
    install_requires=read_requirements(),

    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'ruff>=0.1.0',
            'mypy>=1.0.0',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },

    # Package data
    include_package_data=True,
    package_data={
        'azrael': ['LICENSE'],
    },

    # Entry points (command line scripts)
    entry_points={
        'console_scripts': [
            # Add CLI commands here if needed
            # 'azrael=azrael.cli:main',
        ],
    },

    # Classifiers for PyPI
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],

    # Keywords for discoverability
    keywords='physics simulation robotics reinforcement-learning multi-agent bullet pybullet space',

    # License
    license='AGPL-3.0',

    # Zip safe
    zip_safe=False,
)
