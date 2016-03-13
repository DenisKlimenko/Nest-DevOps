#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os, sys

try:
	import pysvn
except:
	print("Please install pysvn")
	sys.exit(-1)

class SvnUpdater:

	def __init__(self, repositoryPath):
		self.path = repositoryPath
		self.client = pysvn.Client()

		try:
			if os.path.isdir(self.path) and os.path.exists(self.path):
				print ('svn folder: ' + self.path)
				print ('svn url: ' + self.client.info(self.path).url)
				print ('svn current version: ' + str(self.client.info(self.path).commit_revision.number))
			else:
				print (self.path + ' not a direectory or not exist')
				sys.exit(-1)
		except pysvn.ClientError as e:
			print ("location exists but is not under svn-control");
			sys.exit(-1)


	def updateSources(self):
		os.system("svn update " + self.path)

	def revertSources(self):
		self.client.revert(self.path, all)

	def getRevision(self):
		revision = self.client.info(self.path).commit_revision.number
		return revision

