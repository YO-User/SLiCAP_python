#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CScapNoiseI.py
"""
from SLiCAP import *
prj = initProject('CScapNoiseI')
i1 = instruction()
i1.setCircuit('CScapNoiseI.cir')
htmlPage('Noise analysis')
img2html('CScapNoiseI.svg', 300)
# Discard 1/f noise
i1.defPar('KF_N18', 0)
i1.setSource('I1')
i1.setDetector('V_out')
i1.setGainType('vi')
i1.setDataType('noise')
i1.setSimType('numeric')
noiseResult = i1.execute()
head2html('Source referred noise');
text2html('The figure below shows the source referred noise spectrum ' +
          'from  100MHz to 100GHz for $W=W_{opt}$ and at $IC=IC_{CRIT}$.')
figSin = plotSweep('CScapNoiseIspectrum', 'Input noise spectrum', 
                   noiseResult, 1e8, 1e11, 100, funcType='inoise', show=True)
fig2html(figSin,  500)
IniRMS = rmsNoise(noiseResult, 'inoise', 100e6, 1e9);
text2html('The total source referred RMS current noise $i_{ni}$ amounts: ' +
          '%s [A]'%(sp.N(IniRMS, ini.disp)))