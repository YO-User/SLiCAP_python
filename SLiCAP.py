#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:29:52 2020

@author: anton
"""
from SLiCAPinstruction import *

class SLiCAPproject(object):
    """
    Prototype of a SLiCAPproject:
    
    - Copies the directory structure from the templates subdirectory to the
      project directory in the case it has not yet been created.
    - Creates index.html in the html directory
    - Creates the system libraries
    - Updates 'SLiCAPconfig.py'
    """
    def __init__(self, name):
        self.name = name
        self.lastUpdate = datetime.now()
        self.author = getpass.getuser()
        if not os.path.exists(ini.projectPath + 'SLiCAPconfig.py'):
            f = open(ini.installPath + 'SLiCAPconfig.py', 'r')
            txt = f.read()
            f.close()
            txt += '\n\n# Project information'
            txt += '\nPROJECT    = ' + '\'' + self.name + '\'' 
            txt += '\nAUTHOR     = ' + '\'' + self.author + '\'' 
            txt += '\nCREATED    = ' + '\'' + str(self.lastUpdate) + '\'' 
            txt += '\nLASTUPDATE = ' + '\'' + str(self.lastUpdate) + '\'' 
            f = open(ini.projectPath + 'SLiCAPconfig.py', 'w')
            f.write(txt)
            f.close()
        else:
            f = open(ini.projectPath + 'SLiCAPconfig.py', 'r')
            lines = f.readlines()[0:-1]
            f.close()
            lines.append('LASTUPDATE = ' + '\'' + str(self.lastUpdate) + '\'')
            f = open(ini.projectPath + 'SLiCAPconfig.py', 'w')
            f.writelines(lines)
            f.close()
        makeDir(ini.circuitPath)
        makeDir(ini.imgPath)
        makeDir(ini.libraryPath)
        makeDir(ini.csvPath)
        makeDir(ini.txtPath)
        makeDir(ini.htmlPath)
        makeDir(ini.htmlPath + 'img/')
        makeDir(ini.htmlPath + 'css/')
        copyNotOverwrite(ini.installPath + 'slicap.css', ini.htmlPath + 'css/slicap.css')
        copyNotOverwrite(ini.installPath + 'Grid.png', ini.htmlPath + 'css/Grid.png')
        makeDir(ini.mathmlPath)
        makeDir(ini.latexPath)
        startHTML(name)
        makeLibraries()

def makeDir(dirName):
    """
    Creates the directory 'dirName' if it does not yet exist.
    """
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return

def copyNotOverwrite(src, dest):
    """
    Copies the file 'src' to 'dest' if the latter one does not exist.
    """
    if not os.path.exists(dest):
        cp(src, dest)

def initProject(name):
    """
    Initializes a SLiCAP project.
    """
    prj = SLiCAPproject(name)
    return prj

if __name__ == '__main__':
    pass
