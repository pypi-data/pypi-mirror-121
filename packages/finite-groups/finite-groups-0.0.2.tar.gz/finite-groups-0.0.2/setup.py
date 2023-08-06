#!/usr/bin/env python3
#
# Copyright (C) 2021 Cris Torres <cristobal_javier@hotmail.com>
# MIT License

import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="finite-groups",
    version="0.0.2",
    description="Finite Groups Computations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "GitHub": "https://github.com/CrisLeaf/finite-groups",
    },
    author="Cris Torres",
    author_email="cristobal_javier@hotmail.com",
    license="MIT License",
    packages=["fgroups"],
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)

