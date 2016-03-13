#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Denis'

import os

class Chdir:
    def __init__(self, newPath):
        self.oldPath = os.getcwd()
        os.chdir(newPath)

    def __del__(self):
        os.chdir(self.oldPath)