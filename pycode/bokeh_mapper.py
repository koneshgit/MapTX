# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:57:22 2021

@author: mkoneshloo
"""
from os import path
import pandas as pd
import geopandas as gpd
import json
from win32api import GetSystemMetrics
## From Bokeh
from bokeh.models import GeoJSONDataSource, ColorBar, HoverTool , Paragraph
from bokeh.palettes import brewer
from bokeh.plotting import figure, save
from bokeh.models import  ColumnDataSource,mappers
from bokeh.layouts import layout
from bokeh.io import show
from bokeh.models.glyphs import Scatter
# Internal
import statBok

# Setting parameters ------------------------------------------------
settingSrc = r"../data/rpl.json"
#-------------------------------------------------------------------
def load_settings(settingSrc):
    with open(settingSrc) as f:
        pSet = json.load(f)
        if len(pSet["shapeFields"])>0:
            pSet["shapeFields"]=list(pSet["shapeFields"].values())
    return pSet

def load_dataSet(pSet): 
    df = pd.read_csv(pSet["dataFile"])
    if len(pSet["dataFields"])>0:
        df = df[pSet["dataFields"]]
    index_names = df[ (df[pSet["data2Viz"]].values == -999)].index  
    return df.drop(index_names)

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
    return GeoJSONDataSource(geojson = json_data)

def cMapper (pSet):
    #Define a sequential multi-hue color palette.
    # Create control on min and max , merged is requierd for colorMapper Function low = 0, high = 40)
    palette = brewer[pSet["cMapName"]][8]
    if pSet["reversedColorMap"]:
        palette = palette[::-1]
    
    mpc = pSet["mapper"]
    if mpc=="CategoricalColorMapper":
        return mappers.CategoricalColorMapper(palette = palette)
    elif mpc=="ContinuousColorMapper":
        return mappers.ContinuousColorMapper(palette = palette)
    elif mpc=="EqHistColorMapper":
        return mappers.EqHistColorMapper(palette = palette)
    elif  mpc=="LogColorMapper":
        return mappers.LogColorMapper(palette = palette)
    else:
        return mappers.LinearColorMapper(palette = palette)

def add_handle(pSet):
        #Add hover tool
        hover = HoverTool(tooltips = [ ("ID","@"+pSet["dataKey"]),
                              (pSet["dataName2Viz"], "@"+pSet["data2Viz"]),
                              (pSet["tipTitle"],"@"+pSet["tipName"])])
        return [hover, 'pan', 'tap', 'wheel_zoom', 'lasso_select', 'reset']
    
def add_glyph(fg,x=[],y=[]):
    if len(x)==0:
        x=[-95.2744639]
        y=[29.7825265]
    source = ColumnDataSource(dict(x=x, y=y))
    glyph = Scatter(x="x", y="y", size=10, line_color="#000000",fill_alpha=0.1, line_alpha=0.7)
    fg.add_glyph(glyph,source)
    fg.aspect_scale=1.0
    return fg

def add_scatter(df,pSet):
    scat = figure(width=300, height=300)
    chk =(df[pSet["data2Viz"]].values == -999) |  (df[pSet["tipName"]].values == -999)  
    df = df[~chk]
    scat.scatter(x=df[pSet["data2Viz"]], y=df[pSet["tipName"]] )
    scat.xaxis.axis_label = pSet["dataName2Viz"]
    scat.yaxis.axis_label = pSet["tipTitle"]
    return scat    
 
def add_summary(df, pSet):
    descb ="Summary :\n " + df[pSet["data2Viz"]].describe().to_string()
    return Paragraph(text=descb, width=400, height=300)
       
def map_gen(pSet, color_mapper, map_handle,geosource):
    #Create color bar. 
    try:
        wd=GetSystemMetrics(0)
    except:
        wd=1200
        
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=10,width = 20, height =  int(0.5*wd),
    border_line_color=None,location ='left', orientation = 'vertical') #, major_label_overrides = tick_labels)
    
    #Create figure object.
    p = figure(title = pSet["figTitle"], plot_width = int(0.75*wd), plot_height = int(0.50*wd) , #plot_width = 950, 
               toolbar_location = 'left',tools = map_handle)

    p.patches('xs','ys', source = geosource,fill_color = {'field' : pSet["data2Viz"],'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 0.8, legend_label =  pSet["dataName2Viz"])
    
    sFile = open(r"../data/roads.geojson","rb")
    gdfr = gpd.read_file(sFile)
    datar = json.loads(gdfr.to_json())
    for i in range(len(datar['features'])):
         datar['features'][i]['properties']['Color'] = "#000000"

    road_source = GeoJSONDataSource(geojson=json.dumps(datar))
    p.multi_line('xs','ys', source = road_source, alpha=0.3)

    #Specify figure layout.
    p.add_layout(color_bar, 'left')
  
    return p

    
def main_mapper(settingSrc): 
    pSet = load_settings(settingSrc)
    # Fields are in dataframes
    df = load_dataSet(pSet)
    gdf = load_polygon(pSet)
    geosource = geo_merge(pSet,df,gdf)
    # Visualizing
    color_mapper = cMapper (pSet)
    map_handle = add_handle(pSet)
    patch = map_gen(pSet, color_mapper, map_handle,geosource)
    #patch = add_glyph(path) # Add HFB on Map 
    patch.scatter(y=[29.782526491832318],x=[-95.27446389763395], size=10, color="#000000", alpha=0.6)
    patch.aspect_scale=1.0
    hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
    scat = add_scatter(df,pSet)
    statsummary = add_summary(df, pSet)  

    lout =layout([patch, [hst,scat,statsummary]])
    save(lout,filename = pSet["htmlOut"],title = pSet["figTitle" ])
    show(lout)   
    
if __name__ == "__main__":
    if 1:
        main_mapper(settingSrc)
    else:
        settingSrc = r"../data/test.json"