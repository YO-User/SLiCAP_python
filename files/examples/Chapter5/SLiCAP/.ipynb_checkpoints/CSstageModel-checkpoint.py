#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

from SLiCAP import *
from CSstageLTspice import LTmag, LTphase

# Obtain the values of the small-signal parameters from the EKV model
# Alternatively, you could obtain them from a looup table or a SPICE .OP run
from CSstageEKV import gm, go, cgs, cgb, cdg, cdb

# Uncomment the next line if you want to overwrite the main html index page
#prj = initProject('CSstageSmallSignal');

# Generate netlist
#makeNetlist('CSstageModel.asc', 'CS stage MOS small-signal model');

i1 = instruction()
i1.setCircuit('CSstageModel.cir')
# This creates an new index page in the html report and links to new pages
# will now be placed on this index page
i1.defPar('g_m', gm)
i1.defPar('g_o', go)
i1.defPar('c_gs', cgs)
i1.defPar('c_gb', cgb)
i1.defPar('c_dg', cdg)
i1.defPar('c_db', cdb)

htmlPage('Circuit data')
head2html('Circuit diagram')
img2html('CSstageModel.svg', 600)
netlist2html('CSstageModel.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

htmlPage('CS stage small-signal dynamic behavior')
i1.setSimType('numeric');
i1.setGainType('gain');
i1.setDataType('laplace');
i1.setSource('I1');
i1.setDetector('V_out');
gainModel = i1.execute()

head2html('Numeric expression')
eqn2html('Z_t', normalizeRational(gainModel.laplace))

head2html('Bode plots')
magZtModel = plotSweep('magZtModel', 'magnitude', gainModel, 1, 100e9, 200, funcType = 'mag', show=True)
traces2fig(LTmag, magZtModel)
magZtModel.plot()
fig2html(magZtModel, 600)
phaseZtModel = plotSweep('phaseZtModel', 'phase', gainModel, 1, 100e9, 200, funcType = 'phase', show=True)
traces2fig(LTphase, phaseZtModel)
phaseZtModel.plot()
fig2html(phaseZtModel, 600)

i1.setDataType('pz')
pz2html(i1.execute())

