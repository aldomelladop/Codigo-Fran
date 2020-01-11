from bokeh.io import output_file, show
from bokeh.layouts import column, row, gridplot
from bokeh.plotting import figure

from math import pi

import pandas as pd

from bokeh.palettes import Category20c,Category20
from bokeh.palettes import Cividis, Oranges, Spectral6
from bokeh.transform import cumsum, factor_cmap
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

factors = [(i, 'T1') for i in tipos['T1'].keys()] +[(i, 'T2') for i in tipos['T2'].keys()]

s4 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(str(fecha.year) + '-' + contains0(str(fecha.month))),
           toolbar_location=None, tools="")
x = [tipos['T1'][i]  for i in tipos['T1'].keys()] +[tipos['T2'][i] for i in tipos['T2'].keys()]
s4.vbar(x=factors, top=x, width=0.4, alpha=0.5)
s4.y_range.start = 0
s4.x_range.range_padding = 0.05
s4.xaxis.major_label_orientation = 1
s4.xgrid.grid_line_color = None

# =============================================================================
# INDICADOR 6
# =============================================================================
factors = [(tabla_T1.iloc[i,2],tabla_T1.iloc[i,0]) for i in range(0,np.shape(tabla_T1)[0])]
s6 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerradas v/s total mes\n{}".format(str(fecha.year) + '-' + contains0(str(fecha.month))),
           toolbar_location=None, tools="")
x = [tabla_T1.iloc[i,3] for i in range(0,np.shape(tabla_T1)[0])]
# source = ColumnDataSource(data=dict(x=x, counts=factors))

# s6.vbar(x='x', top='x', width=0.3, alpha = 1, legend_field = 'factors', source=source, line_color="white",

#        # use the palette to colormap based on the the x[1:2] values
#        fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=2))

# s6.vbar(x=factors, top=x, width=0.3, alpha=1, legend_field="factors",fill_color=factor_cmap('factors', palette=Category20c, factors=factors))
s6.vbar(x=factors, top=x, width=0.3, alpha=1)
s6.y_range.start = 0
s6.x_range.range_padding = 0.2
s6.xaxis.major_label_orientation = 1
s6.xgrid.grid_line_color = None

# =============================================================================
# INDICADOR 7
# =============================================================================
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
    print("No existen órdenes de Tipo T2 en {}".format(fecha))

          
# INDICADOR 8
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

    
# INDICADOR 9

factors = [(i, 'T1') for i in tipos['T1'].keys()] +[(i, 'T2') for i in tipos['T2'].keys()]

s9 = figure(x_range=FactorRange(*factors), plot_height=ph, title="% de OT cerlegendradas v/s total mes\n{}".format(str(fecha.year) + '-' + contains0(str(fecha.month))),
           toolbar_location=None, tools="")
x = [tipos['T1'][i]  for i in tipos['T1'].keys()] +[tipos['T2'][i] for i in tipos['T2'].keys()]
s9.vbar(x=factors, top=x, width=0.4, alpha=0.5)
s9.y_range.start = 0
s9.x_range.range_padding = 0.05
s9.xaxis.major_label_orientation = 1
s9.xgrid.grid_line_color = None

          
# make a grid
# grid = gridplot([[None, s1, s2, s3, None], 
#                  [None, s4, None, s6, None],
#                  [None, s7, s8, s9, None]], 
#                     plot_width=pw, plot_height=ph)

grid = gridplot([[s1, s2, s3], 
                 [None,s4,None],
                 [s6,None, s7],
                 [s8,None, s9]], 
                    plot_width=pw, plot_height=ph)
show(grid)
