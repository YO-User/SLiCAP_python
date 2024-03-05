#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 20:31:51 2021

@author: anton
"""
from SLiCAP import *

fileName = 'VampNoise';
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('Circuit data')
head2html('Circuit diagram: ' + fileName)
img2html(fileName + '.svg', 600)
netlist2html(fileName + '.cir')
#
i1.setGainType('vi')
i1.setDataType('noise')
#
# Define the source and the detector
i1.setSource('V1');
i1.setDetector('V_out');
#
htmlPage('Symbolic noise analysis')
i1.setSimType('symbolic')
noiseResultSym = i1.execute()
noise2html(noiseResultSym)
#
# Let us find show-stopper values for R_a, S_v, and S_i for the case:
# - source resistance: R_s = 600 Ohm
# - voltage gain     : A_v = 20
# - noise figure     : NF  = 2 (3dB)
#
i1.defPar('R_s', 600)
# Define R_b = (A_v-1)*R_a
i1.defPar('R_b', '(A_v-1)*R_a')
i1.defPar('A_v', 20)
i1.setSimType('numeric')
# Calculate the noise with the given parameters.
noiseResultNum = i1.execute()
#
# Determine the noise figure NF: (the given procedure works with
# frequency-independent noise spectra only)
#
R_a, S_v, S_i, NF, R_a_max, S_i_max, S_v_max = sp.symbols('R_a, S_v, S_i,' +
                                            'NF, R_a_max, S_i_max, S_v_max')
htmlPage('Show-stopper values')
#
text2html('Let us find show-stopper values for $R_a$, $S_v$, and $S_i$ for ' +
          'the case in which the noise factor $NF$ equals 2 (3dB).')
head2html('Noise factor NF')
text2html('The noise factor NF [-] is obtained as:')
NFact = sp.simplify(noiseResultNum.inoise/noiseResultNum.inoiseTerms['V1'])
eqn2html(NF, NFact);
#
# Show stopper (= maximum) value $R_{amax}$ for R_a with S_i=0 and S_v=0
Ra_max = sp.N(sp.solve(NFact.subs([(S_v, 0), (S_i, 0)])-2, R_a)[0], 3)
head2html('Show-stopper value $R_a$');
text2html('The show stopper value $R_{amax}$ for $R_a$ with $NF=2$, ' +
          '$S_v=0$ and $S_i=0$ is obained as:');
eqn2html(R_a_max, Ra_max);
#
# Show stopper (= maximum) $S_{v,max}$ for S_v as a function of R_a and S_i=0
Sv_max = sp.N(sp.solve(NFact.subs(S_i, 0)-2, S_v)[0], 3);
head2html('Show-stopper value $S_v$');
text2html('The show stopper value for $S_v$ with $NF=2$ and $S_i=0$ can be ' +
          'obained a function of $R_a$ (setting $R_a$ to zero would be ' +
          'meaningless):')
eqn2html(S_v_max, Sv_max);
#
# Show stopper (= maximum) $S_{i,max}$ for S_i as a function of R_a and S_i=0
Si_max = sp.N(sp.solve(NFact.subs(S_v, 0)-2, S_i)[0], 3);
head2html('Show-stopper value $S_i$');
text2html('The show stopper value for $S_i$ with $NF=2$ and $S_v=0$ can be ' +
          'obained a function of $R_a$: (setting $R_a$ to zero would be ' +
          'meaningless):');
eqn2html(S_i_max, Si_max);