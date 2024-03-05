#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: createFigures.py

from SLiCAP import *
prj = initProject('Figures')
traceDict = LTspiceData2Traces('antiSeriesCS.txt')
plot('antiSeriesCS', 'DM voltage to current transfer,  W=220n,  L=180n', 'lin',
     traceDict, show=True, yName = '$I_o/I_{ss}$', yUnits='-', 
     xName='V3', xUnits='V')

traceDict = LTspiceData2Traces('antiSeriesCS_Vss.txt')
plot('antiSeriesCS_Vss', 'DM to CM conversion,  W=220n,  L=180n', 'lin',
     traceDict, show=True, yName = '$V_{ss}$', yUnits='V', 
     xName='V3', xUnits='V')

traceDict = LTspiceData2Traces('complParlCS_Io.txt')
plot('complParlCS_Io', 'DM output current,  W=220n,  L=180n', 'lin',
     traceDict, show=True, yName = '$Id(M4)+Id(M3)$', yUnits='A', 
     yScale='u', xName='V7', xUnits='V')

traceDict = LTspiceData2Traces('complParlCS_IQ.txt')
plot('complParlCS_IQ', 'Common-mode current,  W=220n,  L=180n', 'lin',
     traceDict, show=True, yName = '$(Id(M4)-Id(M3))/2$', yUnits='A', 
     yScale='u', xName='V7', xUnits='V')