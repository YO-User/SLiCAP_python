#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:11:37 2021

@author: anton
"""
from SLiCAP import *

fileName = 'RL2_1'
#prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('Root locus plot: ', fileName)
i1.setSource('V1')
i1.setDetector('V_2')
i1.setLGref('E1')
i1.setSimType('numeric')
i1.setGainType('loopgain')
i1.setDataType('pz')
pzL = i1.execute()

i1.setGainType('servo')
i1.setDataType('poles')
i1.stepOn()
i1.setStepVar('A_0')
i1.setStepStart(0)
i1.setStepStop(100)
i1.setStepMethod('lin')
i1.setStepNum(500)
plsS = i1.execute()

figPZ = plotPZ(fileName, fileName, [plsS, pzL], xmin=-400, xmax=0, ymin=-200, ymax=200, show=True)
fig2html(figPZ, 500)