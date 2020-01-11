#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:50:26 2019

@author: aldo_mellado
"""

def isempty(*args):
    [j if len(j)!=0 else False for i in args]
        