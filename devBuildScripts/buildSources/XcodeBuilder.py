#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os
from helpers.Utils import Chdir
from BuildSettings import BuildSettings

class XcodeBuilder:
	def __init__(self):
		self.BuildSettings = BuildSettings()
		self.ProjectDir = self.BuildSettings.getRepositoryPath() + os.sep + ".build-xcode"

	def buildProject(self):
		if not os.path.exists(self.ProjectDir):
			os.mkdir(self.ProjectDir)
		projdir = Chdir(self.ProjectDir)
		print "pwd %s" % os.getcwd()
		os.system("xcodebuild -project %s.xcodeproj -target %s -configuration %s" % (self.BuildSettings.getBrand().lower(), self.BuildSettings.getBuildTarget(), self.BuildSettings.getBuildConfiguration()))
