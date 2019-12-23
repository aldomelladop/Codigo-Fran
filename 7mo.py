# =============================================================================
#              Séptimo indicador (N° de órdenes pendientes en 6 meses)
# =============================================================================
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,1]) #Estado UEM

df2 = pd.DataFrame(df.iloc[:,20]) #Fecha de inicio
df2 = pd.DataFrame([j if type(j)!=str and j!='00-00-00000' else "NaN" for i,j in enumerate(df2['Fecha Inicio'])], columns = ['Fecha Inicio']).dropna()
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])

df3 = df1.join(df2)
df3 = df3[df3['Estado UEM'].notnull()]
df3 = df3[df3['Fecha Inicio'].notnull()]

flag = True
while flag:
    mes = input('\nIngrese Mes a buscar: ')
    año = input('\nIngrese Año a buscar: ')
    if len(mes)==0 or len(año)==0:
        print("\nFavor ingrese un año y un mes válidos\n")
    else:
        flag = False
        
fecha  = datetime.strptime(año +"-" +mes + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
fechas = [fecha - timedelta(365*i/12) for i in range(1,7)]

#Si en lugar de solo guardar los trabajos ocurridos esa fecha, guardo también la de los 6 meses posteriores, podría entonces, 
#Hacer un filtro solo con este comando

#Convertir todos los elementos en el dataframe para poder hacer uso del método str.contains() y compararlo con las fechas

df_total_mes = pd.DataFrame([],columns = ['Estado UEM','Fecha Inicio'])

for i in fechas:
    df_total_mes = df_total_mes.append(df3[df3['Fecha Inicio'].str.contains(str(i.year) + "-" + str(i.month))], ignore_index = True)


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