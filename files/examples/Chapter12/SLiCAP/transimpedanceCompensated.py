#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: transimpedanceCompensated.py

from SLiCAP import *

fileName = 'transimpedanceCompensated'
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
R_f = i1.getParValue('R_f')
# Calculate compensation capacitance
C_phz = sp.N((sp.sqrt(2)*Bw+p_1+p_2)/R_f/Bw**2/2/sp.pi)
# Pass the value to the circuit
i1.defPar('C_phz', C_phz)
# Print the value of C_phz
print('C_phz = {:9.2e}F\n'.format(C_phz))
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
dbMagPlot = plotSweep('transimpedanceCompensatedBodeDBmag', 'transimpedance', [A,L,S,D,G], 1e4, 10e9, 200, funcType='dBmag', show=True)
fig2html(dbMagPlot, 800)
phasePlot = plotSweep('transimpedanceCompensatedBodePhase', 'transimpedance', [A,L,S,D,G], 1e4, 10e9, 200, funcType='phase', show=True)
fig2html(phasePlot, 800)
# limitation of the bandwidth to 200kHz
print('=== Bandwidth limitation to 200kHz ===')
i1.defPar('C_phz', '1/2/pi/2e5/R_f')
# Display the DC value and poles and zeros of the asymptotic gain model
i1.setDataType('pz')
i1.setGainType('asymptotic')
ApzLim = i1.execute()
listPZ(ApzLim)

i1.setGainType('loopgain')
LpzLim = i1.execute()
listPZ(LpzLim)

i1.setGainType('servo')
SpzLim = i1.execute()
listPZ(SpzLim)

i1.setGainType('gain')
GpzLim = i1.execute()
listPZ(GpzLim)

# Generate the Bode plots
i1.setDataType('laplace')
GR = i1.execute()
i1.setGainType('asymptotic')
AR = i1.execute()

i1.setGainType('loopgain')
LR = i1.execute()

i1.setGainType('servo')
SR = i1.execute()

i1.setGainType('direct')
DR = i1.execute()

htmlPage("Bode plots 200kHz bandwidth limitation")
dbMagPlotR = plotSweep('transimpedanceCompensatedBodeDBmag200kHz', 'transimpedance B=200kHz', [AR, LR, SR, DR, GR], 1e4, 10e9, 200, funcType='dBmag', show=True)
fig2html(dbMagPlotR, 800)
phasePlotR = plotSweep('transimpedanceCompensatedBodePhase200kHz', 'transimpedance B=200kHz', [AR, LR, SR, DR, GR], 1e4, 10e9, 200, funcType='phase', show=True)
fig2html(phasePlotR, 800)

# generate root locus plot
i1.setGainType('asymptotic')
i1.setDataType('poles')
pAS = i1.execute()
i1.setGainType('loopgain')
pL = i1.execute()
i1.setDataType('zeros')
zL = i1.execute()
i1.setGainType('gain')
i1.setDataType('poles')
pG = i1.execute()
i1.setGainType('servo')
i1.setStepVar('A_0')
i1.setStepStart(0.01)
i1.setStepStop(1e6)
i1.setStepMethod('log')
i1.setStepNum(2000)
i1.stepOn()
RL = i1.execute()
figRL = plotPZ('transimpedanceCompensatedRL200kHz', 'Root Locus', [pAS, pL, zL, pG, RL], xmin=-0.4, xmax=0, ymin=-0.2, ymax=0.2, xscale='M', yscale='M', show=True)
fig2html(figRL, 600)