from datetime import date
import pandas as pd
import numpy as np
from bokeh.plotting import figure,output_file,ColumnDataSource,curdoc
from bokeh.io import curdoc
from bokeh.models import HoverTool, FactorRange, Label
from bokeh.models import DatePicker, WidgetBox, Tabs, Panel, TextInput
from bokeh.transform import factor_cmap
from bokeh.layouts import column, row

def tab1():
    data = pd.read_csv('latimes-state-totals.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    max_date=data['date'].iloc[0]
    s_date = pd.to_datetime('20200801')
    e_date = pd.to_datetime('20200831')
    data = data[(data['date_time'] >= s_date) & (data['date_time'] <= e_date)]
    output_file('resulting.html')
    p =  figure(y_axis_label='New cases',title='New confirmed cases of Coronavirus in CA on August',x_axis_type='datetime')
    r = p.line('date_time','new_confirmed_cases',source=data)
    p.add_tools(HoverTool(
        tooltips=[
            ('date',"@date_time{%Y-%m-%d}"),
            ('new cases', "@new_confirmed_cases")
        ],
        formatters={'@date_time':'datetime'}
    ))

    mytext = Label(x=20, y=-59, x_units='screen', text=f"Source of data: latimes-state-totals.csv \n "
                                                        f"Date of last update: {max_date}",
    render_mode='css',y_units='screen',
      border_line_color='black', border_line_alpha=1.0,
      background_fill_color='white', background_fill_alpha=1.0,)
    p.add_layout(mytext)
    tab = Panel(child=p, title='New coronavirus cases in California on a particular day in August')
    return tab

def tab2():
    data = pd.read_csv('cdph-race-ethnicity.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    max_date=data['date'].iloc[0]
    data = data[(data['age'] == 'all')]
    percentages = ['confirmed cases', 'general population']
    regions = ['asian', 'black', "cdph-other", 'latino', 'other', 'white']
    x = [(race, percent) for race in regions for percent in percentages]

    def create_dataset(df):
        counts = sum(zip(df['confirmed_cases_percent'], df['population_percent']), ())  # like an hstack
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x),title='Comparison of the persent of cases by race to the general population',
                   y_axis_label='Persentage')
        palette = ["#CAB2D6", "#e84d60"]
        p.vbar(x='x', top='counts', width=0.9, source=source,line_color="white",
               fill_color=factor_cmap('x', palette=palette, factors=percentages, start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        p.xgrid.grid_line_color = None
        mytext = Label(x=20, y=-150, x_units='screen', text=f"Source of data: cdph-race-ethnicity.csv \n "
                                                           f"Date of last update: {max_date}",
                       render_mode='css', y_units='screen',
                       border_line_color='black', border_line_alpha=1.0,
                       background_fill_color='white', background_fill_alpha=1.0, )
        p.add_layout(mytext)
        return p

    def callback(attr, old, new):
        new_src = create_dataset(data[(data['date_time']==date_picker.value)])
        src.data.update(new_src.data)

    # Initial Plot
    src = create_dataset(data[(data['date_time']=='2020-10-01')])
    p = create_plot(src)
    date_picker = DatePicker(title='Click to choose a date (blank means no data)', min_date="2020-05-14", max_date=date.today())
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(controls,p)
    tab = Panel(child=layout, title='Percentage of confirmed cases by race')
    return tab

def tab3():
    data = pd.read_csv('cdph-race-ethnicity.csv')
    data['date_time'] = pd.to_datetime(data['date'])
    max_date=data['date'].iloc[0]
    print(max_date)
    data = data[(data['age'] == 'all')]
    percentages = ['deaths cases', 'general population']
    regions = ['asian', 'black', "cdph-other", 'latino', 'other', 'white']
    x = [(race, percent) for race in regions for percent in percentages]

    def create_dataset(df):
        counts = sum(zip(df['deaths_percent'], df['population_percent']), ())
        source = ColumnDataSource(data=dict(x=x, counts=counts))
        return source

    def create_plot(source):
        p = figure(x_range=FactorRange(*x), title='Comparison of the persent of deaths by race to the general population',
                   y_axis_label='Persentage')
        palette = ["#CAB2D6", "#e84d60"]
        p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
               fill_color=factor_cmap('x', palette=palette, factors=percentages, start=1, end=2))
        p.y_range.start = 0
        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.x_range.range_padding = 0.1
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        p.xgrid.grid_line_color = None
        mytext = Label(x=20,y=-150, x_units='screen', text=f"Source of data: cdph-race-ethnicity.csv \n "
                                                           f"Date of last update: {max_date}",
                       render_mode='css', y_units='screen',
                       border_line_color='black', border_line_alpha=1.0,
                       background_fill_color='white', background_fill_alpha=1.0, )
        p.add_layout(mytext)
        return p

    def callback(attr, old, new):
        new_src = create_dataset(data[(data['date_time']==date_picker.value)])
        src.data.update(new_src.data)

    # Initial Plot
    src = create_dataset(data[(data['date_time']=='2020-10-01')])
    p = create_plot(src)
    date_picker = DatePicker(title='Click to choose a date (blank means no data)', min_date="2020-05-14", max_date=date.today())
    date_picker.on_change('value', callback)
    controls = WidgetBox(date_picker)
    layout = row(controls,p)
    tab = Panel(child=layout, title='Percentage of deaths by race')
    return tab
tab1=tab1()
tab2=tab2()
tab3=tab3()
# Put all the tabs into one application
tabs = Tabs(tabs = [tab1,tab2,tab3])

# Put the tabs in the current document for display
curdoc().add_root(tabs)