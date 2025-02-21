#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

from SLiCAP import *

prj = initProject('NMOS EKV plots') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'mosEKVplotsN.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page                       
htmlPage('Circuit data')
netlist2html(fileName)

elementData2html(i1.circuit)
params2html(i1.circuit)

# Put the plots on a page
htmlPage('CMOS18 EKV model plots')

i1.setDataType('params')

result = i1.execute()

fig_Ids_Vgs  = plotSweep('IdsVgs', '$V_{gs}(I_{ds})$', result, 1e-3, 150, 200, sweepVar= 'I_D', sweepScale = 'u', yVar = 'I_D', yUnits = 'A', yScale = 'u',  xVar = 'V_GS_X1', xUnits = 'V', funcType = 'param', show = True)
fig2html(fig_Ids_Vgs, 600)

fig_gm_Ids  = plotSweep('gmIds', '$g_m(I_{ds})$', result, 0, 150, 100, sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', yVar = 'g_m_X1', yScale = 'u', yUnits = 'S', funcType = 'param', show = True)
fig2html(fig_gm_Ids, 600)

fig_fT_Ids  = plotSweep('fTIds', '$f_{T}(I_{ds})$', result, 0, 150, 100, sweepVar= 'I_D', sweepScale = 'u', xUnits = 'A', yVar = 'f_T_X1', yScale = 'G', yUnits = 'Hz', funcType = 'param', show = True)
fig2html(fig_fT_Ids, 600)

LTspiceTraces =  LTspiceData2Traces('NMOS-gm-testbench.txt')
traces2fig(LTspiceTraces, fig_gm_Ids)
fig_gm_Ids.plot()

LTspiceTraces =  LTspiceData2Traces('NMOS-fT-testbench.txt')
traces2fig(LTspiceTraces, fig_fT_Ids)
fig_fT_Ids.plot()