#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, shutil, stat, sys, commands

from helpers.Utils import Chdir
from BuildSettings import BuildSettings

class FancyDmgBuilder:

	def __init__(self):
		self.BuildSettings = BuildSettings()
		self.Brand = self.BuildSettings.getBrand()
		self.ProjectDir = ".build-%s" % self.BuildSettings.getBuildType().replace(" ", "").replace("\"", "").lower()
		self.ApplicationDir = self.BuildSettings.getRepositoryPath() + os.sep + self.ProjectDir + os.sep + "bin"
		self.ResourcesDir = self.BuildSettings.getDmgResourcesDir()

		self.ScriptDir = os.getcwd()


	def buildProduct(self):
		if not os.path.exists(self.BuildSettings.getInstallDir()):
			os.mkdir(self.BuildSettings.getInstallDir())
		else:
			if os.path.exists(self.BuildSettings.getInstallDir() + os.sep + self.Brand + ".dmg"):
				os.remove(self.BuildSettings.getInstallDir() + os.sep + self.Brand + ".dmg")
			if os.path.exists(self.BuildSettings.getInstallDir() + os.sep + "temp.dmg"):
				os.remove(self.BuildSettings.getInstallDir() + os.sep + "temp.dmg")
		os.chdir(self.BuildSettings.getInstallDir())
		dmgDir = "%s_dmg" % self.Brand
		if os.path.exists(dmgDir):
			shutil.rmtree(dmgDir)

		os.mkdir(dmgDir)
		
		chInDmgDir = Chdir(dmgDir)
		
		shutil.copytree(self.ApplicationDir + os.sep + "%s.app" % self.Brand, "%s.app" % self.Brand)
		
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
		
		bundleName = '%s.app' % self.Brand

		fancyDMGBuildCmd = """
tell application "Finder"
	tell disk "%s"
		open
		set current view of container window to icon view
		set toolbar visible of container window to false
		set statusbar visible of container window to false
		set the bounds of container window to {200, 100, 1080, 640}
		set theViewOptions to the icon view options of container window
		set arrangement of theViewOptions to not arranged
		set icon size of theViewOptions to 128
		set background picture of theViewOptions to POSIX file "%s"
		do shell script "ln -s /Applications /Volumes/%s/Applications"
		set position of item "%s" of container window to {260, 225}
		set position of item "Applications" of container window to {580, 225}
		set position of item ".DS_Store" of container window to {300, 800}
		set position of item ".fseventsd" of container window to {350, 800}
		set position of item ".Trashes" of container window to {400, 800}
		close
		open
		update without registering applications
		delay 5
	end tell
end tell
""" % (dmg, self.ResourcesDir + os.sep + "background.png", dmg, bundleName)

		status, output = commands.getstatusoutput("echo '%s' | osascript" % fancyDMGBuildCmd)
		if status != 0:
			print "Errors during fancy dmg build:\n%s" % output
			sys.exit(status)
		
		os.chmod("/Volumes/%s/%s.app/Contents/MacOS/%s" % (dmg, self.Brand, self.Brand), stat.S_IRWXU | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH | stat.S_IROTH)
    
	def finalizeDMG(self, dmg):
		mountedDMG = "/Volumes/%s" % dmg
		#os.system("chmod -Rf go-w " + mountedDMG)
		#os.chmod(mountedDMG, stat.S_IRWXG | stat.S_IRWXO | ~stat.S_IWOTH)
		os.system("sync")
		os.system("sync")
		os.system("hdiutil detach -force %s" % mountedDMG)

	def compressDMG(self, dmg, output):
		os.system("hdiutil convert %s.dmg -format UDZO -imagekey zlib-level=9 -o %s" % (dmg, output))

		if os.path.exists(dmg + ".dmg"):
			os.remove(dmg + ".dmg")
