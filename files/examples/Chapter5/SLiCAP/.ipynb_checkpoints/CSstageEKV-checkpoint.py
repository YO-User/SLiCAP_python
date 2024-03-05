#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

from SLiCAP import *
from CSstageLTspice import LTmag, LTphase

# Uncomment the next line if you want to overwrite the main html index page
#prj = initProject('CSstageSmallSignal');

# Generate netlist
#makeNetlist('CSstageEKV.asc', 'CS stage EKV small-signal model');

i1 = instruction();
i1.setCircuit('CSstageEKV.cir')
# This creates an new index page in the html report and links to new pages
# will now be placed on this index page


# Obtain the values of the small-signal parameters according to the EKV model,
# the C18 process parameters and the device geometry. They are calculated
# using the model equations in the subcircuit X1: CMOS18N
# We will pass these values to other circuits.
# 
# You could also obtain these values from a lookup table and correct them for 
# the device geometry and operating conditions

gm = i1.getParValue('g_m_XU1')
go = i1.getParValue('g_o_XU1')
cgs = i1.getParValue('c_gs_XU1')
cgb = i1.getParValue('c_gb_XU1')
cdg = i1.getParValue('c_dg_XU1')
cdb = i1.getParValue('c_db_XU1')

htmlPage('Circuit data')
head2html('Circuit diagram')
img2html('CSstageEKV.svg', 600)
netlist2html('CSstageEKV.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

htmlPage('CS stage small-signal dynamic behavior')
i1.setSimType('numeric');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_out');
gainEKV = i1.execute()

head2html('Numeric expression')
eqn2html('Z_t', normalizeRational(gainEKV.laplace))

head2html('Bode plots')
magZtEKV = plotSweep('magZtEKV', 'magnitude', gainEKV, 1, 100e9, 200, funcType = 'mag', show=True)
traces2fig(LTmag, magZtEKV)
magZtEKV.plot()
fig2html(magZtEKV, 600)
phaseZtEKV = plotSweep('phaseZtEKV', 'phase', gainEKV, 1, 100e9, 200, funcType = 'phase', show=True)
traces2fig(LTphase, phaseZtEKV)
phaseZtEKV.plot()
fig2html(phaseZtEKV, 600)

i1.setDataType('pz')
pz2html(i1.execute())
