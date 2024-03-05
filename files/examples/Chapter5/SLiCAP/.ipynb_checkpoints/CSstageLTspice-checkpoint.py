#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:21:00 2021

@author: anton
"""

from SLiCAP import *

# This function will be added to SLiCAPplots!

def LTspiceAC2SLiCAPtraces(fileName, dB=False, color='c'):
    """
    This function converts the results of a single-run LTspice AC analysis 
    into two traces (mag, phase) that can be added to SLiCAP plots.
    
    :param fileName: Name of the file. The file should be located in 
                     the ditectory given in *ini.txtPath*.
    :type fileName:  str
    
    :param dB: True if the trace magnitude should be in dB, else False.
               Default value = False
    :type dB: bool
    
    :param color: Matplotlib color name. Valid names can be found at:
                  https://matplotlib.org/stable/gallery/color/named_colors.html
                  Default value is cyan (c); this does not correspond with one
                  of the standard gain colors of the asymptotic-gain model.
    :type color:  str
    
    :return: a list with two trace dicts, magnitude and phase, respectively.
    :rtype: list
    
    :Example:
        
    >>> LTmag, LTphase = LTspiceAC2SLiCAPtraces('LTspiceACdata.txt')
    """
    try:
        f = open(ini.txtPath + fileName, 'r', encoding='utf-8', errors='replace')
        lines = f.readlines()
        f.close()
    except:
        print('Cannot find: ', fileName)
        lines = []
    freqs = []
    mag   = []
    phase = [] 
    for i in range(len(lines)):
        if i != 0:
            line = lines[i].split()
            if ini.Hz:
                freqs.append(eval(line[0]))
            else:
                freqs.append(eval(line[0])*2*np.pi)
            dBmag, deg = line[1].split(',')
            dBmag = eval(dBmag[1:-2])
            deg = eval(deg[0:-2])
            if not dB:
                mag.append(10**(dBmag/20))
            else:
                mag.append(dBmag)
            if ini.Hz:
                phase.append(deg)
            else:
                phase.append(np.pi*deg/180)
    LTmag = trace([freqs, mag])
    LTmag.label = 'LTmag'
    LTmag.color = color
    LTphase = trace([freqs, phase])
    LTphase.label = 'LTphase'
    LTphase.color = color
    traces = [{'LTmag': LTmag}, {'LTphase': LTphase}]
    return traces

# Convert LTspice AC analysis output to SLiCAP traces
LTmag, LTphase = LTspiceAC2SLiCAPtraces('CSstage.txt')

# Uncomment the next line if you want to overwrite the main html index page
#prj = initProject('CSstageSmallSignal');

htmlPage('LTspice circuit')
head2html('LTspice operating point and AC analysis')
img2html('LTspiceCSstage.svg', 800)

figLTmag = plot('LTmag', 'AC simulation magnitude charactersitics', 
                'log', LTmag, xName='frequency', xUnits='Hz',
                yName='$V_{out}$', yUnits = '$\\Omega$', show=True)

figLTphase = plot('LTphase', 'AC simulation phase charactersitics', 
                'semilogx', LTphase, xName='frequency', xUnits='Hz',
                yName='$arg(V_{out})$', yUnits = 'deg', show=True)

# Place the plots on the HTML active page
fig2html(figLTmag, 600, caption='LTspice AC analysis magnitude of $Z_t$.')
fig2html(figLTphase, 600, caption='LTspice AC analysis phase of $Z_t$.')