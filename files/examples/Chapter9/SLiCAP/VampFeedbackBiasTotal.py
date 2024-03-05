#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File VampFeedbackBiasTotal.py

from SLiCAP import *

fileName = 'VampFeedbackBiasTotal'
i1 = instruction()               # Creates instance of instruction object
i1.setCircuit(fileName + '.cir') # Checks, defines the local circuit object,
                                 # and sets the index page to the circuit 
                                 # index page
i1.setSimType('symbolic')
i1.setGainType('vi')
i1.setDataType('dc')
i1.setSource('V1')
i1.setDetector('V_out')
result = i1.execute()

htmlPage('Feedback biasing')
text2html('The DC output voltage $V_{outDC}$ is:')
eqn2html('V_outDC', result.dc)

# Laplace transfer function with feedback biasing

i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()
text2html('The voltage transfer $A_v$ from source to load is:')
eqn2html('A_v', normalizeRational(result.laplace))
hf = sp.limit(result.laplace, ini.Laplace, 'oo')
text2html('For high frequencies this can be written as:')
eqn2html('A_v', hf)