# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:36:43 2021

@author: mkoneshloo
"""


import geopandas as gpd
from bokeh.io import show, save
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure
import json
outputFile="road.html"
sFile = open(r"../data/roads.geojson","rb")
gdf = gpd.read_file(sFile)
data = json.loads(gdf.to_json())
for i in range(len(data['features'])):
     data['features'][i]['properties']['Color'] = "#000000"

geo_source = GeoJSONDataSource(geojson=json.dumps(data))

TOOLTIPS = [
    ('Road','NAME')
]

p = figure(background_fill_color="lightgrey")
p.multi_line('xs','ys', source = geo_source)

show(p)
save(p,filename = outputFile)