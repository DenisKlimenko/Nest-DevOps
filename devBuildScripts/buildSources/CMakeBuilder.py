#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, shutil

from BuildSettings import BuildSettings
from helpers.Utils import Chdir

class CMakeBuilder:

	def __init__(self, revision):
		self.BuildSettings = BuildSettings()
		self.ProjectDir = self.BuildSettings.getRepositoryPath() + os.sep + (".build-%s" % self.BuildSettings.getBuildType().replace(" ", "").replace("\"", "").lower())
		self.Revision = revision

	def exportEnivronmentParametrs(self):
		for (k, v) in self.BuildSettings.getEnvironmentExportList().items():
			os.environ["%s" % k] = "%s" % v
			os.system("echo export %s=%s" % (k,v))

	def clearPreviousBuild(self):
		if os.path.exists(self.ProjectDir):
			shutil.rmtree(self.ProjectDir)

	def buildSources(self):
		self.clearPreviousBuild()
		self.exportEnivronmentParametrs()

		os.mkdir(self.ProjectDir)

		buildDir = Chdir(self.ProjectDir)
		cmakeStr = "cmake -G %s" % self.BuildSettings.getBuildType()
		for (k, v) in self.BuildSettings.getCMakeListsParamsDict().items():
			cmakeStr += " -D%s=%s " % (k,v)
		cmakeStr += "-DMACOSX_BUNDLE_VERSION=%s " % self.Revision
		cmakeStr += self.BuildSettings.getCMakeRootDir()
		os.system("echo " + cmakeStr)
		os.system(cmakeStr)
