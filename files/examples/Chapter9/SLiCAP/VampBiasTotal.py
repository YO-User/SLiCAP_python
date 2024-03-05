#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: VampBiasTotal.py

from SLiCAP import *

fileName = 'VampBiasTotal.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page
i1.setDetector('V_out')
i1.setSimType('symbolic')
i1.setGainType('vi')

# Obtain the DC detector voltage
i1.setDataType('dc')
detDC = i1.execute().dc

# define the symbols in the python environment
R_a, R_b, R, R_c, alpha = sp.symbols('R_a, R_b, R, R_c, alpha')

detDC = detDC.subs({R_b:R_a, R_c:19*R-R_a/2})

# Assume R_a << R:
# Take R_a=alpha*R and evaluate lim (alpha --> 0)
detDC = detDC.subs(R_a, alpha*R)
detDC = sp.limit(detDC, alpha, 0)

i1.setDataType('dcvar')
detVar = i1.execute().ovar

# Use R_b=R_a and R_c = 19*R- R_a//R_b
detVar = detVar.subs({R_b:R_a, R_c:19*R-R_a/2})
# Assume R_a << R:
# Take R_a=alpha*R and evaluate lim (alpha --> 0)
detVar = detVar.subs(R_a, alpha*R)
detVar = sp.limit(detVar, alpha, 0)

# Make the report
htmlPage('Biasing results')
head2html("Simplifications")
text2html("We will simplify the expressions for the DC voltage and the " +
          " detector-referred variance using the following assumptions:" +
          "<ol><li>$R_c=19R-\\frac{R_aR_b}{R_a+R_b}$</li>" +
          "<li>$R_a=R_b$</li>" +
          "<li>$R_a\\ll R$</li></ol>")
head2html('DC detector voltage')
text2html("The DC detector voltage is:")
eqn2html("V_out", detDC, units="V")
head2html('Detector referred variance')
text2html("The variance of the DC detector voltage is:")
eqn2html("(sigma_V_out)**2", detVar, units="V**2")