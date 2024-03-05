#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File CDstageCompensation.py

from SLiCAP import *
fileName = 'CDcompM18'
prj = initProject(fileName)
    
# Create the netlist if you didn't do it before
#makeNetlist(fileName + '.asc', fileName)

# Create an instruction object
i1 = instruction();

# Define the circuit
i1.setCircuit(fileName + '.cir')
#
i1.defPar('W', '4u')
i1.defPar('L', '1u')
i1.defPar('ID', '250u')
i1.defPar('R_s', '15k')
i1.defPar('C_ell', '250f')
i1.defPar('C_phz', 0)

# Display the circuit information on an HTML page
htmlPage('Ciruit data')
head2html('Schematic diagram')
img2html(fileName + '.svg', 500)
netlist2html(fileName + '.cir')
params2html(i1.circuit)

i1.setSimType('numeric')
i1.setSource('V1')
i1.setDetector('V_out')

# List the DC value, the poles, and the zeros of the gain
i1.setDataType('pz')
i1.setGainType('gain')
gainData = i1.execute()
listPZ(gainData)

i1.defPar('C_phz', '1.7f')
# List the DC value, the poles, and the zeros of the gain after compensation
i1.setDataType('pz')
i1.setGainType('gain')
gainData = i1.execute()
listPZ(gainData)

# Display the magnitude and phase plots of the transfers of the asymptotic-
# gain model
# print(i1.controlled()) # Uncomment this if you don't know the name of  
                         # the controlled source that you want to select
                         # as loop gain reference
i1.setLGref('Gm_M1_XU1')
#
htmlPage('Asymptotic-gain model')
i1.setDataType('laplace')
i1.setGainType('asymptotic')
A  = i1.execute()
i1.setGainType('loopgain')
L = i1.execute()
i1.setGainType('servo')
S = i1.execute()
i1.setGainType('direct')
D = i1.execute()
i1.setGainType('gain')
G = i1.execute()
fig_as_gain_model_mag = plotSweep(fileName + '_as_gain_model_mag', 'Magnitude plots', [A, L, S, D, G], 0.1, 100, 200, sweepScale='G', funcType='mag', show=True)
fig2html(fig_as_gain_model_mag, 800)
fig_as_gain_model_phs = plotSweep(fileName + '_as_gain_model_phs', 'Phase plots', [A, L, S, D, G], 0.1, 100, 200, sweepScale='G', funcType='phase', show=True)
fig2html(fig_as_gain_model_phs, 800)

# Study the poles of the loop gain
htmlPage('Loop gain analysis')
i1.setGainType('loopgain')
i1.setDataType('pz')
result_loopgain = i1.execute()
pz2html(result_loopgain)

# Study the DC value of the loop gain
i1.setSimType('symbolic')
i1.setDataType('laplace')
result=i1.execute()
DCloopgain = result.laplace.subs(ini.Laplace, 0)
eqn2html('L_DC', DCloopgain)

# Study the gain
htmlPage('Gain')
i1.setDataType('pz')
i1.setSimType('numeric')
i1.setGainType('gain')
result_gain = i1.execute()
pz2html(result_gain)

# Study the DC  value of the gain
i1.setSimType('symbolic')
i1.setDataType('laplace')
result=i1.execute()
DCgain = result.laplace.subs(ini.Laplace, 0)
eqn2html('A_DC', DCgain)

# Study the effect of a phantom zero on the pole positions
i1.setSimType('numeric')
i1.setDataType('poles')
i1.setStepVar('C_phz')
i1.setStepMethod('lin')
i1.setStepStart(0)
i1.setStepStop('2f')
i1.setStepNum(50)
i1.stepOn()
polesResult = i1.execute()
figRL = plotPZ(fileName + '_rootLocus', 'CD stage', polesResult, xmin=-3e9, xmax = 0, ymin=-1.5e9, ymax=1.5e9, show=True)
fig2html(figRL, 600)

# Study the effect of a phantom zero on the Bode plots
i1.setDataType('laplace')
i1.setStepNum(5)
gainLaplace = i1.execute()
figMag = plotSweep(fileName + '_dBmag', 'CD stage', gainLaplace, 0.1, 100, 200, sweepScale='G', funcType='dBmag', show=True)
fig2html(figMag, 800)
figPhase = plotSweep(fileName + '_phase', 'CD stage', gainLaplace, 0.1, 100, 200, sweepScale='G', funcType='phase', show=True)
fig2html(figPhase, 800)
