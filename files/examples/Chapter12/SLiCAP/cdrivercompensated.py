#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: cdrivercompensated.py

from SLiCAP import *

fileName = 'cdrivercompensated'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
i1.setSource('V1')
i1.setDetector('V_out1')
i1.setLGref('E_O1')
i1.setSimType('numeric')
i1.setDataType('pz')
i1.setGainType('gain')
listPZ(i1.execute())
i1.setDataType('poles')
i1.setGainType('servo')
i1.setStepVar('R_phz')
i1.setStepStart(0)
i1.setStepStop(0.25)
i1.setStepNum(5)
i1.setStepMethod('lin')
i1.stepOn()
locusR_phz = plotPZ('RootLocusRphz', 'Root locus Rphz', i1.execute(), xmin=-300, xmax=0, ymin=-150, ymax=150, xscale='k', yscale='k', show=True)
fig2html(locusR_phz, 600)
i1.stepOff()
i1.setGainType('gain')
i1.setSource('I1')
i1.setDataType('laplace')
ZoutPassiveESR = i1.execute()
ZoutPassiveESR.label = 'passiveESR'
i1.setSource('I2');
i1.setDetector('V_out2')
ZoutPassive = i1.execute()
ZoutPassive.label = 'passive'
# Use the circuit for active compensation
i1.setCircuit('activePHZ.cir')
i1.setSource('I1')
i1.setDetector('V_out')
i1.setLGref('E_O1')
i1.setSimType('numeric')
i1.setDataType('pz')
i1.setGainType('gain')
pzList = i1.execute()
listPZ(pzList);
i1.setDataType('poles')
i1.setGainType('servo')
i1.setStepVar('A_0')
i1.setStepStart(0);
i1.setStepStop('300k')
i1.setStepNum(100)
i1.setStepMethod('lin')
i1.stepOn()
plotPZ('RLactive', 'RootLocus', i1.execute(), xmin=-2, xmax=0, ymin=-1, ymax=1, xscale='M', yscale='M', show=True)
i1.stepOff()
i1.setGainType('gain')
i1.setDataType('laplace')
ZoutActive = i1.execute()
ZoutActive.label = 'active'
htmlPage('$Z_{out}$')
Zout = plotSweep('Z-out', 'Magnitude $Z_{out}$', [ZoutPassive, ZoutPassiveESR, ZoutActive], 10, 10e6, 200, yUnits='$\\Omega$', show=True)
fig2html(Zout, 800)