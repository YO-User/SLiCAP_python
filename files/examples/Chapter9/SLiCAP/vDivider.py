#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: vDivider.py

from SLiCAP import *

fileName = 'vDivider.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page
#
htmlPage('Netlist and circuit data');
netlist2html(fileName);
elementData2html(i1.circuit);
#
htmlPage('DC variance analysis');
i1.setDetector('V_out')
i1.setSimType('symbolic')
i1.setGainType('vi')
i1.setDataType('dcvar')
result = i1.execute()
dcVar2html(result)