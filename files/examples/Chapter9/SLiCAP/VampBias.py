#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: VampBias.py

from SLiCAP import *

fileName = 'VampBias.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page
i1.setDetector('V_out')
i1.setSimType('symbolic')
i1.setGainType('vi')

# Obtain the DC detector voltage
i1.setDataType('dc')
detDC = i1.execute().dc

# Obtain the detector-referred variance
i1.setDataType('dcvar')
detVar = i1.execute().ovar

htmlPage('Biasing results')
head2html('DC detector voltage')
text2html("The DC detector voltage is:")
eqn2html("V_out", detDC, units="V")
head2html('Variance of the DC detector voltage')
text2html("The variance of the DC detector voltage is:")
eqn2html("(sigma_V_out)**2", detVar, units="V**2")