#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:49:29 2019

@author: aldo_mellado
"""

def ingreso(n1):
    
    if int(n1) <=9 and '0' not in str(n1):
         aux  = '0' + str(n1)
         return(str(aux))
         
    else:
        aux = str(n1)
        return(aux)
