#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with user-defined path settings.

Default values:

>>> PROJECTPATH = None      # Leave it for automatic detection
>>> # PATHS: relative to the project path
>>> HTMLPATH    = 'html/'   # path for html output
>>> CIRCUITPATH = 'cir/'    # path for .asc, .net, .cir, .sch files
>>> LIBRARYPATH = 'lib/'    # path for include and library files
>>> TXTPATH     = 'txt/'    # path for text files (text2html)
>>> CSVPATH     = 'csv/'    # path for CSV files (csv2html)
>>> LATEXPATH   = 'tex/'    # path for LaTeX output saveTeX()
>>> MATHMLPATH  = 'mathml/' # path for mathML output saveMathML()
>>> IMGPATH     = 'img/'    # path for image files
"""
PROJECTPATH = None      # Leave it for automatic detection
# PATHS: relative to the project path
HTMLPATH    = 'html/'   # path for html output
CIRCUITPATH = 'cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH = 'lib/'    # path for include and library files
TXTPATH     = 'txt/'    # path for text files (text2html)
CSVPATH     = 'csv/'    # path for CSV files (csv2html)
LATEXPATH   = 'tex/'    # path for LaTeX output saveTeX()
MATHMLPATH  = 'mathml/' # path for mathML output saveMathML()
IMGPATH     = 'img/'    # path for image files


# Project information
PROJECT    = 'CSstage small-signal dynamic behavior'
AUTHOR     = 'User'
CREATED    = '2024-02-19 03:17:19.071217'
LASTUPDATE = '2024-02-19 03:28:54.166023'