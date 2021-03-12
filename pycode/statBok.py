# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:29:06 2021

@author: mkoneshloo
"""
import numpy as np
from bokeh.plotting import figure

def bistogram (pSet, dataV):
    p = figure(title=pSet["dataName2Viz"], tools='', background_fill_color="#fafafa", width=400, height=300)
    hist, edges = np.histogram(dataV, density=True, bins=50)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)
    return p