#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: poleSplitOpAmp.py

from SLiCAP import *

fileName = 'poleSplitOpamp'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
i1.setSimType('numeric') # This substitutes C_c=0 in the element expressions
i1.setDataType('poles')
i1.setGainType('gain')
i1.setDetector('V_3')
poles = i1.execute().poles
print("Poles:",poles)

result = i1.execute()
denomSym = result.denom
i1.defPars({'R_a':'10k', 'C_a':'100p', 'tau':'100u', 'A_0':'100k'})

htmlPage('plots')

i1.setStepVar('C_c')
i1.setStepStart(0)
i1.setStepStop(2e-12)
i1.setStepNum(6)
i1.setStepMethod('lin')
i1.stepOn()
i1.setSimType('numeric')
i1.setDataType('poles')
i1.setGainType('gain')
i1.setSource('V1')
pSplitPZ = plotPZ('pSplitPZ', 'Pole splitting', i1.execute(), xmin=-5, xmax=0, ymin =-1, ymax = 1, xscale='M', show=True)
fig2html(pSplitPZ, 800)
pSplitPZlow = plotPZ('pSplitPZlow', 'Pole splitting dominant pole', i1.execute(), xmin=-2, xmax=0, ymin =-1, ymax = 1, xscale='k', show=True)
fig2html(pSplitPZ, 800)
i1.setDataType('laplace')
htmlPage('Magnitude plot')
pSplitBode = plotSweep('pSplitBodeMag', 'Pole splitting', i1.execute(), 10, 10e6, 200, funcType='dBmag', show = True)
fig2html(pSplitBode, 800)