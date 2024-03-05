#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: RLvAmp_3_1.py

from SLiCAP import *

fileName = 'RLvAmp_3_1'
prj = initProject(fileName) 
i1 = instruction()        
i1.setCircuit(fileName + '.cir')
i1.setSource('V1')              # Signal source is V1
i1.setDetector('V_3')           # Voltage detector at node (3)
i1.setLGref('E1')               # Loop gain reference variable = E1
i1.setGainType('servo')         # Source to load transfer
i1.setSimType('numeric')        # Numeric simulation
i1.setDataType('poles')         # Calculate the poles
i1.setStepVar('A_0')            # Step the DC controller gain for RL plot
i1.setStepMethod('lin')
i1.setStepStart(0)
i1.setStepStop('12k')
i1.setStepNum(100)
i1.stepOn()
RL = i1.execute()
i1.stepOff()
i1.setGainType('gain')
polesGain = i1.execute()
i1.setGainType('asymptotic')
polesAsymptotic = i1.execute()
i1.setGainType('loopgain')
polesLoopGain = i1.execute()
i1.setDataType('zeros')
zerosLoopGain = i1.execute()
plots = [RL, polesLoopGain, zerosLoopGain, polesAsymptotic, polesGain]
htmlPage('Root locus')
fig_PZ = plotPZ('RL_' + fileName, fileName, plots, xmin=-2, xmax=0, ymin=-1, ymax=1, xscale='k', yscale='k', show=True)
fig2html(fig_PZ, 600)
i1.setGainType('gain')
i1.setDataType('pz')
pzGain = i1.execute()
listPZ(pzGain)
# Calculate the phase margin
i1.setDataType('laplace')
i1.setGainType('loopgain')
L = i1.execute()
loopGain = L.laplace
pmResults = phaseMargin(loopGain)

uF = pmResults[1]
pM = pmResults[0]

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz'.format(pM, uF))

# Generate Bode plots
htmlPage('Bode plots');
i1.setGainType('servo');
S = i1.execute();
i1.setGainType('gain');
G = i1.execute();
i1.setGainType('asymptotic');
A = i1.execute();
plots = [A, L, S, G];
BodeMag  = plotSweep('dBmag_' + fileName, fileName, plots, 1, 1e4, 200, funcType='dBmag',  show=True)
BodePhas = plotSweep('Phase_' + fileName, fileName, plots, 1, 1e4, 200, funcType='phase', show=True)
fig2html(BodeMag, 800)
fig2html(BodePhas,800)