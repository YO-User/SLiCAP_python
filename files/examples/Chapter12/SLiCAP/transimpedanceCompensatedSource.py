#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: transimpedanceCompensatedSource.py

from SLiCAP import *

fileName = 'transimpedanceCompensatedSource'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('Phantom zero compensation')
i1.setSource('I1')
i1.setDetector('V_2')
i1.setLGref('E1')
i1.setSimType('numeric')
i1.setGainType('loopgain')
i1.setDataType('pz')
result = i1.execute()
# Display the DC value and poles and zeros of the loop gain
listPZ(result)
polesLG = result.poles
# Extract data for compensation
p_1 = polesLG[0]/2/sp.pi
p_2 = polesLG[1]/2/sp.pi
L_0 = result.DCvalue
# Calculate achievable bandwidth
Bw = sp.sqrt(sp.Abs((1-L_0)*p_1*p_2))
C_s = i1.getParValue('C_s')
# Calculate compensation resistance
R_phz = sp.N((sp.sqrt(2)*Bw+p_1+p_2)/C_s/Bw**2/2/sp.pi)
# Pass the value to the circuit
i1.defPar('R_phz', R_phz)
# Print the value of R_phz
print('R_phz = {:9.2e} Ohm\n'.format(R_phz))
# Display the DC value and poles and zeros of the loop gain
LGpz = i1.execute()
listPZ(LGpz)
# Display the DC value and poles and zeros of the gain
i1.setGainType('gain')
Gpz = i1.execute()
listPZ(Gpz)
# Create the Bode plots
i1.setDataType('laplace')
G = i1.execute()
i1.setGainType('asymptotic')
A = i1.execute()
i1.setGainType('loopgain')
L = i1.execute()
i1.setGainType('servo');
S = i1.execute()
i1.setGainType('direct')
D = i1.execute()
htmlPage("Bode plots")
dbMagPlot = plotSweep('transimpedanceCompensatedSourceBodeDBmag', 'transimpedance', [A,L,S,D,G], 1e4, 10e9, 200, funcType='dBmag', show=True)
fig2html(dbMagPlot, 800)
phasePlot = plotSweep('transimpedanceCompensatedSourceBodePhase', 'transimpedance', [A,L,S,D,G], 1e4, 10e9, 200, funcType='phase', show=True)
fig2html(phasePlot, 800)