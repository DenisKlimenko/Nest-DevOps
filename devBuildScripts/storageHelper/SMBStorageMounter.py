#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, shutil, sys

from BuildSettings import BuildSettings

class SMBStorageMounter:

	def __init__(self, revision, appid):
		self.BS = BuildSettings()
		self.MountDir = self.BS.getRepositoryPath() + os.sep + "mount"
		self.Revision = revision
		self.ProdType = self.BS.getProductType()
		self.Brand = self.BS.getBrand()
		self.Appid = appid
		if self.Appid != None:
			self.SvnRevision = self.Revision
			self.Revision = "%s_appid_%s" % (self.Revision, self.Appid)


	def mountStorage(self):
		self.unmountShare()
		self.unmountStorage()
		if not os.path.exists(self.MountDir):
			os.mkdir(self.MountDir)
		
		os.system("mount_smbfs //%s:%s@%s/%s %s" % (	self.BS.getStorageServerLogin(),
													self.BS.getStorageServerPassword(),
													self.BS.getStorageServerName(),
													self.BS.getStorageServerShare(),
													self.MountDir))
		
		print "mount_smbfs //%s:%s@%s/%s %s" % (	self.BS.getStorageServerLogin(),
													self.BS.getStorageServerPassword(),
													self.BS.getStorageServerName(),
													self.BS.getStorageServerShare(),
													self.MountDir)

	def unmountStorage(self):
		print "hdiutil detach \"%s\" -debug -force" % self.MountDir
		os.system("hdiutil detach \"%s\" -debug -force" % self.MountDir)
		
		if os.path.exists(self.MountDir):
			if os.listdir(self.MountDir) == [] or os.listdir(self.MountDir) == [".DS_Store"]:
				print "Can be deleted"
				shutil.rmtree(self.MountDir)
			else:
				print "Directory is not empty because of it contain %s" % os.listdir(self.MountDir)
				sys.exit("Mount directory cann't be deleted")

	def unmountShare(self):
		for files in os.listdir("/Volumes"):
			if files in ["Macintosh HD2", ".DS_Store", "Server HD", "WD_Backup", "Time Machine Backups", "Time Capsule"]:
				print "found %s" % files
				continue
			else:
				print "hdiutil detach \"/Volumes/%s\" -debug -force" % files
				os.system("hdiutil detach \"/Volumes/%s\" -debug -force" % files)

	def copyProductToServer(self):
		self.mountStorage()

		outputDir = self.MountDir + os.sep + self.BS.getStorageServerProjectsDir()

		if os.path.exists(outputDir) == False:
			os.makedirs(outputDir)

		if self.Appid != None:
			outputDir = outputDir + os.sep + "%s" % self.SvnRevision + os.sep + "Mac" + os.sep + "AppID" + os.sep + "%s" % self.Appid
		else:
			outputDir = outputDir + os.sep + "%s" % self.Revision + os.sep + "Mac"

		if not os.path.exists(outputDir):
			os.makedirs(outputDir)
		
		print "Final output directory: %s" % outputDir

		if self.ProdType == "fancy dmg":
			installerTypeList = ["Nevermind"]
		elif self.ProdType == "package":
			installerTypeList = ["Offline", "Online", "Pack", "Uninstaller"]
		
		for installerType in installerTypeList:
			if self.ProdType == "fancy dmg":
				productFile = "%s.dmg" % self.Brand
			elif self.ProdType == "package":
				if installerType in ["Offline", "Online"]:
					productFile = "%sInstaller.pkg" % installerType
				elif installerType == "Pack":
					productFile = "%s.dmg" % self.Brand.lower()
				elif installerType == "Uninstaller":
					productFile = "Uninstaller.zip"


			if self.ProdType == "fancy dmg":
				outputFile = "%sSetup.dmg" % self.Brand
			elif self.ProdType == "package":
				if installerType == "Offline":
					outputFile = "%sInstaller-%s.pkg" % (self.Brand, self.Revision)
				elif installerType == "Online":
					outputFile = "%sInstallerStub-%s.pkg" % (self.Brand, self.Revision)
				elif installerType == "Pack":
					outputFile = "%s.dmg" % self.Brand.lower()
				elif installerType == "Uninstaller":
					outputFile = "Uninstaller.zip"
				else:
					sys.exit("Unknown installer type: %s" % installerType)

			outputFile = outputDir + os.sep + outputFile
				
			if os.path.exists(self.BS.getInstallDir() + os.sep + productFile): 		#In case there is no product file in install dir no action will be done
				if os.path.exists(outputFile):
					os.system('rm -rf "%s"' % outputFile)

				os.chdir(self.BS.getInstallDir())

				os.system('cp -R "%s" "%s"' % (productFile, outputFile))

		self.unmountStorage()
			