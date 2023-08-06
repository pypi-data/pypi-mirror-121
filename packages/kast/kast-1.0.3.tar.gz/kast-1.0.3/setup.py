#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

NAME_PACKAGE_ROOT = 'pkg'

DIR_ROOT = Path(__file__).resolve().parent
DIR_PACKAGE_ROOT = DIR_ROOT / NAME_PACKAGE_ROOT

sys.path.append(str(DIR_PACKAGE_ROOT))

from kast import __app_description__, __email__, __version__, __author__, __package_name__, __app_url__


def assert_working_dir():
    currDir = Path().resolve()
    if currDir != DIR_ROOT:
        print(f"[ERROR]: Please change working directory: '{currDir}' -> '{DIR_ROOT}'")
        sys.exit(1)


def get_requirements():
    fileRequirements = DIR_ROOT / 'requirements.txt'

    if not fileRequirements.exists():
        print(f"<!> Could not find '{fileRequirements.name}' file. It will be generated.")
        from generate_requirements import generate
        generate()

    with open(fileRequirements) as fInput:
        return fInput.read().splitlines()


def get_long_description():
    fileReadme = DIR_ROOT / 'README.md'

    with open(fileReadme) as fInput:
        return fInput.read()


assert_working_dir()

kwargs = {}

try:
    from setup_qt import build_qt

    kwargs['cmdclass'] = {'build_qt': build_qt}
    kwargs['options'] = {
        'build_qt': {
            'packages': [f'{NAME_PACKAGE_ROOT}/{__package_name__}'],
            'filename_ui': '{name}.py',
        },
    }

except ImportError:
    print("<!> Could not import 'setup_qt'. Some development feature will not be available!")

setup(
    name=__package_name__,
    version=__version__,
    license="MIT",
    url=__app_url__,
    author=__author__,
    author_email=__email__,
    description=__app_description__,
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    package_dir={'': NAME_PACKAGE_ROOT},
    packages=find_packages(NAME_PACKAGE_ROOT),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    scripts=['script/kast'],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    **kwargs
)
