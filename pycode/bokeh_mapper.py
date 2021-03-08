# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:57:22 2021

@author: mkoneshloo
"""
from os import path
import pandas as pd
import geopandas as gpd
import json
from bokeh.io import output_notebook, show, output_file#, hplot
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, save
#from bokeh.charts import Histogram

# Setting parameters ------------------------------------------------
#input params
settingSrc = r"../data/setting.json"
def load_settings(settingSrc):
    with open(settingSrc) as f:
        pSet = json.load(f)
        pSet["shapeFields"]=list(pSet["shapeFields"].values())
        pSet["dataFields"]=list(pSet["dataFields"].values())

    return pSet
    
#Output params
# cMapName = 'YlGnBu'
# cNumber = 32
# reversedColorMap = 0
# figTitle = ' Visualization map'

# Check input   -------------------------------------------------------

# Files are accesible
pSet = load_settings(settingSrc)

# Fields are in dataframes
_, file_extension = path.splitext(pSet["shapeFile"])

if file_extension.lower() =='geojson':
    gdf = gpd.read_file(open(pSet["shapeFile"]))
else:
    gdf = gpd.read_file(pSet["shapeFile"])

gdf=gdf[pSet["shapeFields"]]
if len(pSet["shapeFields"])>0:
    gdf = gdf[pSet["shapeFields"]] 

#gdf.info()


df = pd.read_csv(pSet["dataFile"])
if len(pSet["dataFields"])>0:
    df = df[pSet["dataFields"]]
#df.head()


# Keys are in dataframes


#--------------------------------------------------------------------
#Perform left merge to preserve every row in gdf.
merged = df.merge(gdf, left_on = pSet["dataKey"], right_on = pSet["shapeKey"], how = 'left')

#Replace NaN values
#merged.fillna('No data', inplace = True)

#Read data to json
merged_json = json.loads(merged.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)
# with open("merged.json", "w") as data_file:
#     json.dump(merged_json, data_file, indent=2)

#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer[pSet["cMapName"]][8] #[cNumber]

#Reverse color order so that dark blue is highest obesity.
if pSet["reversedColorMap"]:
    palette = palette[::-1]

#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette)#, low = 0, high = 40)

"""
adding colormapper option
bokeh.models.mappers.ColorMapper (Python class, in bokeh.models.mappers)
bokeh.models.mappers.CategoricalColorMapper (Python class, in bokeh.models.mappers)
bokeh.models.mappers.ContinuousColorMapper (Python class, in bokeh.models.mappers)
bokeh.models.mappers.EqHistColorMapper (Python class, in bokeh.models.mappers)
bokeh.models.mappers.LinearColorMapper (Python class, in bokeh.models.mappers)
bokeh.models.mappers.LogColorMapper (Python class, in bokeh.models.mappers)
"""



#Add later custom tick labels for color bar.
#tick_labels = {'0': '0%', '5': '5%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40': '>40%'}

#Add hover tool
hover = HoverTool(tooltips = [ ("Tracts","@GEOID"),
                              ("Population", "@e_totpop"),
                              ("Zip Codes", "@zip")])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal') #, major_label_overrides = tick_labels)

#Create figure object.
p = figure(title = pSet["figTitle"], plot_height = 600 , plot_width = 950, 
           toolbar_location = 'left',tools=[hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :pSet["data2Viz"],'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

#Specify figure layout.
p.add_layout(color_bar, 'below')

#Legend
p.legend.location = "top_left"
p.legend.click_policy="hide"

#hist = Histogram(df[pSet['data2Viz']], title=pSet['data2Viz'])


output_file(filename=pSet["htmlOut"], title="Static HTML file")
#save(hplot(p, hist))
save(p,filename = pSet["htmlOut"])



              
""",
("Name","@NAMELSAD"),
("Latitude", "@INTPTLAT")], mode='vline'
              )
"""