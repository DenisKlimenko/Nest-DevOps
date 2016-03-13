#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'


from vcs.SvnUpdater import SvnUpdater
from BuildSettings import BuildSettings
from buildSources.CMakeBuilder import CMakeBuilder
from buildSources.UnixMakefilesBuilder import UnixMakefilesBuilder
from buildSources.XcodeBuilder import XcodeBuilder
from buildProduct.FancyDmgBuilder import FancyDmgBuilder
from buildProduct.FancyDmgBuilderWithTwoApps import FancyDmgBuilderWithTwoApps
from storageHelper.SMBStorageMounter import SMBStorageMounter
from storageHelper.IM3Uploader import IM3Uploader

if __name__ == '__main__':

################
# Update sorces
################

	BuildSettings = BuildSettings()
	
	if BuildSettings.getVcsType() == "svn":
		vcsClient = SvnUpdater(BuildSettings.getRepositoryPath())
	elif BuildSettings.getVcsType() == "git":
		vcsClient = "git"

	if BuildSettings.isNeedRevert():
		vcsClient.revertSources()
	
	if BuildSettings.isNeedUpdate():
		vcsClient.updateSources()

	revision = vcsClient.getRevision()

################
# Build project
################

	CMakeBuilder(revision).buildSources()

	buildType = BuildSettings.getBuildType()
	if buildType == "\"Unix Makefiles\"":
		projectBuilder = UnixMakefilesBuilder()
	elif buildType == "Xcode":
		projectBuilder = XcodeBuilder()

	projectBuilder.buildProject()

###############
# Make product
###############

	if BuildSettings.getProductType() == "fancy dmg":
		if BuildSettings.getIsTwoAppsInDmg():
			productBuilder = FancyDmgBuilderWithTwoApps()
		else:
			productBuilder = FancyDmgBuilder()

	productBuilder.buildProduct()

##########################
# Copy product to storage
##########################

	SMBStorageMounter(revision, None).copyProductToServer()
	IM3Uploader(revision, None).copyProductToServer()
