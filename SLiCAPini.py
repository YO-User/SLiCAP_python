#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from SLiCAPconfig import *
import sympy as sp
import numpy as np
import ply.lex as lex
from shutil import copy2 as cp
from time import time
from datetime import datetime
import re
import subprocess
import os
import getpass
import platform


# Type conversions
# These are the only globals. Read only!
LAPLACE         = sp.Symbol(LAPLACE)
FREQUENCY       = sp.Symbol(FREQUENCY)
OMEGA           = sp.Symbol(OMEGA)
SCALEFACTORS    =  {'y':'-24','z':'-21','a':'-18','f':'-15','p':'-12','n':'-9',
                    'u':'-6','m':'-3','k':'3','M':'6','G':'9','T':'12','P':'15',
                    'E':'18','Z':'21','Y':'24'} 

class settings(object):
    """
    Class with global variables that can be modified from within other modules.
    """
    def __init__(self):
        self.installPath  = None # Directory with SLiCAP python script files
        self.projectPath  = None # Directory with SLiCAP project script files
        self.htmlPath     = None # Directory with SLiCAP HTML output
        self.circuitPath  = None # Directory with SLiCAP project circuit files
        self.libraryPath  = None # Directory with SLiCAP user libraries
        self.txtPath      = None # Directory with text files for HTML output
        self.csvPath      = None # Directory with csv files for HTML tables
        self.latexPath    = None # Directory for LaTeX output
        self.mathmlPath   = None # Directory fro mathML output
        self.imgPath      = None # Directory with images for HTML output
        self.htmlIndex    = None # Active HTML index page
        self.htmlPage     = None # Active HTML page
        self.htmlPrefix   = None # Active HTML prefix
        self.htmlLabels   = None # Dict with HTML labels:
                                 #    key   = labelName
                                 #    value = pageName
        self.htmlEqLabels = None # Dict with HTML equation labels:
                                 #    key   = labelName
                                 #    value = pageName
        self.htmlPages    = None # List with names of HTML pages
        # Add plot globals here!

# Create an instance of globals
ini = settings()
# Automatic detection of install and project paths
# Get the installation path
if platform.system() =='Linux' or platform.system() =='Darwin':
        ini.installPath = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/'
if platform.system() =='Windows':
        ini.installPath = ''.join(os.path.realpath(__file__).split('/')[0:-1]) + ''

# Get the project path (the path of the script that imported SLiCAP.ini)
ini.projectPath = os.path.abspath('.') + '/'
# Copy path settings from user configuration
ini.htmlPath    = ini.projectPath + HTMLPATH
ini.circuitPath = ini.projectPath + CIRCUITPATH
ini.libraryPath = ini.projectPath + LIBRARYPATH
ini.txtPath     = ini.projectPath + TXTPATH
ini.csvPath     = ini.projectPath + CSVPATH
ini.latexPath   = ini.projectPath + LATEXPATH
ini.mathmlPath  = ini.projectPath + MATHMLPATH
ini.imgPath     = ini.projectPath + IMGPATH
# Copy plot globals here!