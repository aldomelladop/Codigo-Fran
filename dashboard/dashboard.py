from bokeh.io import output_file, show
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure
from math import pi

import pandas as pd

from bokeh.palettes import Category20c
from bokeh.palettes import Spectral6
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, FactorRange

output_file("dashboard.html")

pw, ph = 500,500

# INDICADOR 1

# x = {'other': 258, 'services': 136, 'at_home': 135, 'teacher': 72, 'health': 48}
x = {'Cerradas': porcentaje,'Pendientes': round(100-porcentaje,2),'':0}

data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'country'})
data['angle'] = data['value']/sum(x.values()) * 2*pi
data['color'] = Category20c[len(x)]

s1 = figure(plot_height=350, title="% OT Cerradas en {}".format(fecha), toolbar_location=None,
           tools="hover", tooltips=[("Country", "@country"),("Value", "@value")])

s1.annular_wedge(x=0, y=1, inner_radius=0.2, outer_radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend='country', source=data)

s1.axis.axis_label=None
s1.axis.visible= False
s1.grid.grid_line_color = None
                    
# INDICADOR 2          

# x = { 'Oftalmología': 157, 'Pediatría': 93}
x  = {}
for i in range(num_to_filter):
    if ocurr.iloc[i,1] !=0:
        aux =  {'{}'.format(ocurr.iloc[i,0]): round((ocurr.iloc[i,1]/num_trab)*100,2)}    
    else: 
        print(f"\nEn esta fecha para {ocurr.iloc[i,0]} no existen OT")
    
    x.update(aux) 

data = pd.Series(x).reset_index(name='value').rename(columns={'index':'unidad'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(x)]
# data['color'] = chart_colors[:len(x)]

#print(data)
s2 = figure(plot_width=pw, plot_height=ph, title="Num_SoU/Num tot Trab {} ".format(fecha), toolbar_location=None,
           tools="hover", tooltips="@unidad: @value", x_range=(-0.5, 1.0))
s2.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='unidad', source=data)
s2.axis.axis_label=None
s2.axis.visible=False
s2.grid.grid_line_color = None


# INDICADOR 3          

fruits = ['N° Órdenes Abiertas', 'N° Órdenes Cerradas']
counts = [np.shape(mant_mes_ab)[0],np.shape(mant_mes_cr)[0]]

source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6))
s3 = figure(x_range=fruits, y_range=(0,np.max(counts)+50), plot_height=ph, title="OT abiertas y cerradas",
           toolbar_location=None, tools="")
s3.vbar(x='fruits', top='counts', width=0.5, color='color', legend_field="fruits", source=source)
s3.xgrid.grid_line_color = None
s3.legend.orientation = "horizontal"
s3.legend.location = "top_center"

# INDICADOR 4 y 5         

# factors = [ (tipos[i].keys(),)
#     ("Técnico 1", "Tipo 1"), ("Técnico 1", "Tipo 2"),
#     ("Técnico 2", "Tipo 1"), ("Técnico 2", "Tipo 2"),
#     ("Técnico 3", "Tipo 1"), ("Técnico 3", "Tipo 2"),
#     ("Técnico 4", "Tipo 1"), ("Técnico 4", "Tipo 2"),
# ]

factors = [(i, 'T1') for i in tipos['t1'].keys()] +[(i, 'T2') for i in tipos['t2'].keys()]

s4 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(fecha),
           toolbar_location=None, tools="")
x = [tipos['t1'][i]  for i in tipos['t1'].keys()] +[tipos['t2'][i] for i in tipos['t2'].keys()]
s4.vbar(x=factors, top=x, width=0.9, alpha=0.5)
# s4.line(x=["Técnico 1", "Técnico 2", "Técnico 3", "Técnico 4"], y=[9, 6, 11, 7], color="red", line_width=2)
s4.y_range.start = 0
s4.x_range.range_padding = 0.1
s4.xaxis.major_label_orientation = 1
s4.xgrid.grid_line_color = None


# INDICADOR 6 y 7

x = list(range(11))
y0 = x
y1 = [10 - i for i in x]
y2 = [abs(i - 5) for i in x]

s6 = figure(plot_width=250, plot_height=250, background_fill_color="#fafafa")
s6.square(x, y2, size=12, color="#d95b43", alpha=0.8)

s7 = figure(plot_width=250, plot_height=250, background_fill_color="#fafafa")
s7.square(x, y2, size=12, color="#d95b43", alpha=0.8)

          
# INDICADOR 8
fruits = ['Pendientes', 'Terminadas']
counts = [70, 30]
source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6))
s8 = figure(x_range=fruits, y_range=(0,100), plot_height=ph, title="OT pendientes últimos 6 meses",
           toolbar_location=None, tools="")
s8.vbar(x='fruits', top='counts', width=0.7, color='color', legend_field="fruits", source=source)
s8.xgrid.grid_line_color = None
s8.legend.orientation = "horizontal"
s8.legend.location = "top_center"

# INDICADOR 9

fruits = ['Equipo 1', 'Equipo 2', 'Equipo 3', 'Equipo 4', 'Equipo 5', 'Equipo 6']
counts = [70, 30, 40, 12, 15, 22]
source = ColumnDataSource(data=dict(fruits=fruits, counts=counts, color=Spectral6))
s9 = figure(x_range=fruits, y_range=(0,100), plot_height=ph, title="Reincidencias por equipo",
           toolbar_location=None, tools="")
s9.vbar(x='fruits', top='counts', width=0.7, color='color', legend_field="fruits", source=source)
s9.xgrid.grid_line_color = None
s9.legend.orientation = "horizontal"
s9.legend.location = "top_center"


          
# make a grid
# grid = gridplot([[None, s1, s2, s3, None], 
#                  [None, s4, None, s6, None],
#                  [None, s7, s8, s9, None]], 
#                     plot_width=pw, plot_height=ph)

grid = gridplot([[None, s1, s2, None, None], 
                 [None, s3, s4, None, None],
                 [None, None, None, None, None]], 
                    plot_width=pw, plot_height=ph)
show(grid)