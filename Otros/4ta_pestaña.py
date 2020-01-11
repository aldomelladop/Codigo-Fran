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
    
    print('\nIngrese Fecha Término (f2) de búsqueda: ')
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
fechas = [str(j.year) +'-'+ str(contains0(str(j.month))) for i,j in enumerate(fechas)]

aux = pd.DataFrame([])

for i in fechas:
    aux = aux.append(filtro_serie[filtro_serie['Fecha recepcion OT'].str.contains(i)], ignore_index = True)

contador = np.shape(aux)[0]
print(f"La cantidad de ocurrencias entre las fechas {str(f1.year) + '-' + str(f1.month)}- {str(f2.year) + '-' + str(f2.month)} para el equipo {serie} es: {contador}")