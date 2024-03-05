#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: transimpedancePZcancel.py

from SLiCAP import *

fileName = 'transimpedancePZcancel'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
i1.setSource('I1');
i1.setDetector('V_2')
i1.setLGref('E1')
i1.setSimType('numeric')
i1.setGainType('loopgain')
i1.stepOff()
# Display poles
i1.setDataType('poles')
result = i1.execute()
listPZ(result)

# Display zeros
i1.setDataType('zeros')
listPZ(i1.execute())

# Display, poles, zeros and DC gain
i1.setDataType('pz')
listPZ(i1.execute())

# Calculate the phase margin
i1.setDataType('laplace')
i1.setGainType('loopgain')

L = i1.execute()
loopGain = L.laplace
pmResults = phaseMargin(loopGain)

uF = pmResults[1]
pM = pmResults[0]

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz\n'.format(pM, uF))

# Show the poles, zeros and DC value of the gain
i1.setDataType('pz')
i1.setGainType('gain')
listPZ(i1.execute())

# Modified compensation

print('=== Modified compensation C_z = 200p. ===\n')
i1.defPar('C_z', '200p')

# Show the poles, zeros and DC value of the gain
listPZ(i1.execute())

i1.setGainType('loopgain')
# Show the poles, zeros and DC value of the gain
listPZ(i1.execute())
# Show the phase margin of the loop gain
i1.setDataType('laplace')
L = i1.execute()
loopGain = L.laplace
pmResults = phaseMargin(loopGain)

uF = pmResults[1]
pM = pmResults[0]

print('Loop gain: phase margin = {:3.2f}deg at f = {:8.2e}Hz\n'.format(pM, uF))

# Plot the phase margin versus C_z
i1.setStepVar('C_z')
i1.setStepStart(0)
i1.setStepStop('200p')
i1.setStepNum(100)
i1.setStepMethod('lin')
i1.stepOn()

result = i1.execute()

PM = [i1.stepList, phaseMargin(result.laplace)[0]] # x, y trace data
htmlPage('Phase margin')
plotData = {'PhaseMargin vs C_z': PM}
figPM = plot('PM', 'Phase margin versus $C_z$', 'lin', plotData, xName = '$' + sp.latex(i1.stepVar) + '$', xScale = 'p', xUnits = 'F', yName = 'Phase margin', yUnits = 'deg', show = True)
fig2html(figPM, 800)

i1.setDataType('step')
i1.setGainType('gain')
i1.setStepStart('50p')
i1.setStepNum(4)
i1.stepOn()
htmlPage('Step response PZ canceling')
stepPZcancel = plotSweep('stepPZcancel', 'Unit step response lag compensation', i1.execute(), 0, 3, 200, sweepScale='u', yScale='k', show=True)
fig2html(stepPZcancel, 800)

i1.setDataType('laplace')
htmlPage('Bode plots PZ canceling')
dBmagStepped = plotSweep('dBmagSteppedCancelPZ', 'Lag compensation', i1.execute(), 1, 10e3, 200, sweepScale='k', show=True)
phaseStepped = plotSweep('PhaseSteppedCancelPZ', 'Lag compensation', i1.execute(), 1, 10e3, 200, sweepScale='k', funcType='phase', show=True)
fig2html(dBmagStepped, 800)
fig2html(phaseStepped, 800)

i1.setGainType('servo')
i1.setStepVar('A_0')
i1.setStepStart(1)
i1.setStepStop(1e6)
i1.setStepNum(500)
i1.setStepMethod('log')
i1.setDataType('poles')
polesPlot = i1.execute()
i1.setDataType('zeros')
i1.setGainType('loopgain')
i1.stepOff()
zerosPlot = i1.execute()
pzRLpzComp = plotPZ('pzRLpzComp', 'Lag compensation root locus', [polesPlot, zerosPlot], xmin=-2, xmax=0, ymin=-1, ymax=1, xscale='M', yscale='M', show=True)
pzRLpzCompZoom = plotPZ('pzRLpzCompZoom', 'Lag compensation root locus', [polesPlot, zerosPlot], xmin=-0.5, xmax=0, ymin=-0.25, ymax=0.25, xscale='M', yscale='M', show=True)