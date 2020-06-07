#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:10:18 2020

@author: anton
"""

LOGFILE         = True
LANGUAGE        = 'english' # Language for error and warnings:
                            # not yet implemented
DISP            = 4         # Numner of digits for floats in output
MATHJAXLOCAL    = False     # Will be ignored, later it will be replaced with
                            # a selection between mathml and MatJax cloud

LAPLACE         = 's'       # Laplace veriable
FREQUENCY       = 'f'       # Frequency in Hz
OMEGA           = 'omega'   # Frequency in rad/s
MAXRECSUBST     = 10        # Maximum number of recursic=ve substitutions
HZ              = True      # Display method for frequency on HTML pages:
                            # True if frequency in Hz, else: False

# PATHS: relative to the project path
HTMLPATH        = 'html/'   # path for html output
CIRCUITPATH     = 'cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH     = 'lib/'    # path for include and library files
TXTPATH         = 'txt/'    # path for text files (text2html)
CSVPATH         = 'csv/'    # path for CSV files (csv2html)
LATEXPATH       = 'tex/'    # path for LaTeX output saveTeX()
MATHMLPATH      = 'mathml/' # path for mathML output saveMathML()
IMGPATH         = 'img/'    # path for image files

# Default plot settings
figureAxisHeight= 4
figureAxisWidth = 6
defaultColors   = ('r','b','g','c','m','y','k')
defaultMarkers  = ['']
tableFileType   = 'csv'
figureFileType  = 'svg'
axisXscale      = 'linear'    # Scale for the x-axis can be 'linear' or 'log'
axisYscale      = 'linear'    # Scale for the y-axis can be 'linear' or 'log'
legendLoc       = 'best'

# Project information
PROJECT    = 'My first SLiCAP project'
AUTHOR     = 'anton'
CREATED    = '2020-06-05 12:53:28.334315'
LASTUPDATE = '2020-06-05 18:56:25.333244'