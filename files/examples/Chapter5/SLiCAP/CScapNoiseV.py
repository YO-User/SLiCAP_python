#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CScapNoiseV.py
"""
from SLiCAP import *
prj = initProject('CScapNoiseV')
i1 = instruction()
i1.setCircuit('CScapNoiseV.cir')
# create an html page for the results
htmlPage('Noise analysis')
img2html('CScapNoiseV.svg', 300)
# Discard 1/f noise
i1.defPar('KF_N18', 0)
# print important operating point parameters
text2html('The inversion coefficient $IC$ equals: ' +
          '%s'%(sp.N(i1.getParValue('IC_X1'), ini.disp)))
text2html('The critical inversion coefficient $IC_{CRIT}$ equals: ' +
          '%s'%(sp.N(i1.getParValue('IC_CRIT_X1'), ini.disp)))
text2html('The transconductance $g_m$ equals: ' +
          '%s'%(sp.N(i1.getParValue('g_m_X1'), ini.disp)))
# calculate source referred noise spectrum
i1.setSource('V1')
i1.setDetector('V_out')
i1.setGainType('vi')
i1.setDataType('Noise')
i1.setSimType('numeric')
noiseResult = i1.execute()
head2html('Source referred noise')
iNoise = sp.sqrt(noiseResult.inoise)
text2html('The spectrum of the source-referred voltage noise [V/rt(Hz)] ' +
          'is: %s'%(sp.N(iNoise, ini.disp)))
text2html('The plot below shows the source-referred noise spectrum ' +
          'from  100MHz to 100GHz; as expected, it does not depend on ' +
          'the frequency.');
figSin = plotSweep('CScapNoiseVspectrum','Input noise spectrum', noiseResult,
                   1e8, 1e11, 100, funcType='inoise', show = True)
fig2html(figSin,  500)
# Find the width for the lowest noise
htmlPage('Noise performance optimization')
# Delete the numeric definition of W so we can calculate the optimum value 
# symbolically
i1.delPar('W')
# Keep IC at IC_CRIT
i1.defPar('ID', '7.44m*W/66u');
Svi_f_W = i1.execute().inoise
W = sp.Symbol('W')
# Find optimum value of W
W_opt = sp.solve(sp.diff(Svi_f_W, W), W)
for w in W_opt:
    if w > 0:
        i1.defPar('W', w)
        print(w)
text2html('The optimum device width $W_{opt}$ is found as: ' +
          '%s'%(sp.N(i1.getParValue('W'), ini.disp)) + ' [m].')
text2html('At this width we have in input capacitance $c_{iss}$ of: ' +
          '%s'%(sp.N(i1.getParValue('c_iss_X1'), ini.disp)) + ' [F],')
text2html('a drain current $I_{DS}$ of: %s'%(sp.N(i1.getParValue('ID'), 
          ini.disp)) + ' [A],')
text2html('and a transadmittance $g_m$ of: %s'%(sp.N(i1.getParValue('g_m_X1'), 
          ini.disp)) + ' [S]')
text2html('The plot below shows the total source referred noise over a ' +
          'frequency range from 0.1GHZ to 1GHz as a function of the ' +
          'device width, with the inversion coefficient held constant at ' +
          '$IC_{CRIT}$.')
f_max = 1e9
f_min = 1e8
B = f_max-f_min
i1.defPar('Vni', sp.sqrt(Svi_f_W*B))
# Redefine the width so it can be used as sweep variable, any value is K
i1.defPar('W', 0)
i1.setDataType('params')
result = i1.execute()
fig_Vni_W = plotSweep('Vni_W', 'Source-referred noise voltage versus ' +
                      'width: 0.1GHz-1GHz', 
                     result, 10, 200, 200, sweepVar = 'W', sweepScale = 'u', 
                     funcType = 'param', xUnits = 'm', yVar = 'Vni', 
                     yUnits = 'V', yScale='u', show = True)
fig2html(fig_Vni_W, 500)