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
porcentaje = round((num_pendientes/num_trab) * 100,1)

import pygal

pie_chart = pygal.Pie()
pie_chart.title = "Trabajos pendientes v/s Trabajos Cerrados en los 6 meses previos a {}".format(str(fecha.year)+'-'+
                                                                                                 str(fecha.month))
pie_chart.add("Trabajos Pendientes", porcentaje)
pie_chart.add('Trabajo Terminado', 100-porcentaje)
pie_chart.render_in_browser()

# =============================================================================
# Noveno Indicador
# =============================================================================
# Si en input pongo "SN" debe decirme cuantas veces aparece SN entre la fecha que indique
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from contains0 import contains0

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
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
    else:
        print(f"type(m1) = {type(m1)}\ntype(m2) = {type(m2)}")
        m1 = contains0(m1)
        m2 = contains0(m2)flag = True

        f1  = datetime.strptime(a1 +"-" +m1 + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
        f2  = datetime.strptime(a2 +"-" +m2 + '-28 08:15:27.243860', '%Y-%m-%d %H:%M:%S.%f')
        
        flag = False
        print(f"\nelse:\nm1 = {m1}, m2 = {m2}")
        
# =============================================================================
#   Revisar si el numero contiene 0 o no. En caso que no, agregarlo. 
#       En caso que si, conservarlo. (listo)
#   Filtrar por Serie  [listo]
#   Filtrar entre fechas [listo]
#   Contar filas  np.shape(filtro_serie)[0]
# =============================================================================

# Filtrar por serie
filtro_serie = df4[df4['Serie'].str.contains(serie)]
# diferencia entre fechas 
# Representa la cantidad de meses y años que hay de diferencia entre la f1 y la f2


dbd = (f2 -f1).days/30
fechas = [f2 - timedelta(365*i/12) for i in range(0,int(dbd)+1)]
fechas = [str(j.year) +'-'+str(j.month) for i,j in enumerate(fechas)]

aux = pd.DataFrame([])

for i in fechas:
    aux = aux.append(filtro_serie[filtro_serie['Fecha recepcion OT'].str.contains(i)], ignore_index = True)
    if filtro_serie['Fecha recepcion OT'].str.contains(i) == True:
        print(np.shape(aux))
    else:
        print('Pato')


# =============================================================================
# Subir codigo
# =============================================================================
!git add .
!git commit -m "mensaje"
!git push