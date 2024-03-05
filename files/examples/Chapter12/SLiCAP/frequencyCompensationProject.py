#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 21:21:38 2021

@author: anton
"""

from SLiCAP import *
t1 = time()
prj = initProject('Frequency compensation')

import RLvFollower_2                   # Example 12.1
import RLvAmp_2                        # Example 12.2
import RLvFollower_3                   # Example 12.3
import RLvAmp_3_1                      # Example 12.4
import RLvAmp_3_2                      # Example 12.5
import transimpedanceCompensated       # Example 12.8
import transimpedanceCompensatedSource # Example 12.9
import cdriver                         # Example 12.10
import cdrivercompensated              # Example 12.11
import PhZbwLimit                      # Example 12.12
import poleSplitOpAmp                  # Example 12.13
import transimpedancePZcancel          # Example 12.15 and 12.16
import QampBias                        # Example 12.18
t2=time()
print(t2-t1,'s')