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