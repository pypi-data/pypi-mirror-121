#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import re
import os
import sys

# In this way, we are sure we are getting
# the installer's version of the library
# not the system's one
setupBaseDir = os.path.dirname(__file__)
sys.path.insert(0, setupBaseDir)

from fairtracks_validator import version as fairtracks_validator_version

# Populating the long description
with open(os.path.join(setupBaseDir, "README.md"), "r") as fh:
	long_description = fh.read()

# Populating the install requirements
with open(os.path.join(setupBaseDir, 'requirements.txt')) as f:
	requirements = []
	egg = re.compile(r"#[^#]*egg=([^=&]+)")
	for line in f.read().splitlines():
		m = egg.search(line)
		requirements.append(line  if m is None  else m.group(1))


setuptools.setup(
	name="fairtracks_validator",
	version=fairtracks_validator_version,
	scripts=["fairGTrackJsonValidate.py"],
	author="José Mª Fernández",
	author_email="jose.m.fernandez@bsc.es",
	description="FAIRtracks JSON Validator",
	license="LGPLv2",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/fairtracks/fairtracks_validator_python",
	project_urls={
		"Bug Tracker": "https://github.com/fairtracks/fairtracks_validator_python/issues"
	},
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.6",
)
