# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 10:29:08 2021

@author: mkoneshloo
"""

import folium
import pandas as pd
import geopandas as gpd

def read_data(dataSrc, sheetName):
    return pd.read_excel(open(dataSrc, 'rb'), sheetName)
    
    
    
def read_polyg():
     df = geopandas.read_file(zipFile)
    

def generate_baseMap(center =[29.5,-96.5], init_zoom=3):
    mapl = folium.Figure()
    map = folium.Map(location=center, default_zoom_start=init_zoom)
    map.add_to(mapl)
    return mapl


def add_toolTips(agencyes):
    
    return None
    
    
def add_Choropleth ():
     return None
   
    
def mapperMain():
    df =  read_data(dataSrc, sheetName)
    map_base =generate_baseMap()
    sf = shapefile.Reader("shapefiles/blockgroups.shp")
    return None

    
    

#generate_baseMap()

import geopandas as gpd

zipDf =  gpd.read_file(r"C:\Users\mkoneshloo\Desktop\v107\0000USA Zip Code Boundaries.lyr")

gdf = gpd.read_file(r"C:\Users\mkoneshloo\Desktop\zip2020")
#gdf.to_file('myshpfile.geojson', driver='GeoJSON')
gdf.crs = {'init' :'epsg:4326'}
folium.Choropleth(geo_data=gdf,
                line_opacity=0.2).add_to(mapl)