#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:31:42 2019
@author: aldo_mellado
"""
# =============================================================================
#              Primer indicador (% de órdenes cerradas en el mes)
# =============================================================================
import pandas as pd
import numpy as np
from contains0 import contains0

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,1]) #Estado UEM

df2 = pd.DataFrame(df.iloc[:,20]) #Fecha Inicio
df2 = df2[df2['Fecha Inicio'] !='00-00-0000']
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])

df3 = df1.join(df2).dropna() #fusiona ambos archivos; Estado UEM y Fecha Inicio, eliminando valores no validos (nan)

flag = True
#while usado para que solicite los datos hasta que estos sean válidos
while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag = False
        
fecha  = año +"-" + contains0(mes) #contains0 corrige la posibiliadd que el usuario ingrese 1, en lugar de 01

df_total_mes  = df3[df3['Fecha Inicio'].str.contains(fecha)]
num_trab = np.shape(df_total_mes)[0]

# Se buscan el índice de los elementos en la columna 'Estado UEM' que satisfacen la condicion de decir 'TRABAJO TERMINADO'
indexNames = df_total_mes[ df_total_mes['Estado UEM'] == 'TRABAJO TERMINADO'].index

# eliminar valores en índices que cumplieron la condicion en línea 28
df_total_mes.drop(indexNames , inplace=True)

# contar la cantidad de filas que tienen por estado 'Pendiente'
num_pendientes = np.shape(df_total_mes)[0]

if num_trab!=0:
    #calculo porcentaje
    porcentaje = round((num_trab - num_pendientes)/num_trab * 100,1)
else:
    print("División por 0")
    
# =============================================================================
#                               Segundo Indicador (?)
    
# En esta parte haremos que se solicite un mes y una unidad en particular, 
# para entonces, mostrar las órdenes de trabajo asociadas a dicha unidad en dicho mes.
# =============================================================================

import pandas as pd
import numpy as np

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,3]).dropna() #unidad

df2 = pd.DataFrame(df.iloc[:,9]) #fecha recepción OT
df2 = df2[df2['Fecha recepcion OT'] !='00-00-0000']
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha recepcion OT'])],dtype=object, columns = ['Fecha recepcion OT']) #Fecha convertida a str para luego buscar fecha

df3 = df1.join(df2).dropna() #Unir ambos dataFrame para relacionarlos

# flag = True
# while flag:
#     mes = input('\nIngrese Mes a buscar: ')
#     año = input('\nIngrese Año a buscar: ')
#     if len(mes)==0 or len(año)==0:
#         print("\nFavor ingrese un año y un mes válidos\n")
#     else:
#         flag =False

# fecha  = año +"-" + contains0(mes)

unidades = np.unique(list(df1.iloc[1:,0])) #Me permite encontrar sin repeticion los nombres de los Servicios o Unidades disponibles

# Filtro por fecha
# Se ingresa el la fecha que se desea filtrar y aparecen las OT en esa fecha para todas las unidades

ot_mes  = df3[df3['Fecha recepcion OT'].str.contains(fecha)]
num_trab = np.shape(ot_mes)[0]# Numero de OT generadas durante el mes y año indicados

# Crear un diccionario, que almacene la cantidad de ocurrencias u OT para esa unidad determinada
ocurrencias = {
        }

for i in unidades:
    num_ot_uni_mes = np.shape(ot_mes.loc[ot_mes['Servicio o Unidad'] == i])[0]
    print(f"num_ot_uni_mes = {num_ot_uni_mes}\t Servicio o Unidad = {i}")
    ocurrencias[i] = num_ot_uni_mes
    
num_to_filter = 3 #Cantidad de valores a filtrar
ocurr = pd.DataFrame(sorted(ocurrencias.items(), key = lambda x:x[1], reverse = True)).iloc[:num_to_filter,:]
flag =  any(ocurr.iloc[:,1])# verifica que la cantidad de OT para las unidades no sea 0
    
#=============================================================================
#                           Tercer Indicador (Contador)
#                               OT abiertas
#=============================================================================
nom_tec = ['CARLOS LOBOS','FELIPE ACOSTA',
           'GUIDO VICENCIO','IGNACIO VALDIVIA',
           'PABLO SILVA']

# (suma de todas las ordenes T1 generadas en el mes - sum ordenes T1 abiertas en el mes)/suma de todas las ordenes T1 generadas en el mes
import pandas as pd 
import numpy as np

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')

# =============================================================================
# Agregando, filtrando y casteando datos Fecha Inicio
# =============================================================================
df0 = pd.DataFrame(df.iloc[:,20]) # Fecha Inicio
df0 = pd.DataFrame([str(j) for i,j in enumerate(df0['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio']) #Fecha convertida a str para luego buscar fecha
df0 = df0[df0['Fecha Inicio'] !='00-00-0000']

df1 = pd.DataFrame(df.iloc[:,52]) # Fecha Termino6
df1 = pd.DataFrame([str(j) for i,j in enumerate(df1['Fecha Termino6'])],dtype=object, columns = ['Fecha Termino6']) #Fecha convertida a str para luego buscar fecha
df1 = df1[df1['Fecha Termino6'] !='00-00-0000']

df2 = pd.DataFrame(df.iloc[:,15]) # Nombre de técnico
df3 = pd.DataFrame(df.iloc[:,12]) # Tipo de mantención

# =============================================================================
# Concatena hacia la derecha, las columnas de nom. tec, tipo de mant. f. inicio, fecha term.
# usamos dropna() para quitar la fila con valores vacíos o no correspondientes 00-00-0000
# =============================================================================
df4 = pd.concat([df0,df1,df2,df3], axis = 1, sort = False).dropna()

flag = True
# while flag:
#     mes = input('\nIngrese Mes a buscar: ')
#     año = input('\nIngrese Año a buscar: ')
#     if len(mes)==0 or len(año)==0:
#         print("\nFavor ingrese un año y un mes válidos\n")
#     else:
#         flag =False
        
# fecha  = año +"-" + contains0(mes)

mant_mes_ab  = df4[df4['Fecha Inicio' ].str.contains(fecha)]

print(f"\nLa cantidad de órdenes abiertas en {fecha} es: {np.shape(mant_mes_ab)[0]}")

mant_mes_cr  = mant_mes_ab[mant_mes_ab['Fecha Termino6' ].str.contains(fecha)]

print(f"\nLa cantidad de órdenes cerradas en {fecha} es: {np.shape(mant_mes_cr)[0]}")