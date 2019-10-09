#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:31:42 2019

@author: aldo_mellado
"""

import pandas as pd
import numpy as np

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')

# =============================================================================
# del documento original, filtrar columna "EStado UEM"
# =============================================================================
df1 = pd.DataFrame(df.iloc[:,1])

# =============================================================================
# del documento original, filtrar columna "Fecha Inicio"
# =============================================================================
df2 = pd.DataFrame(df.iloc[:,20])

# =============================================================================
# Para las filas  de la columna Fecha Inicio, conversión de datos a string
    #esto con la finalidad de poder manipular los datos para buscar en ellos, la fecha (linea 37)
# =============================================================================
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])

# =============================================================================
# 
# =============================================================================
df3 = df1.join(df2)


# =============================================================================
# Pedir usuario ingresar mes y año a filtrar
# =============================================================================
mes = input('\nIngrese Mes a buscar: ')
año = input('\nIngrese Año a buscar: ')

fecha  = año +"-" +mes

# =============================================================================
# Busca valores en columna Fecha Inicio que coincidan con "fecha"
# np.shape(df) retorna una tupla (num_filas, num_columnas) que contiene la dimensión o cantidad de elementos por columna
# np.shape(df)[0] retorna num_filas
# =============================================================================
df_total_mes  = df3[df3['Fecha Inicio'].str.contains(fecha)]
num_trab = np.shape(df_total_mes)[0]

# Se buscan el índice de los elementos en la columna 'Estado UEM' que satisfacen la condicion de decir 'TRABAJO TERMINADO'
indexNames = df_total_mes[ df_total_mes['Estado UEM'] == 'TRABAJO TERMINADO'].index

# eliminar valores en índices que cumplieron la condicion en línea 28
df_total_mes.drop(indexNames , inplace=True)

# contar la cantidad de filas que tienen por estado 'Pendiente'
num_pendientes = np.shape(df_total_mes)[0]

#calculo porcentaje
porcentaje = round((num_trab - num_pendientes)/num_trab * 100,1)


# =============================================================================
# Librería para graficar datos
# =============================================================================
import pygal

b_chart = pygal.SolidGauge(inner_radius=0.75)
b_chart.title = "Destiny Kill/Death Ratio"
b_chart.add("Trabajos Completados", porcentaje)
b_chart.render_in_browser()