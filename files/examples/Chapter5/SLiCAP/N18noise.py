#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N18noise.py
"""
from SLiCAP import *
prj = initProject('N18noise');
makeNetlist('N18noise.asc', 'CS stage noise');
i1 = instruction();
i1.setCircuit('N18noise.cir')
#i1.defPar('AF_N18', 1)
htmlPage('Circuit data')
img2html('N18noise.svg', 500)
netlist2html('N18noise.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)
i1.setSimType('numeric');
i1.setGainType('vi');
i1.setDataType('noise');
i1.setSource('V1');
i1.setDetector('V_out');
htmlPage('Voltage noise NMOS')
# Plot S_vi for ID=10uA, step W and L, while keeping W/L=1
i1.defPar('ID','10u')
i1.setStepVar('W')
i1.setStepMethod('list')
i1.setStepList([0.2e-6, 0.5e-6, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6])
i1.stepOn()
noiseResult = i1.execute()
SvN18mos = plotSweep('SvN18mos', 'Svi V/rt(Hz) NMOS W/L=1 ID=10uA',
                    noiseResult, 10, 100e6, 200, funcType='inoise', show=True)
fig2html(SvN18mos, 800)
# Another method is to calculate S_vi(f, W), define it as a circuit parameter
# and plot this parameter.
# Calculate the function and define it as a circuit parameter
i1.delPar('W') # Delete the definition of W, this keeps it a symbolic variable
i1.stepOff()   # Disable parameter stepping to obtain a single expression
inoise_f_W = sp.N(i1.execute().inoise)    # calculate S_vi(f,W)
i1.defPar('Si_f_W', inoise_f_W) # define a circuit parameter for this function
i1.defPar('W', '1u')  # Redefine the parameter W otherwise it cannot be stepped
i1.defPar('f', 1)     # Define the parameter f otherwise it cannot be swept
i1.stepOn()           # Enable parameter stepping
i1.setDataType('params')
result = i1.execute()
S_vi_f_W = plotSweep('S_vi_f_W', 'Svi V/rt(Hz) noise NMOS W/L=1 ID=10uA', 
                     result, 10, 100e6, 200, funcType='param', axisType='log', 
                     sweepVar='f', xUnits='Hz', yVar='Si_f_W', yUnits='$V^2/Hz$', 
                     show=True)
fig2html(S_vi_f_W, 800)
# Plot f_T and f_l versus W for W/L=1 and ID=10uA (dataType = 'params')
i1.setDataType('params')
i1.stepOff()
result = i1.execute()
f_T_f_L = plotSweep('f_T_f_L', '$f_T,\, f_{\ell}, NMOS W/L=1 ID=10uA$', result, 
                    0.2e-6, 50e-6, 200, funcType='param', axisType='log', 
                    sweepVar='W', xUnits='m', xScale='u', 
                    yVar=['f_T_XU1', 'f_ell_XU1'], yScale='G', yUnits='Hz', 
                    show=True)
fig2html(f_T_f_L, 800)
i1.delPar('f')      # Remove the numeric definition of the frequency
# Plot S_vi for W = L = 50u while stepping ID
i1.defPar('W', '50u')
i1.setDataType('noise');
i1.setStepVar('ID')
i1.stepOn()
i1.setStepMethod('list')
i1.setStepList([10e-6, 20e-6, 50e-6, 100e-6, 1e-3, 2e-3, 5e-3])
i1.stepOn()
noiseResult = i1.execute()
SvN18mos50u = plotSweep('SvN18mos50u', 'Svi V/rt(Hz) noise W=50u', noiseResult,
                        1, 1e6, 200, funcType='inoise', show=True)
fig2html(SvN18mos50u, 800)