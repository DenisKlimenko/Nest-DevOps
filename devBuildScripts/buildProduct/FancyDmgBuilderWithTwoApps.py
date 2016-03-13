#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, shutil, stat, sys

from helpers.Utils import Chdir
from BuildSettings import BuildSettings

class FancyDmgBuilderWithTwoApps:

	def __init__(self):
		self.BuildSettings = BuildSettings()
		self.Brand = self.BuildSettings.getBrand()
		self.ProjectDir = ".build-%s" % self.BuildSettings.getBuildType().replace(" ", "").replace("\"", "").lower()
		self.ApplicationDir = self.BuildSettings.getRepositoryPath() + os.sep + self.ProjectDir + os.sep + "bin"
		self.ResourcesDir = self.BuildSettings.getDmgResourcesDir()

		self.ScriptDir = os.getcwd()


	def buildProduct(self):
		os.mkdir(self.BuildSettings.getInstallDir())
		os.chdir(self.BuildSettings.getInstallDir())
		dmgDir = "%s_dmg" % self.Brand
		if os.path.exists(dmgDir):
			shutil.rmtree(dmgDir)

		os.mkdir(dmgDir)
		
		chInDmgDir = Chdir(dmgDir)
		
		shutil.copytree(self.ApplicationDir + os.sep + "%s.app" % self.Brand, "%s.app" % self.Brand)
		os.system("svn export %s/%s %s" % (self.BuildSettings.getSecondAppDir(), self.BuildSettings.getSecondAppBrand(), self.BuildSettings.getSecondAppBrand()))
		
		del chInDmgDir
		
		self.unmountDMGs(self.Brand)
		self.makeDMG(dmgDir, self.Brand, "temp")
		shutil.rmtree(dmgDir)
		self.mountDMG("temp")
		self.makeFancyOfDMG(self.Brand)
		self.finalizeDMG(self.Brand)
		self.compressDMG("temp", self.Brand)

	def unmountDMGs(self, title):
		from commands import getoutput

		os.system("killall %s" % title)
		done = False
		while not done:
			output = getoutput("umount /Volumes/%s" % title)
			if output == '':
				continue
			elif output.find('not currently mounted') != -1:
				done = True
			else:
				print("Error: failed unmount old %s dmg", title)
				sys.exit(-1)

	def makeDMG(self, source, title, output):
		if os.path.exists(source + os.sep + ".Trashes"):
			shutil.rmtree(source + os.sep + ".Trashes")

		os.system("""hdiutil create \
			-srcfolder "%s" \
			-volname "%s"   \
			-fs HFS+        \
			-fsargs "-c c=64,a=16,e=16" \
			-format UDRW    \
			%s.dmg""" % (source, title, output))
    
	def mountDMG(self, dmg):
		os.system("""$(hdiutil attach   \
			-readwrite  \
			-noverify "%s.dmg" \
			| egrep '^/dev/' \
			| sed 1q \
			| awk '{print $1}')""" % (dmg))
    
	def makeFancyOfDMG(self, dmg):
		from appscript import *
		
		ch = Chdir("/Volumes/%s" % dmg)
		
		finder = app('Finder')
		finder.run()
		
		folder = finder.disks[dmg]
		folder.open()
		
		finder.make(new=k.alias, at=folder.get(), to=finder.startup_disk.folders['Applications'].get())
		shutil.copyfile(self.ResourcesDir + os.sep + "applicationIcon.png", "applications_icon.png")
		
		os.system("sips -i applications_icon.png")
		os.system("DeRez -only icns applications_icon.png > tempincs.rsrc")
		os.system("SetFile -a C Applications")
		os.system("Rez -append tempincs.rsrc -o Applications")
		
		if os.path.exists("applications_icon.png"):
		    os.remove("applications_icon.png")
		
		if os.path.exists("tempincs.rsrc"):
		    os.remove("tempincs.rsrc")
		
		shutil.copyfile(self.ResourcesDir + os.sep + "background.png", ".background.png")
		
		bundleName = '%s.app' % self.Brand

		folder.container_window.current_view.set(k.icon_view)
		folder.container_window.bounds.set([200, 100, 1200, 640])
		viewOptions = folder.container_window.icon_view_options
		viewOptions.arrangement.set(k.not_arranged)
		viewOptions.icon_size.set(128)
		viewOptions.background_picture.set(folder.items['.background.png'])
		folder.container_window.items[bundleName].position.set([260,225])
		folder.container_window.items['Applications'].position.set([580,225])
		folder.container_window.items[self.BuildSettings.getSecondAppBrand()].position.set([900, 225])
		folder.close()
		
		os.system("/Developer/Tools/SetFile -a V /Volumes/%s/.background.png" % dmg)
		os.chmod("/Volumes/%s/%s.app/Contents/MacOS/%s" % (dmg, self.Brand, self.Brand), stat.S_IRWXU | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IROTH)
		# os.chmod("/Volumes/%s/background.png" % dmg, stat.UF_HIDDEN)
    
	def finalizeDMG(self, dmg):
		mountedDMG = "/Volumes/%s" % dmg
		#os.system("chmod -Rf go-w " + mountedDMG)
		#os.chmod(mountedDMG, stat.S_IRWXG | stat.S_IRWXO | ~stat.S_IWOTH)
		os.system("sync")
		os.system("sync")
		os.system("hdiutil detach %s" % mountedDMG)

	def compressDMG(self, dmg, output):
		os.system("hdiutil convert %s.dmg -format UDZO -imagekey zlib-level=9 -o %s" % (dmg, output))

		if os.path.exists(dmg + ".dmg"):
			os.remove(dmg + ".dmg")