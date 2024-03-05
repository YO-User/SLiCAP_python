#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: vAmpBlack.py

from SLiCAP import *

fileName = 'vAmpBlack'
prj = initProject(fileName)    # Creates the SLiCAP libraries and the
                               # project HTML index page
i1 = instruction()             # Creates an instance of an instruction object
i1.setCircuit(fileName+'.cir') # Checks and defines the local circuit object,
                               # and sets the index page to the project index 
i1.setSource('V1')
i1.setDetector('V_3')
i1.setSimType('symbolic')
i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()

htmlPage('Voltage amplifier with VCVS controller')
text2html('The gain of the system is obtained as:')
V_ell, V_s = sp.symbols('V_ell, V_s')
eqn2html(V_ell/V_s, result.laplace)