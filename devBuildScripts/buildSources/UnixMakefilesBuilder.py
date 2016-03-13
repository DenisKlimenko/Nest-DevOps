#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os

from helpers.Utils import Chdir
from BuildSettings import BuildSettings

class UnixMakefilesBuilder:

	def buildProject(self):
		projectDir = Chdir(BuildSettings().getRepositoryPath() + os.sep + ".build-%s" % BuildSettings().getBuildType().replace(" ", "").replace("\"", "").lower())
		os.system("make -j4")
		os.system("make install")
