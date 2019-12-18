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

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,1])
df2 = pd.DataFrame(df.iloc[:,20])
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])
df3 = df1.join(df2)

flag = True
while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag = False
        
fecha  = año +"-" +mes

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

import pygal

b_chart = pygal.SolidGauge(inner_radius=0.45)
b_chart.title = "Trabajos abiertos v/s Trabajos Cerrados en\n{}".format(fecha)
b_chart.add("Trabajos Completados", porcentaje)
#b_chart.add("Trabajos Terminados", num_trab-num_pendientes)
#b_chart.add("Total Trabajos", num_trab)
b_chart.render_in_browser()

# =============================================================================
#                               Segundo Indicador (?)

# En esta parte haremos que se solicite un mes y una unidad en particular, 
# para entonces, mostrar las órdenes de trabajo asociadas a dicha unidad en dicho mes.
# =============================================================================
import pandas as pd
import numpy as np

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,3]) #unidad

df1 = df1[df1['Servicio o Unidad'].notnull()] #filtra nan o NaN

df2 = pd.DataFrame(df.iloc[:,9]) #fecha recepción OT
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha recepcion OT'])],dtype=object, columns = ['Fecha recepcion OT']) #Fecha convertida a str para luego buscar fecha
df3 = df1.join(df2) #Unir ambos dataFrame para relacionarlos

flag = True
while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag =False

fecha  = año +"-" +mes

unidades = np.unique(list(df1.iloc[1:,0])) #Me permite encontrar sin repeticion los nombres de los Servicios o Unidades disponibles

#opcion = input("Para filtrar los datos, ingrese:\na) Si desea filtrar por mes\nSi desea filtrar por año\nc)Si desea filtrar por Unidad\nd)Si desea filtrar por unidad y año\ne)Si desea filtrar por unidad y mes")

# Filtro por fecha
# Se ingresa el la fecha que se desea filtrar y aparecen las OT en esa fecha para
# todas las unidades

ot_mes  = df3[df3['Fecha recepcion OT' ].str.contains(fecha)]
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

import pygal
b_chart = pygal.SolidGauge(inner_radius=0.75)
b_chart.title = "Num_SoU/Num tot Trab {} ".format(fecha)
if flag==True: #Si la cantidad de OT para las unidades no es 0, entonces:
    for i in range(num_to_filter):
        b_chart.add(ocurr.iloc[i,0], (ocurr.iloc[i,1]/num_trab)*100)
    b_chart.render_in_browser()
else: #en cambio, si no hubieron OT para ninguna unidad, entonces:
    print("\nEn esta fecha no existen OT")
#=============================================================================
#                           Tercer Indicador (Contador)
# OT abiertas
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
while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag =False
        
fecha  = año +"-" +mes

mant_mes_ab  = df4[df4['Fecha Inicio' ].str.contains(fecha)]

print(f"\nLa cantidad de órdenes abiertas en {fecha} es: {np.shape(mant_mes_ab)[0]}")

mant_mes_cr  = mant_mes_ab[mant_mes_ab['Fecha Termino6' ].str.contains(fecha)]

print(f"\nLa cantidad de órdenes cerradas en {fecha} es: {np.shape(mant_mes_cr)[0]}")

#mant_T2 = mant_mes_cr[mant_mes_cr['Tipo de mantención'] == 'T1']
#mant_T2 = np.shape(mant_mes_cr[mant_mes_cr['Tipo de mantención'] == 'T1'])[0]


# =============================================================================
# # Cuarto y Quinto Indicador (Porcentaje de Atenciones cerradas netas de tipo 
#                            T1 y T2 por tecnicos)
# =============================================================================
import pandas as pd
import numpy as np
import pygal

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
nom_tec = ['CARLOS LOBOS','FELIPE ACOSTA',
           'GUIDO VICENCIO','IGNACIO VALDIVIA',
           'PABLO SILVA']
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
#flag_mes = 0
#flag_año = 0

while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    
#    flag_mes = int(mes) #copia de los valores de mes y año ingresados que no modifican originales
#    flag_año = int(año) #se hace un casteo para corroborar formato
    
#    if len(mes)==0 or len(año)==0 or flag_mes not in range(1,13): #se hace el filtro para la condición que no cumple
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag = False
        
fecha  = año +"-" +mes

# =============================================================================
# #mant_mes_gen  = df4[df4['Fecha Inicio'].str.contains(fecha)]
# #mant_mes_ab = mant_mes_gen
# 
# # Se buscan el índice de los elementos en la columna 'Fecha Termino6' que satisfacen la condicion de coincidir con la fecha ingresada
# #indexNames = df4[df4['Fecha Termino6'].str.contains(fecha)].head().index

# eliminar valores en índices que cumplieron la condicion en línea 28
# mant_mes_ab.drop(indexNames , inplace=True)
# =============================================================================
mant_mes  = df4[df4['Fecha Inicio'].str.contains(fecha)]

# Órdenes de tipo T1 generadas en la fecha

mant_T1 = mant_mes[mant_mes['Tipo de mantención'] == 'T1']
mant_T1 = mant_T1[mant_T1['Nombre Técnico'].isin(nom_tec)]

mant_T2 = mant_mes[mant_mes['Tipo de mantención'] == 'T2']
mant_T2 = mant_T2[mant_T2['Nombre Técnico'].isin(nom_tec)] #elimina todos las filas que contenian informacion sobre atención realizadas por personas que no eran técnicos

#mant_T3 = mant_mes[mant_mes['Tipo de mantención'] == 'T3']
#mant_T4 = mant_mes[mant_mes['Tipo de mantención'] == 'T4']

#Órdenes cerradas de tipo T1 y T2 en esa fecha
mant_cer_mes = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_mes = mant_cer_mes[mant_cer_mes['Nombre Técnico'].isin(nom_tec)]

mant_cer_T1 = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_T1 = mant_cer_T1[mant_cer_T1['Nombre Técnico'].isin(nom_tec)]
mant_cer_T1 = mant_cer_T1[mant_cer_T1['Tipo de mantención']=='T1']

mant_cer_T2 = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_T2 = mant_cer_T2[mant_cer_T2['Nombre Técnico'].isin(nom_tec)]
mant_cer_T2 = mant_cer_T2[mant_cer_T2['Tipo de mantención']=='T2']


#mant_cer_T3 = mant_T3[mant_T3['Fecha Termino6'].str.contains(fecha)]
#mant_cer_T4 = mant_T4[mant_T4['Fecha Termino6'].str.contains(fecha)]

T = ["T1", "T2"]
aux = {}

#Ordenes de tipo T1 cerradas por técnico
for s,t in enumerate(nom_tec):
    df_s = mant_cer_mes.loc[mant_cer_mes['Nombre Técnico'] == t]
    mant_T = [{t:np.shape(df_s[df_s['Tipo de mantención'] == t])[0]} for t in T]
    aux[s] = {t:mant_T}
    
resultados = [aux[i] for i,j in enumerate(aux.items())]

percent_formatter = lambda x: '{:.2g}%'.format(x)

pie_chart = pygal.Pie(print_values = True)
pie_chart.title = "% de OT T1 cerradas v/s total mes\n{}".format(fecha)

if np.shape(mant_T1)[0]!=0:
    for x,y in enumerate(nom_tec):
        print(x,y,resultados[x][y][0]['T1'])
        #todas las generadas - las abiertas (generadas - cerradas)
        pie_chart.add(y,(resultados[x][y][0]['T1'])/np.shape(mant_T1)[0] * 100, formatter = percent_formatter)
    pie_chart.render_in_browser()
else:
    print("\nEn esta fecha no existen OT de tipo T1")

pie_chart = pygal.Pie(print_values = True)
pie_chart .title = "% de OT T2 cerradas v/s total mes\n{}".format(fecha)

if np.shape(mant_T2)[0]!=0:
    for x,y in enumerate(nom_tec):
        print(x,y,resultados[x][y][1]['T2'])
        #todas las generadas - las abiertas (generadas - cerradas)
        pie_chart .add(y,(resultados[x][y][1]['T2'])/np.shape(mant_T2)[0] * 100, formatter = percent_formatter)
    pie_chart.render_in_browser()
else:
    print("\nEn esta fecha no existen OT de tipo T2\nNo se desplegará gráfico")
    
# =============================================================================
#                           Sexto Indicador
# =============================================================================
import pandas as pd
import numpy as np

nom_tec = ['CARLOS LOBOS','FELIPE ACOSTA',
           'GUIDO VICENCIO','IGNACIO VALDIVIA',
           'PABLO SILVA']

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df = df[df['Estado UEM'].isin(['TRABAJO TERMINADO'])]
#df= df[df['Estado UEM'].map(lambda x: str(x)=="TRABAJO TERMINADO")]

#df.iloc[:,X] --> x =4, Equipo; x=12, HH; x=15, Nom_Tec; x=12, T_Mant;
df4 = pd.concat([df.iloc[:,4],df.iloc[:,12],df.iloc[:,15],df.iloc[:,32]], axis = 1, sort = False).dropna()

equipos = ['MONITOR', 'ANESTESIA', 'DESFIBRILADOR', 'VENTILADOR', 'INCUBADORA', 'ELECTROBIST']
df4['Equipo'] = df4['Equipo'].str.upper()

#Filtrar, del listado de equipos, aquellos que no pertenecen al listado de interés
df4 =  df4[~df4['Equipo'].isin(["SISTEMA DE MONITOREO MULTIPARAMETRO", 
           "AGITADOR DE PLAQUETAS (INCUBADORA Y AGITADOR)"])]

aux = pd.DataFrame([])

for i in equipos:
        aux = aux.append(df4[df4['Equipo'].str.contains(i)], ignore_index = True)

#Ante la posibilidad que la búsqueda de elementos coincida por alcance con otros, borramos estas alternativas.
aux = aux[~aux['Equipo'].isin(['MONITOR DESFIBRILADOR','MONITOR DESFIBRILADOR CON ECG'])]

#Filtramos técnicos que no figuran en la nómina de interés
aux = aux[aux['Nombre Técnico'].isin(nom_tec)]

#Filtramos las órdenes que no son del tipo de interés
aux = aux[aux['Tipo de mantención'].isin(['T1','T2'])]

equipo =  list(aux['Equipo'].unique())

tipo = ['T1','T2']
l = 0
tiempos =  {'T1':{'MONITOR':4, 'ANESTESIA':5,'DESFIBRILADOR':5, 'VENTILADOR':5,'INCUBADORA':3,'ELECTROBIST':4},'T2':{'MONITOR':5, 'ANESTESIA':6,'DESFIBRILADOR':6, 'VENTILADOR':6,'INCUBADORA':4,'ELECTROBIST':-1}}

while(l<np.shape(tipo)[0]):
    globals()['prom_hh_eq_tec_{}'.format(tipo[l])] = pd.DataFrame(columns=['Equipo','Tipo de mantención','Nombre Técnico','Horas Hombres'])
    globals()['tabla_{}'.format(tipo[l])] = pd.DataFrame([])
    
    for i in nom_tec:
        globals()['ord_{}'.format(i)] = aux[aux['Nombre Técnico']==i]
        globals()['ord_{}'.format(i)] = globals()['ord_{}'.format(i)][globals()['ord_{}'.format(i)]['Tipo de mantención']==tipo[l]]
    
        for j in equipo:
            aux1=  globals()['ord_{}'.format(i)][globals()['ord_{}'.format(i)]['Equipo']==j]
            promedio = aux1['Horas Hombres'].mean()

            aux2 = pd.DataFrame([[j,tipo[l],i,round(promedio,1)]],columns=['Equipo','Tipo de mantención','Nombre Técnico','Horas Hombres'])    
            globals()['prom_hh_eq_tec_{}'.format(tipo[l])] = globals()['prom_hh_eq_tec_{}'.format(tipo[l])].append(aux2).dropna() #NaN borrados. Usado para calcular apropiadamente el promedio de hh


    for x in equipos:
        for i in nom_tec:
            aux1 = globals()['prom_hh_eq_tec_{}'.format(tipo[l])][globals()['prom_hh_eq_tec_{}'.format(tipo[l])]['Equipo'].str.contains(x)]
            aux1 = aux1[aux1['Nombre Técnico']==i]
            
            if np.shape(aux1)[0]!=0:                
                aux4 = pd.DataFrame(np.array([[x,tipo[l], i, round(aux1['Horas Hombres'].mean(),2)]]),columns =['Equipo','Tipo de mantención','Nombre Técnico','Horas Hombres Prom'])
                globals()['tabla_{}'.format(tipo[l])] = globals()['tabla_{}'.format(tipo[l])].append(aux4).dropna()
            else:
                pass


    for j in equipos:
        for i in range(np.shape(globals()['tabla_{}'.format(tipo[l])])[0]):
            if globals()['tabla_{}'.format(tipo[l])].iloc[i,0] == j:
                # globals()['tabla_{}'.format(tipo[l])].iloc[i,3] = str(round(float(globals()['tabla_{}'.format(tipo[l])].iloc[i,3])/tiempos[tipo[l]][str(j)],1)*100) +'%'
                globals()['tabla_{}'.format(tipo[l])].iloc[i,3] = round(float(globals()['tabla_{}'.format(tipo[l])].iloc[i,3])/tiempos[tipo[l]][str(j)],1)
    
    # =============================================================================
    # Grafico  
    # =============================================================================
                
    line_chart = pygal.Bar()
    line_chart.title = 'Eficiencia técnicos atenciones de tipo ' + tipo[l]
    line_chart.x_labels = map(str, nom_tec)
    
    line_chart.add('Hola', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.render_to_file('line_chart_'+tipo[l]+'.svg')
    line_chart.render_in_browser()
    l+=1

# =============================================================================
# Subir codigo
# =============================================================================
!git add .
!git commit -m "mensaje"
!git push