# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 14:57:22 2021

@author: mkoneshloo
"""
from os.path import  splitext
import pandas as pd
import geopandas as gpd
import json
from bokeh.io import output_notebook, show, output_file
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, save


# Setting parameters ------------------------------------------------
#input params
shapeFile = r'C:\MoK\Projects\HFB\maptool\data\C2020_TX_County_Sub.geojson'
shapeUrl =''
dataFile = r'C:\MoK\Projects\HFB\maptool\data\County_Sub.csv'
shapeFields =['OBJECTID','COUSUBNS','GEOID','NAMELSAD', 'geometry']
shapeKey ='OBJECTID'
dataFields =['OBJECTID', 'ALAND','AWATER','INTPTLAT','INTPTLON'] #OBJECTID,COUSUBNS,GEOID,NAMELSAD,CLASSFP,ALAND,AWATER,INTPTLAT,INTPTLON
dataKey ='OBJECTID'
data2Viz= 'INTPTLAT'
dataName2Vize='Latitude of the center of subdivision'

#Output params
cMapName = 'YlGnBu'
cNumber = 32
reversedColorMap = 0
figTitle = ' Visualization map'

# Check input   -------------------------------------------------------
# Files are accesible


# Fields are in dataframes
_, file_extension = splitext(shapeFile)

if file_extension.lower() =='geojson':
    gdf = gpd.read_file(open(shapeFile))
else:
    gdf = gpd.read_file(shapeFile)

gdf=gdf[shapeFields]    
#gdf.info()


df = pd.read_csv(dataFile)
df = df[dataFields]
#df.head()


# Keys are in dataframes


#--------------------------------------------------------------------
#Perform left merge to preserve every row in gdf.
merged = gdf.merge(df, left_on = shapeKey, right_on = dataKey, how = 'left')

#Replace NaN values to string 'No data'.
#merged.fillna('No data', inplace = True)



#Read data to json
merged_json = json.loads(merged.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)


#Input GeoJSON source that contains features for plotting.
geosource = GeoJSONDataSource(geojson = json_data)

#Define a sequential multi-hue color palette.
palette = brewer[cMapName][8] #[cNumber]

#Reverse color order so that dark blue is highest obesity.
if reversedColorMap:
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
hover = HoverTool(tooltips = [ ("Name","@NAMELSAD"),
                              ("Latitude", "@INTPTLAT"),
                              ("Location", "($x, $y)")])

#Create color bar. 
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
border_line_color=None,location = (0,0), orientation = 'horizontal') #, major_label_overrides = tick_labels)

#Create figure object.
p = figure(title = figTitle, plot_height = 600 , plot_width = 950, 
           toolbar_location = 'left',tools=[hover])
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

#Add patch renderer to figure. 
p.patches('xs','ys', source = geosource,fill_color = {'field' :data2Viz, 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

#Specify figure layout.
p.add_layout(color_bar, 'below')
output_file(filename=r"C:\MoK\Projects\HFB\maptool\data\Tx_Subd.html", title="Static HTML file")
save(p)



              
""",
("Name","@NAMELSAD"),
("Latitude", "@INTPTLAT")], mode='vline'
              )
"""