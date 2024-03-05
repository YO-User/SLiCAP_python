#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mosPoleSplitting.py
"""
from SLiCAP import *
prj = initProject('mosPoleSplitting')
i1 = instruction()
i1.setCircuit('mosPoleSplitting.cir')
htmlPage('Circuit data')
netlist2html('mosPoleSplitting.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)
i1.setSimType('numeric')
i1.setSource('I1')
i1.setDetector('V_2')
i1.setGainType('gain')
i1.setDataType('poles')
htmlPage('Pole splitting in CS stage:')
result = i1.execute()
poles = result.poles
sp.symbols('p_1 p_2')
sumOfPoles = poles[0] + poles[1]
text2html('The sum of the poles in [rad/s] with $c_{dg}=300$fF equals:')
eqn2html('p_1+p_2', sumOfPoles)
i1.defPar('c_dg', 0);
result =i1. execute()
poles = result.poles
sumOfPoles = poles[0] + poles[1]
text2html('The sum of the poles in [rad/s] with $c_{dg}=0$ equals:')
eqn2html('p_1+p_2', sumOfPoles)
htmlPage('Pole splitting with $c_{dg}$')
i1.defPar('c_dg', 20.44e-15);
result = i1.execute();
poles = result.poles
sumOfPoles = poles[0] + poles[1]
text2html('The sum of the poles in [rad/s] with $c_{dg}=20.44$fF equals:')
eqn2html('p_1+p_2', sumOfPoles)
i1.setStepVar('c_dg')
i1.setStepStart(0)
i1.setStepStop('50f')
i1.setStepNum(100)
i1.setStepMethod('lin')
i1.stepOn()
figPZ = plotPZ('poleSplitting', 'Poles vs $c_{d_g}$', i1.execute(), show=True)
fig2html(figPZ, 500)