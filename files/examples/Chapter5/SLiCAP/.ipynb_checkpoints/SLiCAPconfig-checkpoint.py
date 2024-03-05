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
CREATED    = '2023-05-11 18:24:50.148076'
LASTUPDATE = '2023-05-17 02:41:53.665344'