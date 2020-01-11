#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 21:31:42 2019
@author: aldo_mellado
"""
# =============================================================================
# Import global
# =============================================================================
from datetime import datetime
from datetime import timedelta

# =============================================================================
#                                      Dashboard
# =============================================================================
from bokeh.io import output_file, show
from bokeh.layouts import gridplot
from bokeh.plotting import figure

from math import pi

import pandas as pd

from bokeh.palettes import Category20c,Category20
from bokeh.palettes import Oranges, Spectral6
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, FactorRange

output_file("dashboard.html")

pw, ph = 500,500

# =============================================================================
#                               Primer indicador 
#                       (% de órdenes cerradas en el mes)
# =============================================================================
import numpy as np
from contains0 import contains0

print(f"\n* Primer indicador")
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

print(f"\n\tPrimer Indicador listo\n")

# =============================================================================
#                              DASHBOARD INDICADOR 1
# =============================================================================

x = {'Cerradas': porcentaje,'Pendientes': round(100-porcentaje,2),'':0}

data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'country'})
data['angle'] = data['value']/sum(x.values()) * 2*pi
data['color'] = Category20c[len(x)]

s1 = figure(plot_height=350, title="% OT Cerradas en {}".format(fecha), toolbar_location=None,
           tools="hover", tooltips=[("Country", "@country"),("Value", "@value")])

s1.annular_wedge(x=0, y=1, inner_radius=0.2, outer_radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_label='country', source=data)

s1.axis.axis_label=None
s1.axis.visible= False
s1.grid.grid_line_color = None
    
# =============================================================================
#                               Segundo Indicador (?)
# En esta parte haremos que se solicite un mes y una unidad en particular, 
# para entonces, mostrar las órdenes de trabajo asociadas a dicha unidad en dicho mes.
# =============================================================================

import pandas as pd
import numpy as np

print(f"\n* Segundo Indicador")
# df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,3]).dropna() #unidad

df2 = pd.DataFrame(df.iloc[:,9]) #fecha recepción OT
df2 = df2[df2['Fecha recepcion OT'] !='00-00-0000']
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha recepcion OT'])],dtype=object, columns = ['Fecha recepcion OT']) #Fecha convertida a str para luego buscar fecha

df3 = df1.join(df2).dropna() #Unir ambos dataFrame para relacionarlos

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
    ocurrencias[i] = num_ot_uni_mes
    
num_to_filter = 3 #Cantidad de valores a filtrar
ocurr = pd.DataFrame(sorted(ocurrencias.items(), key = lambda x:x[1], reverse = True)).iloc[:num_to_filter,:]
flag =  any(ocurr.iloc[:,1])# verifica que la cantidad de OT para las unidades no sea 0

# =============================================================================
#                                  DASHBOARD INDICADOR 2          
# =============================================================================

x  = {}
for i in range(num_to_filter):
    if ocurr.iloc[i,1] !=0:
        aux =  {'{}'.format(ocurr.iloc[i,0]): round((ocurr.iloc[i,1]/num_trab)*100,2)}    
    else: 
        print(f"\nEn esta fecha para {ocurr.iloc[i,0]} no existen OT")
    
    x.update(aux) 

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'unidad'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20[len(x)]

s2 = figure(plot_width=pw, plot_height=ph, title="Num_SoU/Num tot Trab {} ".format(fecha), toolbar_location=None,
           tools="hover", tooltips="@unidad: @value", x_range=(-0.5, 1.0))
s2.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='unidad', source=data)
s2.axis.axis_label=None
s2.axis.visible=False
s2.grid.grid_line_color = None
print(f"\n\tSegundo Indicador listo")

# =============================================================================
#                                   INDICADOR 3          
# =============================================================================

print(f"\n* Tercer Indicador")
nom_tec = ['CARLOS LOBOS','FELIPE ACOSTA',
           'GUIDO VICENCIO','IGNACIO VALDIVIA',
           'PABLO SILVA']

# (suma de todas las ordenes T1 generadas en el mes - sum ordenes T1 abiertas en el mes)/suma de todas las ordenes T1 generadas en el mes

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

mant_mes_ab  = df4[df4['Fecha Inicio' ].str.contains(fecha)]

print(f"\n\t\tLa cantidad de órdenes abiertas en {fecha} es: {np.shape(mant_mes_ab)[0]}")

mant_mes_cr  = mant_mes_ab[mant_mes_ab['Fecha Termino6' ].str.contains(fecha)]

print(f"\t\tLa cantidad de órdenes cerradas en {fecha} es: {np.shape(mant_mes_cr)[0]}\n")

# =============================================================================
#                               DASHBOARD INDICADOR 3
# =============================================================================
fruits = ['N° Órdenes Abiertas', 'N° Órdenes Cerradas']
counts = [np.shape(mant_mes_ab)[0],np.shape(mant_mes_cr)[0]]

source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6[:2]))
s3 = figure(x_range=fruits, y_range=(0,np.max(counts)+50), plot_height=ph, title="OT abiertas y cerradas",
           toolbar_location=None, tools="")
s3.vbar(x='fruits', top='counts', width=0.5, color='color', legend_field="fruits", source=source)
s3.xgrid.grid_line_color = None
s3.legend.orientation = "horizontal"
s3.legend.location = "top_center"
print(f"\n\tTercer Indicador listo")

# =============================================================================
#                              Cuarto y Quinto Indicador 
#       (Porcentaje de Atenciones cerradas netas de tipo T1 y T2 por tecnicos)
# =============================================================================

print(f"\n* Cuarto Indicador")

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

# =============================================================================
mant_mes  = df4[df4['Fecha Inicio'].str.contains(fecha)]

# Órdenes de tipo T1 generadas en la fecha

mant_T1 = mant_mes[mant_mes['Tipo de mantención'] == 'T1']
mant_T1 = mant_T1[mant_T1['Nombre Técnico'].isin(nom_tec)]

mant_T2 = mant_mes[mant_mes['Tipo de mantención'] == 'T2']
mant_T2 = mant_T2[mant_T2['Nombre Técnico'].isin(nom_tec)] #elimina todos las filas que contenian informacion sobre atención realizadas por personas que no eran técnicos

#Órdenes cerradas de tipo T1 y T2 en esa fecha
mant_cer_mes = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_mes = mant_cer_mes[mant_cer_mes['Nombre Técnico'].isin(nom_tec)]

mant_cer_T1 = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_T1 = mant_cer_T1[mant_cer_T1['Nombre Técnico'].isin(nom_tec)]
mant_cer_T1 = mant_cer_T1[mant_cer_T1['Tipo de mantención']=='T1']

mant_cer_T2 = df4[df4['Fecha Termino6'].str.contains(fecha)]
mant_cer_T2 = mant_cer_T2[mant_cer_T2['Nombre Técnico'].isin(nom_tec)]
mant_cer_T2 = mant_cer_T2[mant_cer_T2['Tipo de mantención']=='T2']

T = ["T1", "T2"]
aux = {}

#Ordenes de tipo T1 cerradas por técnico
for s,t in enumerate(nom_tec):
    df_s = mant_cer_mes.loc[mant_cer_mes['Nombre Técnico'] == t]
    mant_T = [{t:np.shape(df_s[df_s['Tipo de mantención'] == t])[0]} for t in T]
    aux[s] = {t:mant_T}
    
resultados = [aux[i] for i,j in enumerate(aux.items())]

tipos = {'T1':{},'T2':{}}

if np.shape(mant_T1)[0]!=0:
    for x,y in enumerate(nom_tec):
        aux = {y:resultados[x][y][0]['T1']}
        tipos['T1'].update(aux)
else:
    print("\nEn esta fecha no existen OT de tipo T1")

if np.shape(mant_T2)[0]!=0:
    for x,y in enumerate(nom_tec):
        tipos['T2'].update({y:resultados[x][y][1]['T2']})
else:
    tipos['T2'].update({y:0})
    print("\nEn {} no existen OT de tipo T2".format(fecha))

# =============================================================================
#                                 INDICADOR 4 y 5         
# =============================================================================

factors = [(i, 'T1') for i in tipos['T1'].keys()] +[(i, 'T2') for i in tipos['T2'].keys()]

s4 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(fecha),
           toolbar_location=None, tools="")
x = [tipos['T1'][i]  for i in tipos['T1'].keys()] +[tipos['T2'][i] for i in tipos['T2'].keys()]
s4.vbar(x=factors, top=x, width=0.4, alpha=0.5)
s4.y_range.start = 0
s4.x_range.range_padding = 0.05
s4.xaxis.major_label_orientation = 1
s4.xgrid.grid_line_color = None

print(f"\n\tCuarto Indicador listo")
print(f"\n* Quinto Indicador")
print(f"\n\tQuinto Indicador listo")
# =============================================================================
#                           Sexto-Séptimo Indicador
# =============================================================================

print(f"\n* Sexto Indicador")

nom_tec = ['CARLOS LOBOS','FELIPE ACOSTA',
           'GUIDO VICENCIO','IGNACIO VALDIVIA',
           'PABLO SILVA']

# df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = df[df['Estado UEM'].isin(['TRABAJO TERMINADO'])]
df4 = pd.concat([df1.iloc[:,4],df1.iloc[:,12],df1.iloc[:,15],df1.iloc[:,32]], axis = 1, sort = False).dropna()

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
                globals()['tabla_{}'.format(tipo[l])].iloc[i,3] = round(float(globals()['tabla_{}'.format(tipo[l])].iloc[i,3])/tiempos[tipo[l]][str(j)],1)
    l+=1

# =============================================================================
#                                     INDICADOR 6
# =============================================================================
factors = [(tabla_T1.iloc[i,2],tabla_T1.iloc[i,0]) for i in range(0,np.shape(tabla_T1)[0])]
s6 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(fecha),
           toolbar_location=None, tools="")
x = [tabla_T1.iloc[i,3] for i in range(0,np.shape(tabla_T1)[0])]
s6.vbar(x=factors, top=x, width=0.3, alpha=1)
s6.y_range.start = 0
s6.x_range.range_padding = 0.2
s6.xaxis.major_label_orientation = 1
s6.xgrid.grid_line_color = None
print(f"\n\tSexto Indicador listo")

# =============================================================================
#                                     INDICADOR 7
# =============================================================================
print(f"\n* Séptimo Indicador")
try:
    factors = [(tabla_T2.iloc[i,2],tabla_T2.iloc[i,0]) for i in range(0,np.shape(tabla_T2)[0])]

    s7 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(str(fecha.year) + '-' + contains0(str(fecha.month))),
               toolbar_location=None, tools="")
    x = [tabla_T2.iloc[i,3] for i in range(0,np.shape(tabla_T2)[0])]
    s7.vbar(x=factors, top=x, width=0.4, alpha = 1)
    s7.y_range.start = 0
    s7.x_range.range_padding = 0.05
    s7.xaxis.major_label_orientation = 1
    s7.xgrid.grid_line_color = None
except:
    print("\n\tNo existen órdenes de Tipo T2 en {}".format(fecha))
    s7 = None
print(f"\n\tSéptimo Indicador listo\n")

# =============================================================================
#                               Octavo Indicador
# =============================================================================
    # Evaluar la productividad y cumplimiento de la unidad relacionando con el
    # N° de OT cerradas y  OT acumuladas los ultimos 6 meses    

print(f"\n* Octavo Indicador")

df1 = pd.DataFrame(df.iloc[:,1]) #Estado UEM

df2 = pd.DataFrame(df.iloc[:,20]) #Fecha de inicio
df2 = pd.DataFrame([j if type(j)!=str and j!='00-00-00000' else np.nan for i,j in enumerate(df2['Fecha Inicio'])], columns = ['Fecha Inicio']).dropna()
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])

df3 = df1.join(df2).dropna()

fecha  = datetime.strptime(año +"-" +mes + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
fechas = [fecha - timedelta(365*i/12) for i in range(1,7)]

#Si en lugar de solo guardar los trabajos ocurridos esa fecha, guardo también la de los 6 meses posteriores, podría entonces, 
#Hacer un filtro solo con este comando

#Convertir todos los elementos en el dataframe para poder hacer uso del método str.contains() y compararlo con las fechas

df_total_mes = pd.DataFrame([],columns = ['Estado UEM','Fecha Inicio'])

for i in fechas:
    if len(str(i.month))==1:
        aux = str(i.year) + "-0" + str(i.month)
    else:
        aux = str(i.year) + "-" + str(i.month)
        
    j = np.shape(df3[df3['Fecha Inicio'].str.contains(aux)])
    
    if j[0]!=0:
        k = df3[df3['Fecha Inicio'].str.contains(aux)].iloc[1,:]

    df_total_mes = pd.concat([df_total_mes, df3[df3['Fecha Inicio'].str.contains(aux)]])
    
# Se buscan el índice de los elementos en la columna 'Estado UEM' que satisfacen la condicion de decir 'TRABAJO TERMINADO'
ord_pend = df_total_mes[~df_total_mes['Estado UEM'].isin(['TRABAJO TERMINADO'])]

num_pendientes = np.shape(ord_pend)[0]
num_trab = np.shape(df_total_mes)[0]

#calculo porcentaje
if num_trab!=0:
    porcentaje_c = round((num_pendientes/num_trab) * 100,1)
else:
    print(f"\tnum_trab  = {num_trab}\n")

# =============================================================================
#                                   INDICADOR 8
# =============================================================================
x  = {'Terminada': 100-porcentaje_c, 'Pendiente':porcentaje_c, '':0}

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'unidad'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Oranges[len(x)]

s8 = figure(plot_width=pw, plot_height=ph, title="Num_SoU/Num tot Trab {} ".format(str(fecha.year) + '-' + contains0(str(fecha.month))), toolbar_location=None,
           tools="hover", tooltips="@unidad: @value", x_range=(-0.5, 1.0))
s8.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='unidad', source=data)
s8.axis.axis_label=None
s8.axis.visible=False
s8.grid.grid_line_color = None

print(f"\n\tOctavo Indicador listo")

# =============================================================================
#                                   Noveno Indicador
# =============================================================================
# Si en input pongo "SN" debe decirme cuantas veces aparece SN entre la fecha que indique

print(f"\nNoveno Indicador\n")

df1 = pd.DataFrame(df.iloc[:,7])# Serie
df1 = pd.DataFrame([np.nan if j in ['SN','S/N','sn','na','nan'] else str(j) for i,j in enumerate(df1['Serie'])], columns = ['Serie'])
df1 = df1.dropna()

df2 = pd.DataFrame(df.iloc[:,9]) #Fecha recepción
df2 = pd.DataFrame([str(j) if type(j)!=str and j!='00-00-00000' else np.nan for i,j in enumerate(df2['Fecha recepcion OT'])], columns = ['Fecha recepcion OT'])
df2 = df2.dropna()

df3 = pd.DataFrame(df.iloc[:,11]) #Clasificación
df3 = pd.DataFrame([j if j=='MCC' else np.nan for i,j in enumerate(df3['Clasificación'])], columns = ['Clasificación'])
df3 = df3.dropna()

df4 = df1.join([df2,df3]).dropna()

flag = True

while flag:
    serie = input('\nIngrese Equipo (Serie) a buscar: ')
    print('\nIngrese Fecha Inicio  (f1) de búsqueda: ')
    a1 = input('\tAño: ')
    m1 = input('\tMes: ')
    
    print('\nIngrese Fecha término (f2) de búsqueda: ')
    a2 = input('\tAño: ')
    m2 = input('\tMes: ')
    
    if len(a2)==0 or len(a2)==0 or len(m1)==0 or len(m2)==0:
        print("\nFavor corrija los datos ingresados por uno válido\n")
    elif a2<a1:
        print(f"\nEl año de término {a2} es menor que el año de inicio {a1}\n")
    else:
        # print(f"type(m1) = {type(m1)}\ntype(m2) = {type(m2)}")
        m1 = contains0(m1)
        m2 = contains0(m2)

        f1  = datetime.strptime(a1 +"-" +m1 + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
        f2  = datetime.strptime(a2 +"-" +m2 + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
        
        flag = False
        # print(f"\nelse:\nm1 = {m1}, m2 = {m2}")
    
# Filtrar por serie
filtro_serie = df4[df4['Serie'].str.contains(serie)]
# diferencia entre fechas 
# Representa la cantidad de meses y años que hay de diferencia entre la f1 y la f2

dbd = (f2 -f1).days/30
fechas = [f2 - timedelta(365*i/12) for i in range(0,int(dbd)+1)]
fechas = [str(j.year) +'-'+ str(contains0(str(j.month))) for i,j in enumerate(fechas)]

aux = pd.DataFrame([])

for i in fechas:
    aux = aux.append(filtro_serie[filtro_serie['Fecha recepcion OT'].str.contains(i)], ignore_index = True)

contador = np.shape(aux)[0]
print(f"La cantidad de ocurrencias entre las fechas {str(f1.year) + '-' + str(f1.month)}- {str(f2.year) + '-' + str(f2.month)} para el equipo {serie} es: {contador}")

# =============================================================================
#                                   INDICADOR 9
# =============================================================================

# factors = [(i, 'T1') for i in tipos['T1'].keys()] +[(i, 'T2') for i in tipos['T2'].keys()]

# s9 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerlegendradas v/s total mes\n{}".format(str(fecha.year) + '-' + contains0(str(fecha.month))),
#            toolbar_location=None, tools="")
# x = [tipos['T1'][i]  for i in tipos['T1'].keys()] +[tipos['T2'][i] for i in tipos['T2'].keys()]
# s9.vbar(x=factors, top=x, width=0.4, alpha=0.5)
# s9.y_range.start = 0
# s9.x_range.range_padding = 0.05
# s9.xaxis.major_label_orientation = 1
# s9.xgrid.grid_line_color = None

fruits = ['Equipo 1']
counts = [70]

source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6))
s9 = figure(x_range=fruits, y_range=(0,100), plot_height=ph, title="Reincidencias por equipo",
           toolbar_location=None, tools="")
s9.vbar(x='fruits', top='counts', width=0.7, color='color', legend_field="fruits", source=source)
s9.xgrid.grid_line_color = None
s9.legend.orientation = "horizontal"
s9.legend.location = "top_center"

print(f"\n\tNoveno Indicador listo")
# =============================================================================
#                       GENERAR DASHBOARD
# =============================================================================

grid = gridplot([[s1, s2, s3], 
                 [None,s4,None],
                 [s6,None, s7],
                 [s8,None, s9]], 
                    plot_width=pw, plot_height=ph)
show(grid)