#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:41:46 2020

@author: anton
"""

from SLiCAPyacc import *
       
def doInstruction(instObj):
    """
    Execution of the instruction with parameter stepping.
    """
    if instObj.step:
        if ini.stepFunction:
            # Create a substitution dictionary that does not contain step parameters
            subsDict = {}
            if instObj.stepMethod == 'array':
                for key in instObj.circuit.parDefs.keys():
                    if key not in instObj.stepVars:
                        subsDict[key] = instObj.circuit.parDefs[key]
            else:
                for key in instObj.circuit.parDefs.keys():
                    if key != instObj.stepVar:
                        subsDict[key] = instObj.circuit.parDefs[key]
            instObj.parDefs = subsDict
            # Do the instruction
            (instObj.Iv, instObj.M, instObj.Dv) = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)
            # Do stepping by means of substitution in the numerator and denominator
            if instObj.dataType == 'poles':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                # pz analysis is numeric so better lambdify!
                for poly in denoms:
                    instObj.poles.append(numRoots(poly, ini.Laplace))
                instObj.zeros = []
            elif instObj.dataType == 'zeros':
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for poly in numers:
                    instObj.zeros.append(numRoots(poly, ini.Laplace))
                instObj.poles = []
            elif instObj.dataType == 'pz':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                instObj.poles = []
                instObj.zeros = []
                instObj.DCvalue = []
                for i in range(len(denoms)):
                    poles = numRoots(denoms[i], ini.Laplace)
                    zeros = numRoots(numers[i], ini.Laplace)
                    (poles, zeros) = cancelPZ(poles, zeros)
                    instObj.poles.append(poles)
                    instObj.zeros.append(zeros)
                    try:
                        # Lets try a real limit with Maxima CAS
                        instObj.DCvalue.append(maxLimit(numers[i]/denoms[i], str(ini.Laplace), '0', 'plus'))
                    except:
                        # If not just substitute s=0 with Sympy
                        instObj.DCvalue.append(sp.Subs(numers[i]/denoms[i], ini.Laplace, 0))
            elif instObj.dataType == 'step':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(invLaplace(numers[i], denoms[i]*ini.Laplace))
                    except:
                        print "Warning: could not calculate the unit step response."
            elif instObj.dataType == 'impulse':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(invLaplace(numers[i], denoms[i]))
                    except:
                        print "Warning: could not calculate the unit impulse response."
            elif instObj.dataType == 'time':
                pass
            elif instObj.dataType == 'numer':
                numer = doNumer(instObj)
                instObj.numer = stepFunctions(instObj, numer)
            elif instObj.dataType == 'denom':
                denom = doDenom(instObj)
                instObj.denom = stepFunctions(instObj, denom)
            elif instObj.dataType == 'laplace':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                instObj.laplace = []
                for i in range(len(denoms)):
                    instObj.laplace.append(normalizeLaplaceRational(numers[i], denoms[i]))
            elif instObj.dataType == 'solve':
                sol = doSolve(instObj)
                sols = stepFunctions(instObj. sol)
                instObj.solve = []
                for i in range(len(sols)):
                    instObj.solve.append(sp.simplify(sols[i]))
        else:
            # Create a deep copy of the substitution dictionary
            subsDict = {}
            for key in instObj.circuit.parDefs.keys():
                subsDict[key] = instObj.circuit.parDefs[key]
            instObj.parDefs = subsDict
            # For each set of step variable create the numeric substitution
            # dictionary, make the matrices and do the non-stepped instruction.
            if instObj.stepMethod != 'array':
                for stepVal in instObj.stepList:
                    instObj.parDefs[instObj.stepVar] = stepVal
                    doDataType(instObj)
            else:
                # array stepping, number of steps is length of lists in stepArray
                for i in range(len(instObj.stepArray[0])):
                    # substitute the i-th value for each step variable in the
                    # .parDefs dictionary.
                    for j in range(len(instObj.stepVars)):
                        instObj.parDefs[instObj.stepVars[j]] = instObj.stepArray[j][i]
                    doDataType(instObj)
    else:
        # No parameter stepping, just do the non-stepped instruction.
        instObj.parDefs = instObj.circuit.parDefs
        doDataType(instObj)
    return instObj

def stepFunctions(instObj, function):
    """
    Substitutes step values for step parameters in functions and returns a list
    of functions with these substitutions.
    """
    
    """
    # The lambdify method was not faster then one-by-one substitution
    if instObj.stepMethod == 'array':
        func = sp.lambdify(instObj.stepVars, function)
        functions = [func(instObj.stepArray[i]) for i in range(len(instObj.stepArray))]
    else:
        func = sp.lambdify(instObj.stepVar, function)
        functions = [func(instObj.stepList[i]) for i in range(len(instObj.stepList))]
    """
    # One-by-one substitition
    if instObj.stepMethod == 'array':
        functions = []
        for i in range(len(instObj.stepArray[0])):
            subsList = []
            for j in range(len(instObj.stepVars)):
                subsList.append((instObj.stepVars[j], instObj.stepArray[j][i]))
            functions.append(function.subs(subsList))
    else:
        functions = [function.xreplace({instObj.stepVar: instObj.stepList[i]}) for i in range(len(instObj.stepList))]
    return functions

def doDataType(instObj):
    """
    Returns the instruction object with the result of the execution without 
    parameter stepping
    """
    (instObj.Iv, instObj.M, instObj.Dv) = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)  
    if instObj.dataType == 'matrix':
        pass
    elif instObj.dataType == 'poles':
        if instObj.step:
            instObj.poles.append(doPoles(instObj))
        else:
            instObj.poles = doPoles(instObj)  
            instObj.DCvalue = None
    elif instObj.dataType == 'zeros':
        if instObj.step:
            instObj.zeros.append(doZeros(instObj))
        else:
            instObj.zeros = doZeros(instObj)
            instObj.DCvalue = None
    elif instObj.dataType == 'pz':
        (poles, zeros, DCvalue) = doPZ(instObj)
        if instObj.step:
            instObj.poles.append(poles)
            instObj.zeros.append(zeros)
            instObj.DCvalue.append(DCvalue)
        else:    
            instObj.poles = poles
            instObj.zeros = zeros
            instObj.DCvalue = DCvalue
    elif instObj.dataType == 'denom':
        if instObj.step:
            instObj.denom.append(doDenom(instObj))
        else:
            instObj.denom = doDenom(instObj)
    elif instObj.dataType == 'numer':
        if instObj.step:
            instObj.numer.append(doNumer(instObj))
        else:
            instObj.numer = doNumer(instObj)
    elif instObj.dataType == 'laplace':
        if instObj.step:
            instObj.laplace.append(doLaplace(instObj))
        else:
            instObj.laplace = doLaplace(instObj)
    elif instObj.dataType == 'step':
        try:
            instObj.stepResp = invLaplace(doNumer(instObj), doDenom(instObj)*ini.Laplace)
        except:
            print "Warning: could not calculate the unit step response."
    elif instObj.dataType == 'impulse':
        try:
            instObj.stepResp = invLaplace(doNumer(instObj), doDenom(instObj))
        except:
            print "Warning: could not calculate the unit impulse response."
    elif instObj.dataType == 'time':
        pass 
    elif instObj.dataType == 'solve':
        if instObj.step:
            instObj.solve.append(doSolve(instObj))
        else:
            instObj.solve = doSolve(instObj)            
    return instObj

def doDenom(instObj):
    """
    Calculates the denominator of a transfer by evaluating of the determinant
    of the MNA matrix.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    denom = maxDet(instObj.M)
    if instObj.gainType == 'servo':
        (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
        numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        numer = numer * lgNumer
        denom = denom * lgDenom + numer
    elif instObj.gainType == 'loopgain':
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        denom = denom * lgDenom
    return denom


def doPoles(instObj):
    """
    Calculates the denominator of a transfer from source to detector and find
    the poles.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), ini.Laplace))
    return numRoots(denom, ini.Laplace)

def lgValue(instObj):
    """
    Calculates the corrected gain of the loop gain reference. In case of
    a loop gain reference of the type EZ and HZ the calculation of the loop
    gain proceeds as if a current source was placed in parallel with the
    output impedance (zo) of this controlled source. The value of this source
    is the loop gain reference divided by the output impedance of the device
    (Norton equivalent representation).
    """
    lgRef = instObj.circuit.elements[instObj.lgRef]
    if lgRef.model == 'g':
        value = lgRef.params['value']
    elif lgRef.model == 'E':
        value = lgRef.params['value']
    elif lgRef.model == 'EZ':
        value = lgRef.params['value']/lgRef.params['zo']
    elif lgRef.model == 'HZ':
        value = lgRef.params['value']/lgRef.params['zo']
    elif lgRef.model == 'H':
        value = lgRef.params['value']
    elif lgRef.model == 'F':
        value = lgRef.params['value']
    elif lgRef.model == 'G':
        value = lgRef.params['value']
    if instObj.simType == 'numeric':
        value = fullSubs(value, instObj.circuit.parDefs)
    return value

def makeSrcDetPos(instObj):
    """
    Returns the number of the source rows and detector colums for calculation
    of the cofactors or application of Cramer's rule.
    """
    detectors = []
    for var in instObj.circuit.depVars:
        if var != 'V_0':
            detectors.append(var)
    if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
        lgRef = instObj.circuit.elements[instObj.lgRef]
        if lgRef.model == 'E':
            srcP = detectors.index('I_o_' + instObj.lgRef)
            srcN = None
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
        elif lgRef.model == 'EZ':
            # Signal source is a current source in parallel with Zo
            # gain will be divided by the value of Zo.
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            if lgRef.nodes[0] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[0])
            if lgRef.nodes[1] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[1])
        elif lgRef.model == 'F':
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
        elif lgRef.model == 'G':
            srcP = detectors.index('I_o_' + instObj.lgRef)
            srcN = None
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
        elif lgRef.model == 'g':
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
        elif lgRef.model == 'H':
            srcP = detectors.index('I_o' + instObj.lgRef)
            srcN = None
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
        elif lgRef.model == 'HZ':
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
            if lgRef.nodes[0] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[0])
            if lgRef.nodes[1] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[1])    
    else:
        (detP, detN) = instObj.detector
        if detP != None:
            detP = detectors.index(detP)
        if detN != None:
            detN = detectors.index(detN)
        if instObj.source[0].upper() == 'V':
            srcP = detectors.index('I_' + instObj.source)
            srcN = None
        elif instObj.source[0].upper() == 'I':
            nodes = instObj.circuit.elements[instObj.source].nodes
            if nodes[0] != '0':
                srcP = detectors.index('V_' + nodes[0])
            else:
                scrP = None
            if nodes[1] != 0:
                srcN = detectors.index('V_' + nodes[1])
            else:
                srcN = None
    return(detP, detN, srcP, srcN)
    
def doNumer(instObj):
    """
    Calculates the numerator of a transfer by evaluating cofactors or the 
    numerator of the detector response using Cramer's rule.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
    if instObj.gainType == 'vi':
        numer = maxCramerNumer(instObj.M, instObj.Iv, detP, detN)
    else:
        numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
        if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
            (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
            numer *= lgNumer
        elif instObj.gainType == 'servo':
            numer *= -lgNumer
    return numer

def doZeros(instObj):
    """
    Calculates the numerator of a transfer from source to detector and find the
    zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), ini.Laplace))
    return numRoots(numer, ini.Laplace)
    
def doPZ(instObj):
    """
    Calculates the numerator and the denominator of the transfer from source to
    detector and determines the zero-frequency value, the poles and the zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with poles, list with zeros, DCvalue.
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), ini.Laplace))
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), ini.Laplace))
    poles = numRoots(denom, ini.Laplace)
    zeros = numRoots(numer, ini.Laplace)
    (poles, zeros) = cancelPZ(poles, zeros)
    try:
        # Lets try a real limit with maxima
        DCvalue = maxLimit(numer/denom, str(ini.Laplace), '0', 'plus')
    except:
        # If not just substitute s=0
        DCvalue = sp.Subs(numer/denom, ini.Laplace, 0)
    return(poles, zeros, DCvalue)

def doLaplace(instObj):
    """
    Calculates the numerator and the denominator of the transfer and normalizes
    the result to:
        
        F(s) = gain * s^l (1+b_1*s + ... + b_m*s^m)/ (1+a_1*s + ... + a_n*s^n),

        with l zero if there is a finite nonzero zero-frequency value, else
        positive or negative integer.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    numer = doNumer(instObj)
    denom = doDenom(instObj)
    return normalizeLaplaceRational(numer, denom)

def doSolve(instObj):
    """
    Calculates the solution of a network.
    """
    return maxSolve(instObj.M, instObj.Iv)

def checkNumeric(expr, stepVar = None):
    """
    Checks if the expressions does not contain parameters other then stepVar',
    'ini.Laplace', 'FREQUECY' or 'OMEGA'.
    
    expr:         Sympy expression
    stepVar:      str or Sympy.Symbol
    return value: 'True' if numeric, else 'False'.
    """
    numeric = True
    if type(expr) == str:
        expr = sp.N(sp.sympify(expr))
    if isinstance(expr, tuple(sp.core.all_classes)):
        expr = sp.N(expr)
        params = list(expr.free_symbols)
        for par in params:
            if stepVar == None and par != ini.Laplace and par != ini.frequency:
                numeric = False
            elif par != stepVar and par != ini.Laplace and par != ini.frequency:
                numeric = False
    return numeric

def findServoBandwidth(loopgainRational):
    """
    Determines the intersection points of the asymptotes of the magnitude of
    the loopgain with unity. It returns a dictionary with key-value pairs:
        
        - hpf: frequency of high-pass intersection
        - hpo: order at high-pass intersection
        - lpf: frequency of low-pass intersection
        - lpo: order at low-pass intersection
        - mbv: mid-band value of the loopgain (highest value at order = zero)
        - mbf: lowest freqency of mbv
        
    """
    numer, denom    = sp.fraction(loopgainRational)
    numer           = sp.expand(sp.collect(numer.evalf(), ini.Laplace))
    denom           = sp.expand(sp.collect(denom.evalf(), ini.Laplace))
    poles           = numRoots(denom, ini.Laplace)
    zeros           = numRoots(numer, ini.Laplace)
    (poles, zeros)  = cancelPZ(poles, zeros)
    numPoles        = len(poles)
    numZeros        = len(zeros)
    numCornerFreqs  = numPoles + numZeros
    coeffsN,coeffsD = coeffsTransfer(loopgainRational)
    coeffsN         = np.array(coeffsN)
    coeffsD         = np.array(coeffsD)
    firstNonZeroN   = np.argmax(coeffsN != 0)
    firstNonZeroD   = np.argmax(coeffsD != 0)
    startOrder      = firstNonZeroN - firstNonZeroD
    startValue      = np.abs(coeffsN[firstNonZeroN]/coeffsD[firstNonZeroD])    
    freqsOrders     = np.zeros((numCornerFreqs, 6))
    mbv             = sp.N(sp.Subs(loopgainRational, ini.Laplace, 0))
    mbf             = 0
    for i in range(numZeros):
        freqsOrders[i, 0] = np.abs(zeros[i])
        freqsOrders[i, 1] = 1
    for i in range(numPoles):
        freqsOrders[numZeros + i, 0] = np.abs(poles[i])
        freqsOrders[numZeros + i, 1] = -1
    # sort the rows with increasing corner frequencies 
    freqsOrders = freqsOrders[freqsOrders[:,0].argsort()]
    
    start = 0
    for i in range(numCornerFreqs):
        if freqsOrders[i, 0] == 0:
            start = i + 1
            freqsOrders[i, 2] = startOrder
            freqsOrders[i, 4] = 0
            freqsOrders[i, 5] = freqsOrders[-1, 0]
        if i == start:
            freqsOrders[i, 2] =  startOrder + freqsOrders[i, 1]
            freqsOrders[i, 3] = startValue/(freqsOrders[i, 0]**freqsOrders[i, 1])
            if freqsOrders[i, 2] != 0:
                Bw = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                Bw = 0
            if Bw > freqsOrders[i, 0]:
                if freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 4] = Bw
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] < 0:
                    freqsOrders[i, 5] = Bw
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = Bw
                elif freqsOrders[i, 2] == 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
            else:
                freqsOrders[i, 4] = 0
                freqsOrders[i, 5] = freqsOrders[-1, 0]
        elif i > start:
            freqsOrders[i, 2] = freqsOrders[i - 1, 2] + freqsOrders[i, 1]
            if freqsOrders[i, 1] != 0:
                freqsOrders[i, 3] = freqsOrders[i - 1, 3]/(freqsOrders[i, 0]**freqsOrders[i, 1])
            else:
                freqsOrders[i, 3] = np.NaN
            if freqsOrders[i, 2] != 0:
                freqsOrders[i, 5] = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                freqsOrders[i, 5] = 0
            if freqsOrders[i, 2] != 0:
                Bw = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                Bw = 0
            if Bw > freqsOrders[i, 0]:
                if freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 4] = Bw
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] < 0:
                    freqsOrders[i, 5] = Bw
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = Bw
                elif freqsOrders[i, 2] == 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
            else:
                freqsOrders[i, 4] = 0
                freqsOrders[i, 5] = freqsOrders[-1, 0]
    result = {}
    result['hpf']=np.amax(freqsOrders[:,4])
    result['lpf']=np.amin(freqsOrders[:,5])
    result['hpo']=freqsOrders[np.where(freqsOrders[:,4]==result['hpf'])[0][0],2]
    result['lpo']=freqsOrders[np.where(freqsOrders[:,5]==result['lpf'])[0][0],2]
    for i in range(numCornerFreqs):
        if freqsOrders[i,2] == 0 and freqsOrders[i,3] > mbv:
            result['mbv'] = freqsOrders[i,3]
            result['mbf'] = freqsOrders[i,0]
    if ini.HZ:
        result['hpf'] = result['hpf']/np.pi/2
        result['lpf'] = result['lpf']/np.pi/2
        result['mbf'] = result['mbf']/np.pi/2
    return result

if __name__ == '__main__': 
    s = sp.Symbol('s')
    loopGainNumer = -s*(1 + s/20)*(1 + s/40)/2
    loopGainDenom = (s + 1)**2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)
    loopGain        = loopGainNumer/loopGainDenom
    r = findServoBandwidth(loopGain)
    print r