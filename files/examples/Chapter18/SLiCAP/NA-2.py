#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: NA-2.py

from SLiCAP import *
prj = initProject('NA-2')
instr = instruction()
instr.setCircuit('NA-2.cir')
instr.setSimType('symbolic')
instr.setGainType('vi')
instr.setDataType('matrix')
result = instr.execute()
htmlPage("Example Nodal Analysis")
head2html('MNA equation')
matrices2html(result)
instr.setSource('I1')
instr.setDetector(['V_0', 'V_2'])
instr.setGainType('gain')
instr.setDataType('laplace')
result = instr.execute()
head2html('Transimpedance')
eqn2html('Z_t', result.laplace)