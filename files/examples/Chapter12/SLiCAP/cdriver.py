#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: cdriver.py

from SLiCAP import *

fileName = 'cdriver'
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir')
i1.setSource('V1')
i1.setDetector('V_out')
i1.setLGref('E_O1')
i1.setSimType('numeric')
i1.setDataType('poles')
i1.setGainType('loopgain')
listPZ(i1.execute())
i1.setDataType('zeros')
listPZ(i1.execute())
i1.setDataType('pz')
listPZ(i1.execute())
i1.setDataType('laplace')
result = i1.execute()
i1.setGainType('gain');
i1.setDataType('poles');
listPZ(i1.execute());