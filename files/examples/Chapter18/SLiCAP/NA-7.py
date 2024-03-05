#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: NA-2.py

from SLiCAP import *
prj = initProject('NA-7')
instr = instruction()
instr.setCircuit('NA-7.cir')
instr.setSimType('symbolic')
instr.setGainType('vi')
instr.setDataType('matrix')
result = instr.execute()
htmlPage("Example Modified Nodal Analysis")
head2html('MNA equation')
matrices2html(result)
instr.setDetector('V_2')
instr.setDataType('laplace')
result = instr.execute()
head2html('Output voltage')
text2html("The voltage $V_2$ at node (2) is obtained as:")
eqn2html('V_2', sp.simplify(result.laplace))