#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: QampBias.py

from SLiCAP import *

fileName='QampBias'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName+ '.cir')
htmlPage('Circuit data')
netlist2html(fileName+ '.cir')
i1.setSource('I1')
i1.setDetector('V_2')
i1.setSimType('numeric')
i1.setGainType('gain')
i1.setDataType('laplace')
GainUncomp = i1.execute()
GainUncomp.label = 'uncomp.' # Assign a plot label to this result
i1.defPar('C_c','220p')
GainComp = i1.execute()
GainComp.label = 'phz comp.' # Assign a plot label to this result
htmlPage("Bode plots charge amplifier with feedback biasing")
dBmag = plotSweep('dBmagQamp', 'Charge amplifier with feedback biasing', [GainUncomp, GainComp], 100, 10e6, 500, funcType='dBmag', show=True)
phase = plotSweep('phaseQamp', 'Charge amplifier with feedback biasing', [GainUncomp, GainComp], 100, 10e6, 500, funcType='phase', show=True)
fig2html(dBmag, 800)
fig2html(phase, 800)
i1.setDataType('poles')
i1.stepOn()
i1.setStepVar('C_c')
i1.setStepStart(0)
i1.setStepStop('500p')
i1.setStepNum(20)
i1.setStepMethod('lin')
pzPlot = plotPZ('RLqAmp', 'Biased charge amplifier', i1.execute(), xmin=-3, xmax=0, ymin=-1.5, ymax=1.5, xscale='k', yscale='k', show=True)