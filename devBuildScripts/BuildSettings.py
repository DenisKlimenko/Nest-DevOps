#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os

class BuildSettings:

    def __init__(self):
        self.Brand = ""
        self.Branch = "Trunk"  # Trunk or name of branch
        self.NeedUpdate = True
        self.NeedRevert = True
        self.RepositoryPath = os.path.expanduser("~/Projects/%s/%s" % (self.Brand, self.Branch))
        self.VcsType = "svn"   # svn or git
        self.ProjectVersion = "1.0.0"
        self.BuildType = "Xcode"   # Xcode or \"Unix Makefiles\"
        self.BuildConfiguration = "MinSizeRel"  # Debug, Release, MinSizeRel
        self.CMakeListsParamsDict = { "CMAKE_PREFIX_PATH" : "/usr/local/opt/qt5/"}
        self.EnvironmentExportList = {}
        self.BuildTarget = "install"
        self.InstallDir = self.RepositoryPath + os.sep + (".build-%s" % self.BuildType.replace(" ", "").replace("\"", "").lower()) + os.sep + ".%s-fancy-dmg" % self.Brand
        self.DmgResourcesDir = self.RepositoryPath + os.sep + "resources" + os.sep + "MacOSXResources" + os.sep + "fancyDmg"
        self.ProductType = "fancy dmg" # fancy dmg or package
        self.CMakeRootDir = self.RepositoryPath
        self.StorageServerLogin = ""
        self.StorageServerPassword = ""
        self.StorageServerShare = ""
        self.StorageServerName = ""
        self.StorageServerProjectsDir = "Builds" + os.sep + self.Brand + "_new" + os.sep + self.Branch + os.sep + "406"
        
        ## for fancy dmg with two apps in it

        self.IsTwoAppsInDmg = False
        self.SecondAppBrand = "VLC.app"
        self.SecondAppDir = "%s/installation/resources/static/vlc" % self.RepositoryPath

        ## for im3
        self.IM3Url = ""
        self.IM3User = ""
        self.IM3ShareRootDir = ""


    def getBrand(self):
        return self.Brand

    def getBranch(self):
        return self.Branch

    def isNeedUpdate(self):
        return self.NeedUpdate

    def isNeedRevert(self):
        return self.NeedRevert

    def getRepositoryPath(self):
        return self.RepositoryPath

    def getVcsType(self):
        return self.VcsType

    def getBuildType(self):
        return self.BuildType

    def getCMakeListsParamsDict(self):
        return self.CMakeListsParamsDict

    def getBuildTarget(self):
        return self.BuildTarget

    def getBuildConfiguration(self):
        return self.BuildConfiguration

    def getInstallDir(self):
        return self.InstallDir

    def getDmgResourcesDir(self):
        return self.DmgResourcesDir

    def getProductType(self):
        return self.ProductType

    def getCMakeRootDir(self):
        return self.CMakeRootDir

    def getProjectVersion(self):
        return self.ProjectVersion

    def getEnvironmentExportList(self):
        return self.EnvironmentExportList

    def getStorageServerLogin(self):
        return self.StorageServerLogin

    def getStorageServerPassword(self):
        return self.StorageServerPassword

    def getStorageServerShare(self):
        return self.StorageServerShare

    def getStorageServerName(self):
        return self.StorageServerName

    def getStorageServerProjectsDir(self):
        return self.StorageServerProjectsDir

    def getSecondAppBrand(self):
        return self.SecondAppBrand

    def getSecondAppDir(self):
        return self.SecondAppDir

    def getIsTwoAppsInDmg(self):
        return self.IsTwoAppsInDmg

    def getIM3Url(self):
        return self.IM3Url

    def getIM3User(self):
        return self.IM3User

    def getIM3ShareRootDir(self):
        return self.IM3ShareRootDir

    def getUpdaterBrand(self):
        return self.UpdaterBrand
