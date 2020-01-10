# =============================================================================
#   Octavo Indicador
# =============================================================================
    # Evaluar la productividad y cumplimiento de la unidad relacionando con el
    # N° de OT cerradas y  OT acumuladas los ultimos 6 meses    
    
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

df = pd.read_excel('PLANILLA GESTION UEM 2018 OFICIAL.xlsx')
df1 = pd.DataFrame(df.iloc[:,1]) #Estado UEM

df2 = pd.DataFrame(df.iloc[:,20]) #Fecha de inicio
df2 = pd.DataFrame([j if type(j)!=str and j!='00-00-00000' else np.nan for i,j in enumerate(df2['Fecha Inicio'])], columns = ['Fecha Inicio']).dropna()
df2 = pd.DataFrame([str(j) for i,j in enumerate(df2['Fecha Inicio'])],dtype=object, columns = ['Fecha Inicio'])

df3 = df1.join(df2).dropna()

# flag = True
# while flag:
#     mes = input('\nIngrese Mes a buscar: ')
#     año = input('\nIngrese Año a buscar: ')
#     if len(mes)==0 or len(año)==0:
#         print("\nFavor ingrese un año y un mes válidos\n")
#     else:
#         flag = False
        
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
    print(f"num_trab  = {num_trab}")
