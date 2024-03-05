#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSresnoise.py
"""
from SLiCAP import *
prj = initProject('CS stage noise with resistive source')
fileName = 'CSresNoise'
i1 = instruction()
i1.setCircuit(fileName + '.cir')
htmlPage('Circuit data')
img2html(fileName + '.svg', 700)
netlist2html(fileName+'.cir')
# Set value of 1/f noise to zero, and I_D to critical inversion
i1.defPar('KF_N18', 0)
i1.setSimType('numeric')
I_D     = i1.getParValue('ID')
IC      = i1.getParValue('IC_X1')
IC_CRIT = i1.getParValue('IC_CRIT_X1')
I_D     = I_D*IC_CRIT/IC
i1.defPar('ID', I_D)
# Print some important noise parameters to an HTML page
htmlPage('Operating point parameters')
R_N     = i1.getParValue('R_N_X1')
R_s     = i1.getParValue('R_s')
f_T     = i1.getParValue('f_T_X1')
g_m     = i1.getParValue('g_m_X1')
Width   = i1.getParValue('W')
text2html('Device width:')
eqn2html('W', Width)
text2html('Dain current at critical inversion:')
eqn2html('I_D', I_D)
text2html('Effective noise resistance $R_N$:')
eqn2html('R_N', R_N)
text2html('Cut-off frequency $f_T$:')
eqn2html('f_T', f_T)
i1.setSource('V1')
i1.setDetector('V_out')
i1.setGainType('vi')
i1.setDataType('noise')
i1.setSimType('numeric')
noise_result   = i1.execute()
figInoise      = plotSweep('Inoise', 'Source-referred noise spectrum', 
                           noise_result, 1e8, 1e11, 100, funcType = 'inoise', 
                           show=True)
# Calculate the noise figure at critical inversion and the given width
tot_inoise     = rmsNoise(noise_result, 'inoise', 1e9, 5e9)
# Calculate the noise figure
tot_inoise_src = rmsNoise(noise_result, 'inoise', 1e9, 5e9, 
                           source = noise_result.source)
NF             = 20*sp.log(tot_inoise/tot_inoise_src)/sp.log(10)
# Estimation of the corner frequency f_c:
f_c            = f_T*sp.sqrt(R_N/R_s)
htmlPage("Noise analysis-1")
text2html("The figure below shows the spectrum of the source-referred " + 
          "voltage noise.")
fig2html(figInoise, 500)
text2html("The source-referred RMS noise voltage over this frequency range " +
          "equals: %s [$\mu$V]."%(sp.N(1e6*tot_inoise, ini.disp)))
text2html("The noise figure equals: %s [dB]."%(sp.N(NF, ini.disp)))
text2html("The estimated conrner frequency $f_c$" +
          ": %s [GHz]."%(sp.N(f_c*1e-9, ini.disp)))
# Calculate the width W at which we will have the best noise performance.
W               = sp.Symbol('W') # 'W' in the Python environment
i1.circuit.delPar('W')        # delete the numeric definition of the width
# We will keep the inversion coefficient at critical inversion, hence we scale 
# the current with the width.
i1.defPar('ID', I_D*W/Width)
noise_w = i1.execute() # calculate the noise spectra as a function of W and f
# We now calculate the noise as a function of W over a frequency range 
# 'fmin' to 'fmax':
f_min = sp.Symbol('f_min')
f_max = sp.Symbol('f_max')
rms_noise_w        = rmsNoise(noise_w, 'inoise', f_min, f_max)
rms_noise_w_source = rmsNoise(noise_w, 'inoise', f_min, f_max, noise_w.source)
# We now calculate the noise figure as a function of 'W', 'f_min' and 'f_max':
# Use the variance instead of the RMS value (simpler equation for later use)
NF_W               = (rms_noise_w/rms_noise_w_source)**2
# We now calculate the optimum width as a function of 'fmin' and 'fmax':
W_opt              = sp.solve(sp.diff(NF_W, W), W)
# The sympy solve function returns a list with solutions, we will print the 
# positive one.
for w in W_opt:
    w = sp.N(w.subs([(f_min, 1e9), (f_max, 5e9)]), ini.disp)
    if w > 0:
        W = w
        print(W)
# Create a plot of the noise figure versus the with for different values of 
# f_max and f_min = 1G
# Define the plot parameters, 'fw', 'W' and 'fmax'
i1.defPar('W', W)
i1.defPar('f_max', '10G')
# Define the noise figure as a function of f_max:
i1.defPar('NF', 10*sp.log(NF_W.subs([(f_min, 2e8)]))/sp.log(10))
# Define the step parameters
i1.setStepVar('f_max')
i1.setStepStart('2G')
i1.setStepStop('10G')
i1.setStepMethod('lin')
i1.setSimType('numeric')
i1.setStepNum(5)
i1.stepOn()
i1.setDataType('params')
result = i1.execute()
# Plot the function
fig_NF_W = plotSweep('NF_W', 'Noise Figure versus width, $f_{min}$ = 200MHz', 
                     result, 10, 200, 50, sweepVar = 'W', sweepScale = 'u', 
                     funcType = 'param', xUnits = 'm', yVar = 'NF', 
                     yUnits = 'dB', show = True)
# Put it all on an HTML page
htmlPage("Noise analysis-2")
text2html("The lowest noise figure over a frequency range from 1GHz to 5GHz " +
          "and at critical inversion is achieved at a width " +
          "of: %s [um]"%(sp.N(W*1e6, ini.disp)))
text2html("The figure below shows the noise figure as a function of the " +
          "width and at critical inversion for diferent values of the " +
          "maximum frequency $f_{max}$, and $f_{min}$=200MHz.")
fig2html(fig_NF_W, 500)