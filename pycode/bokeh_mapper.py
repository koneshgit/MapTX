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
from bokeh.models import GeoJSONDataSource, ColorBar, HoverTool #,LinearColorMapper,
from bokeh.models import CustomJS, Div, Button, Select, GMapOptions
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, save, curdoc, gmap
from bokeh.layouts import column, row
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, Vendors
from bokeh.models import mappers

# range bounds supplied in web mercator coordinates
# p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
#            x_axis_type="mercator", y_axis_type="mercator")


# Internal
#from statBok import bistogram
import statBok
# Setting parameters ------------------------------------------------
#input params
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
    # with open("merged.json", "w") as data_file:
    #     json.dump(merged_json, data_file, indent=2)

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
                              (pSet["tipTitle"],pSet["tipName"])])
        return [hover, 'pan', 'tap', 'wheel_zoom', 'lasso_select', 'reset']
    
def map_gen(pSet, color_mapper, map_handle,geosource):
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal') #, major_label_overrides = tick_labels)
    
    #Create figure object.
    p = figure(title = pSet["figTitle"], #plot_height = 600 , plot_width = 950, 
               # x_range=(-8781403, -6403544), y_range=(11828971, 10874679),
               # x_axis_type="mercator", y_axis_type="mercator",
               #x_range=(-107, -93), y_range=(25, 37),
               toolbar_location = 'left',tools = map_handle)
    #gmap_options = GMapOptions(lat=30.00, lng=-95.5, map_type="roadmap", zoom=8)
    #p = gmap("AIzaSyBuBur_u0ceQNjqYwh4xCJGI95jEax55ok", map_options, )
    # p.xgrid.grid_line_color = None
    # p.ygrid.grid_line_color = None
    # print (tile_provider)
    # p.add_tile(tile_provider)
    p.patches('xs','ys', source = geosource,fill_color = {'field' : pSet["data2Viz"],'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 0.8, legend_label =  pSet["dataName2Viz"])
    
    sFile = open(r"../data/roads.geojson","rb")
    gdfr = gpd.read_file(sFile)
    datar = json.loads(gdfr.to_json())
    for i in range(len(datar['features'])):
         datar['features'][i]['properties']['Color'] = "#000000"

    road_source = GeoJSONDataSource(geojson=json.dumps(datar))
    p.multi_line('xs','ys', source = road_source)

    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    p.aspect_scale=1.0
    
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
    
    patch = map_gen(pSet, color_mapper, map_handle,geosource)
    patch.scatter(y=[29.782526491832318],x=[-95.27446389763395], size=10, color="#000000", alpha=0.6)
    hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
    # button = Button(label="Update", width=300)
    # #label="Factors",
    # dSel = Select(value=pSet["data2Viz"], options=df.columns.to_list())
    # def update_var(attr, old, new):
    #     pSet["data2Viz"] = new
    #     patch = map_gen(pSet, color_mapper, map_handle,geosource)
    #     hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
        
    # dSel.on_change('value', update_var)
    
    # #label="Pallets",
    # cSel = Select(value=pSet["cMapName"], options=["Viridis","Spectral",
    #                                                   "RdYlGn", "Bokeh", "Turbo256"])
    # def update_cbar (attr, old, new) :
    #     pSet["cMapName"] = new
    #     color_mapper = cMapper (pSet)
    #     patch = map_gen(pSet, color_mapper, map_handle,geosource)
    #     #hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
        
    # cSel.on_change('value', update_cbar)
    # layout = column(button, row(patch, hst),row(cSel,dSel))

    layout = row(patch, hst)
    save(layout,filename = pSet["htmlOut"],title = pSet["figTitle" ])
    # curdoc().add_root(layout)
    # curdoc().title = "Map Tool"
    show(layout)
    
    # curdoc().add_root(layout)
    
    #def update(attr, old, new):
        
    #     inds = new
    #     if len(inds) == 0 or len(inds) == len(x):
    #         hhist1, hhist2 = hzeros, hzeros
    #         vhist1, vhist2 = vzeros, vzeros
    #     else:
    #         neg_inds = np.ones_like(x, dtype=np.bool)
    #         neg_inds[inds] = False
    #         hhist1, _ = np.histogram(x[inds], bins=hedges)
    #         vhist1, _ = np.histogram(y[inds], bins=vedges)
    #         hhist2, _ = np.histogram(x[neg_inds], bins=hedges)
    #         vhist2, _ = np.histogram(y[neg_inds], bins=vedges)
    
    #     hh1.data_source.data["top"]   =  hhist1
    #     hh2.data_source.data["top"]   = -hhist2
    #     vh1.data_source.data["right"] =  vhist1
    #     vh2.data_source.data["right"] = -vhist2
    
    #r.patches.selected.on_change('indices', update)
    
    
    
    
    
if __name__ == "__main__":
    if 1:
        main_mapper(settingSrc)
    else:
        settingSrc = r"../data/test.json"