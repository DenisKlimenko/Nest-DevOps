#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, shutil, sys, subprocess

from BuildSettings import BuildSettings

class IM3Uploader:

	def __init__(self, revision, appid):
		self.BS = BuildSettings()
		self.Revision = revision
		self.ProdType = self.BS.getProductType()
		self.Brand = self.BS.getBrand()
		self.PackFile = "%s.dmg" % self.Brand
		self.Appid = appid
		if self.Appid != None:
			self.SvnRevision = self.Revision
			self.Revision = "%s_appid_%s" % (self.Revision, self.Appid)


	def copyProductToServer(self):
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

			shareDir = "%s/%s/%s/" % (self.BS.getIM3ShareRootDir(), self.Brand, self.BS.getBranch())

			os.chdir(self.BS.getInstallDir())

			if self.Appid != None:
				productDir = self.BS.getInstallDir() + os.sep + str(self.SvnRevision) + os.sep + "Mac" + os.sep + "AppID" + os.sep + str(self.Appid)
			else:
				productDir = self.BS.getInstallDir() + os.sep + str(self.Revision) + os.sep + "Mac"

			if os.path.exists(productDir) == False:
				os.makedirs(productDir)

			if os.path.exists(productDir + os.sep + outputFile):
				os.system('rm -rf "%s"' % (productDir + os.sep + outputFile))
			
			os.system("cp -R %s %s" % (productFile, productDir + os.sep + outputFile))

			if self.Appid != None:
				outputFile = "." + os.sep + str(self.SvnRevision) + os.sep + "Mac" + os.sep + "AppID" + os.sep + str(self.Appid) + os.sep + outputFile
			else:
				outputFile = "." + os.sep + str(self.Revision) + os.sep + "Mac" + os.sep + outputFile

			print "Current working dir: %s" % os.getcwd()
			uploadCMD = "rsync -avR %s %s@%s:%s" % (outputFile, self.BS.getIM3User(), self.BS.getIM3Url(), shareDir)
			print uploadCMD
			process = subprocess.Popen(uploadCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			# wait for the process to terminate
			out, err = process.communicate()
			errcode = process.returncode

			if errcode == 0:
				if os.path.exists(self.BS.getInstallDir() + os.sep + str(self.Revision)):
					shutil.rmtree(self.BS.getInstallDir() + os.sep + str(self.Revision))
					print "Product successfully uploaded to %s as %s/%s" % (self.BS.getIM3Url(), shareDir, outputFile)
			else:
				print "Product wasn't uploaded to %s" % self.BS.getIM3Url()
				sys.exit(1)
