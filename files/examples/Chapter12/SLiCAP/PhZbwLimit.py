#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  14 15:36:50 2020

@author: anton
"""

from SLiCAP import *
t1 = time()
#prj = initProject('Phantom Zero Bandwidth limitation')

fileName = 'PhZbwLimit'
#makeNetlist(fileName + '.asc', 'PhZ bandwidth limitation')
i1 = instruction()
i1.setCircuit(fileName + '.cir')

# Define the circuit parameters
A = -20e6
f_p2 = 1e9
R_f  = 10e3
C_s  = 300e-12
C_f  = 0

i1.defPar('A', A)
i1.defPar('tau_2', 1/2/sp.pi/f_p2)
i1.defPar('R_f', R_f)
i1.defPar('C_s', C_s)
i1.defPar('C_f', C_f)

htmlPage('Circuit data')
head2html('Circuit diagram')
img2html(fileName + '.svg', 500)
netlist2html(fileName + '.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setSource('I1')
i1.setDetector('V_out')
i1.setLGref('E1')
i1.setSimType('numeric')
i1.setDataType('laplace')

i1.setGainType('asymptotic')
ag = i1.execute()
i1.setGainType('loopgain')
lg = i1.execute()
i1.setGainType('servo')
servo = i1.execute()
i1.setGainType('gain')
gain = i1.execute()
i1.setGainType('direct')
direct = i1.execute()
figdBmagUncomp = plotSweep('Uncomp', 'Uncompensated transimpedance', [ag, lg, servo, gain, direct], 1e3, 1e7, 200, show=True)

# Compensate the amplifier
servoData = findServoBandwidth(lg.laplace)
Bf = servoData['lpf']
f_phz = Bf**2/(np.sqrt(2)*Bf - 1/(2*np.pi*R_f*C_s))
C_phz = 1/(2*np.pi*f_phz*R_f)
i1.defPar('C_f', C_phz)

i1.setGainType('asymptotic')
ag = i1.execute()
i1.setGainType('loopgain')
lg = i1.execute()
i1.setGainType('servo')
servo = i1.execute()
i1.setGainType('gain')
gain = i1.execute()
i1.setGainType('direct')
direct = i1.execute()
figdBmagComp = plotSweep('Comp', 'Compensated transimpedance', [ag, lg, servo, gain, direct], 1e3, 1e7, 200, show=True)

# Limit bandwidth stepwise to 10kHz:
f_max = 10e3
C_max = sp.N(1/(f_max*2*sp.pi*R_f))

i1.setStepVar('C_f')
i1.setStepStart(C_phz)
i1.setStepStop(C_max)
i1.setStepNum(10)
i1.setStepMethod('log')
i1.stepOn()

i1.setGainType('gain')
gain = i1.execute()
figdBmagBWL = plotSweep('BWL', 'Bandwidth limited transimpedance', gain, 1e3, 1e7, 200, show=True)

i1.setGainType('loopgain')
loopgain = i1.execute()
figdBmagBWLL = plotSweep('BWLloopgain', 'Loop gain bandwidth limited transimpedance', loopgain, 1e3, 1e7, 200, show=True)

i1.setDataType('poles')
i1.setGainType('servo')
i1.setStepNum(100)
pServoCf = i1.execute()

# Root-locus plots
i1.setDataType('poles')
i1.setGainType('servo')
i1.setStepVar('A')
i1.setStepStart(-0.1)
i1.setStepStop(A)
i1.setStepMethod('lin')
i1.setStepNum(100)
i1.stepOn()


i1.defPar('C_f', C_phz)
servoPolesC_phz = i1.execute()
i1.setDataType('zeros')
i1.setGainType('loopgain')
i1.defPar('A_0',A)
i1.stepOff()
loopgainZerosC_phz = i1.execute()

figPservoCphz = plotPZ('RL_C_phz', 'Poles $C_f=C_{phz}$.', [servoPolesC_phz, loopgainZerosC_phz], xmin=-2, xmax=0, ymin=-1, ymax = 1, xscale='M', yscale='M', show=True)

i1.defPar('C_f', C_max)
loopgainZerosC_max = i1.execute()
i1.setDataType('poles')
i1.setGainType('servo')
i1.stepOn()
servoPolesC_max = i1.execute()

figPservoCmax = plotPZ('pRL_C_max', 'Poles $C_f=C_{max}$.', [servoPolesC_max, loopgainZerosC_max], xmin=-4, xmax=0, ymin=-2, ymax = 2, xscale='M', yscale='M', show=True)

i1.setStepNum(1000)
i1.setStepStop(-5e5)
servoPolesC_max = i1.execute()
figPservoZoom = plotPZ('pRL_C_max_Zoom', 'Poles $C_f=C_{max}$.', [servoPolesC_max, loopgainZerosC_max], xmin=-20, xmax=0, ymin=-10, ymax = 10, xscale='k', yscale='k', show=True)

figPservoCf = plotPZ('pServo', 'Poles step $C_f$.', pServoCf, xmin=-4, xmax=0, ymin=-2, ymax = 2, xscale='M', yscale='M', show=True)

htmlPage('Asymptotic-gain model plots')
fig2html(figdBmagUncomp, 800)
fig2html(figdBmagComp, 800)
htmlPage('Bandwidth limitation plots')
fig2html(figdBmagBWL, 800)
fig2html(figdBmagBWLL, 800)
htmlPage('Root locus plots')
fig2html(figPservoCphz, 800)
fig2html(figPservoCmax, 800)
fig2html(figPservoZoom, 800)
fig2html(figPservoCf, 800)