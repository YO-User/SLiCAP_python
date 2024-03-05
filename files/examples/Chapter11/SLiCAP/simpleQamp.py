#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file: simpleQamp.py

from SLiCAP import *

fileName = 'simpleQamp'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('High-pass cut-off design')
i1.setSource('I1')
i1.setDetector('V_2')
i1.setLGref('E1')
i1.setSimType('numeric')
i1.setGainType('servo')
i1.setDataType('laplace')
result = i1.execute()
exprGain = result.laplace
eqn2html('S', exprGain);
gain, numerCoeffs, denomCoeffs = coeffsTransfer(exprGain)
order          = len(denomCoeffs) - 1
omegaLow       = denomCoeffs[0]/denomCoeffs[-1]
f_l            = 1e3
A0min          = sp.solve(omegaLow - (2*sp.pi*f_l)**(1/order))[0]
A_min = sp.Symbol('A_min')
text2html('In order to meet the requirement for $f_{\\ell}$ we need a minimum value $A_{\\min}$ for the DC gain $A_0$ of the controller:');
eqn2html(A_min, A0min);
i1.defPar('A_0', A0min);
htmlPage('Bode plots simpleQamp')
S = i1.execute()
i1.setGainType('loopgain')
L = i1.execute()
i1.setGainType('asymptotic')
A = i1.execute()
i1.setGainType('direct')
D = i1.execute()
i1.setGainType('gain')
G = i1.execute()
figMag = plotSweep('magQamp', 'Magnitude characteristics', [A, L, S, D, G], 10, 10e6, 200, funcType='mag', show=True)
fig2html(figMag, 800)
figPhase = plotSweep('phaseQamp', 'Magnitude characteristics', [A, L, S, D, G], 10, 10e6, 200, funcType='phase', show=True)
fig2html(figPhase, 800);