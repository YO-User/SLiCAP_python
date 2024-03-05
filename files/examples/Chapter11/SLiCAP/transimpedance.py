#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# file: transimpedance.py

from SLiCAP import *

fileName = 'transimpedance'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('Example controller GB product requirements')
i1.setSimType('numeric')
i1.setDataType('laplace')
i1.setSource('I1')
i1.setDetector('V_2')

i1.setLGref('E1')
i1.setGainType('loopgain')
result = i1.execute()
#
gain, numerCoeffs, denomCoeffs = coeffsTransfer(result.laplace)
if len(numerCoeffs) > 1:
  text2html('Zeros found, GB determination method not valid.')
else:
  text2html('Found the nonzero DC loop gain.')
if denomCoeffs[0] == 0:
  text2html('Found poles in the origin, GB determination method not valid.')
#
LP = sp.symbols('LP')
text2html('The DC loop gain equals:')
eqn2html('L_DC', gain)

if len(denomCoeffs) == 1:
  text2html('No poles found, GB determination method not valid.')
LPproduct = -gain/denomCoeffs[-1]

text2html('The loop gain-poles product is found as:')
eqn2html(LP, LPproduct)
order = len(denomCoeffs) - 1
text2html('The order of the LP product is: ' + str(order))

B_f = 500e3
R_o, C_d, C_c, G_B, GB_min, A_0 = sp.symbols('R_o, C_d, C_c, G_B, GB_min, A_0')

GB_minAll = sp.solve(LPproduct -(B_f*2*sp.pi)**order, G_B)[0]
text2html('The required bandwidth  = ' + str(B_f/1000) + 'kHz')
text2html('With this value, the show stopper value of the gain-bandwidth product $G_B$ is:')
GB_minNum = GB_minAll.subs([(R_o, 0), (C_d, 0), (C_c, 0)])
eqn2html('GB_min', GB_minNum/1e6, units="MHz")

htmlPage('Device selection and verification')
i1.defPar('A_0', '1M')
i1.defPar('C_d', '8p')
i1.defPar('C_c', '7p')
i1.defPar('R_o', 55)
i1.defPar('G_B', '16M')
i1.defPar('I_s', 1)
params2html(i1.circuit)

Bf = 1/(2*sp.pi)*LPproduct**(1/order)
BfOPA627 = sp.N(Bf.subs([(R_o, 55), (C_d, 8e-12), (C_c, 7e-12), (G_B,16e6),  (A_0, 1e6)]), 4)
text2html('The achievable low-pass cut-off frequency $f_h$ with the OPA627 in [MHz] is:')
eqn2html('f_h', BfOPA627*1e-6)
htmlPage('Bode plots')
L = i1.execute()
i1.setGainType('asymptotic')
A = i1.execute()
i1.setGainType('servo')
S = i1.execute()
i1.setGainType('direct')
D = i1.execute()
i1.setGainType('gain')
G = i1.execute()
figMag = plotSweep('TrimpMag', 'Magnitude characteristics', [L, A, S, D, G], 10e3, 10e6, 200, funcType = 'mag', show = True)
fig2html(figMag, 800)
figPhase = plotSweep('TrimpPhase', 'Phase characteristics', [L, A, S, D, G], 10e3, 10e6, 200, funcType = 'phase', show = True)
fig2html(figPhase, 800)

htmlPage('Routh array')
i1.setGainType('gain')
i1.setDataType('denom')
denomLaplace = i1.execute().denom
text2html('The characteristic equation of the gain is:')
eqn2html('charPoly', denomLaplace)
text2html('The Routh array of this poly is:')
eqn2html('RA', routh(denomLaplace))

htmlPage('Nyquist plot')
i1.setGainType('loopgain')
i1.setDataType('laplace')
result = i1.execute()
result.laplace = -result.laplace
figNyquist = plotSweep('Nyquist', 'Nyquist plot: polar plot of $-L$', result, 1e6, 10e6, 100, axisType='polar', funcType='mag', show=True)
fig2html(figNyquist, 800)