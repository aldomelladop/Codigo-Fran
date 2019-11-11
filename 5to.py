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

mes = input('\nIngrese Mes a buscar: ')
año = input('\nIngrese Año a buscar: ')

fecha  = año +"-" +mes

mant_mes_ab  = df4[df4['Fecha Inicio' ].str.contains(fecha)]
mant_mes_cr  = mant_mes_ab[mant_mes_ab['Fecha Termino6' ].str.contains(fecha)]
mant_T2 = mant_mes_cr[mant_mes_cr['Tipo de mantención'] == 'T2']
mant_T2 = np.shape(mant_mes_cr[mant_mes_cr['Tipo de mantención'] == 'T2'])[0]

# Numero de OT T2 Generadas en la fecha ingresada
mant_T2_ab = np.shape(mant_mes_ab[mant_mes_ab['Tipo de mantención'] == 'T2'])[0]

# Numero de OT T2 Cerradas en la fecha ingresada
mant_T2_cr = np.shape(mant_mes_cr[mant_mes_cr['Tipo de mantención'] == 'T2'])[0]

T = ["T2"]
aux = {}

for s,t in enumerate(nom_tec):
    df_s = mant_mes_cr.loc[mant_mes_cr['Nombre Técnico'] == t]
    mant_T2 = [{t:np.shape(df_s[df_s['Tipo de mantención'] == t])[0]} for t in T]
    aux[s] = {t:mant_T2}
    
resultados = [aux[i] for i,j in enumerate(aux.items())]

percent_formatter = lambda x: '{:.2g}%'.format(x)

pie_chart = pygal.Pie(print_values = True)
pie_chart .title = "% de OT T2 cerradas v/s total mes".format(fecha)

flag =  any(mant_T2_ab.iloc[:,1])# verifica que la cantidad de OT para las unidades no sea 0

if flag==True: #Si la cantidad de OT para las unidades no es 0, entonces:
    for x,y in enumerate(nom_tec):
        pie_chart .add(y,((mant_T2_ab - resultados[x][y][0]['T2'])/mant_T2_ab) * 100, formatter = percent_formatter)
        pie_chart.render_in_browser()
else: #en cambio, si no hubieron OT para ninguna unidad, entonces:
    print("\nEn esta fecha no existen OT de tipo T2 cerradas")