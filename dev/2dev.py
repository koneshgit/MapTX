# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 11:28:31 2021

@author: mkoneshloo
-----------------------------------------------------------
#Further developement
## Adding tiled background
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, Vendors

p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
            x_axis_type="mercator", y_axis_type="mercator") #range bounds supplied in web mercator coordinates


# Adding google map
gmap_options = GMapOptions(lat=30.00, lng=-95.5, map_type="roadmap", zoom=8)
p = gmap("AIzaSyBuBur_u0ceQNjqYwh4xCJGI95jEax55ok", map_options, )

# Graph style
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
print (tile_provider)
p.add_tile(tile_provider)

# Interactions and callbacks
button = Button(label="Update", width=300)
    #label="Factors",
dSel = Select(value=pSet["data2Viz"], options=df.columns.to_list())
def update_var(attr, old, new):
    pSet["data2Viz"] = new
    patch = map_gen(pSet, color_mapper, map_handle,geosource)
    hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
    
dSel.on_change('value', update_var)

#label="Pallets",
cSel = Select(value=pSet["cMapName"], options=["Viridis","Spectral",
                                                  "RdYlGn", "Bokeh", "Turbo256"])
def update_cbar (attr, old, new) :
    pSet["cMapName"] = new
    color_mapper = cMapper (pSet)
    patch = map_gen(pSet, color_mapper, map_handle,geosource)
    #hst = statBok.bistogram(pSet, df[pSet["data2Viz"]])
    
cSel.on_change('value', update_cbar)
layout = column(button, row(patch, hst),row(cSel,dSel))

 
curdoc().add_root(layout)

def update(attr, old, new):
    
inds = new
if len(inds) == 0 or len(inds) == len(x):
    hhist1, hhist2 = hzeros, hzeros
    vhist1, vhist2 = vzeros, vzeros
else:
    neg_inds = np.ones_like(x, dtype=np.bool)
    neg_inds[inds] = False
    hhist1, _ = np.histogram(x[inds], bins=hedges)
    vhist1, _ = np.histogram(y[inds], bins=vedges)
    hhist2, _ = np.histogram(x[neg_inds], bins=hedges)
    vhist2, _ = np.histogram(y[neg_inds], bins=vedges)

hh1.data_source.data["top"]   =  hhist1
hh2.data_source.data["top"]   = -hhist2
vh1.data_source.data["right"] =  vhist1
vh2.data_source.data["right"] = -vhist2

r.patches.selected.on_change('indices', update)

    
    
"""


    
