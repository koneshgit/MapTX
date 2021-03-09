# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:57:22 2021

@author: mkoneshloo
"""
from os import path
import pandas as pd
import geopandas as gpd
import json
## From Bokeh
from bokeh.io import output_notebook, show, output_file#, hplot
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.models import CustomJS, Div, Button
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row
# Internal
from statBok import bistogram
#from bokeh.charts import Histogram

# Setting parameters ------------------------------------------------
#input params
settingSrc = r"../data/TractSetting.json"
#-------------------------------------------------------------------
def load_settings(settingSrc):
    with open(settingSrc) as f:
        pSet = json.load(f)
        pSet["shapeFields"]=list(pSet["shapeFields"].values())
        pSet["dataFields"]=list(pSet["dataFields"].values())
    return pSet

def load_dataSet(pSet): 
    df = pd.read_csv(pSet["dataFile"])
    if len(pSet["dataFields"])>0:
        df = df[pSet["dataFields"]]
    return df

def load_polygon(pSet): 
    _, file_extension = path.splitext(pSet["shapeFile"])    
    if file_extension.lower() =='geojson':
        gdf = gpd.read_file(open(pSet["shapeFile"]))
    else:
        gdf = gpd.read_file(pSet["shapeFile"])
        
    if len(pSet["shapeFields"])>0:
        gdf = gdf[pSet["shapeFields"]]         

    return gdf 
    
def geo_merge(pSet,df,gdf):
    
    #gdf.info()
    gdf[pSet["dataKey"]]=gdf[pSet["shapeKey"]].astype('int64')
    
    merged = gdf.merge(df, left_on = pSet["dataKey"], right_on = pSet["dataKey"], how = 'left')  
    merged = merged.dropna()

    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)
    # with open("merged.json", "w") as data_file:
    #     json.dump(merged_json, data_file, indent=2)

    return GeoJSONDataSource(geojson = json_data)

def cMapper (pSet):
    #Define a sequential multi-hue color palette.
    # Create control on min and max , merged is requierd for colorMapper Function low = 0, high = 40)
    """
    adding colormapper option
    bokeh.models.mappers.ColorMapper (Python class, in bokeh.models.mappers)
    bokeh.models.mappers.CategoricalColorMapper (Python class, in bokeh.models.mappers)
    bokeh.models.mappers.ContinuousColorMapper (Python class, in bokeh.models.mappers)
    bokeh.models.mappers.EqHistColorMapper (Python class, in bokeh.models.mappers)
    bokeh.models.mappers.LinearColorMapper (Python class, in bokeh.models.mappers)
    bokeh.models.mappers.LogColorMapper (Python class, in bokeh.models.mappers)
    """
    
    palette = brewer[pSet["cMapName"]][8] #[cNumber]
    if pSet["reversedColorMap"]:
        palette = palette[::-1]
    
    return LinearColorMapper(palette = palette)

def add_handle(pSet):
        #Add hover tool
        hover = HoverTool(tooltips = [ ("ID","@"+pSet["dataKey"]),
                              (pSet["dataName2Viz"], "@"+pSet["data2Viz"]),
                              (pSet["tipTitle"],pSet["tipName"])])
        return [hover, 'pan', 'tap', 'wheel_zoom']
    
def fig_gen(pSet, color_mapper, map_handle,geosource):
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal') #, major_label_overrides = tick_labels)
    
    #Create figure object.
    p = figure(title = pSet["figTitle"], plot_height = 600 , plot_width = 950, 
               toolbar_location = 'left',tools = map_handle)
    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    p.patches('xs','ys', source = geosource,fill_color = {'field' : pSet["data2Viz"],'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1, legend_label =  pSet["dataName2Viz"])
    
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    
    return p


    
def main_mapper(settingSrc): 
# Files are accesible
    pSet = load_settings(settingSrc)
    # Fields are in dataframes
    df = load_dataSet(pSet)
    gdf = load_polygon(pSet)
    geosource = geo_merge(pSet,df,gdf)
    color_mapper = cMapper (pSet)
    map_handle = add_handle(pSet)
    patch = fig_gen(pSet, color_mapper, map_handle,geosource)
    hst = bistogram(pSet, df[pSet["data2Viz"]])
    button = Button(label="Button", width=300)
    layout = column(button, row(patch, hst))

    
    save(layout,filename = pSet["htmlOut"],title = pSet["figTitle" ])

if __name__ == "__main__":
   main_mapper(settingSrc)