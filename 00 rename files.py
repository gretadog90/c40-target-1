#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:30:30 2022

@author: gretam
"""


#%% load modules
import os

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/c40 target1/'

dir_list=['ga100/', 'ndvi100/']

for dirs in dir_list:
    # file path for easier referencing 
    files = os.listdir(data_folder+dirs)

    for f in files:
        newname = f.split('_')[0]
        newname = newname+'.tif'
        print(newname) 
        os.rename(os.path.join(data_folder+dirs,f), os.path.join(data_folder+dirs,newname))
  