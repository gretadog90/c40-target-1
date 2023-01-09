#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:30:30 2022

@author: gretam
"""
        
#%% load modules
import os

#%% 
# data root folder path
data_folder = '/Users/gretam/Documents/data/'

### TARGET 1
#set up file pathway and dictionary with folder name and expected file suffix
c40t1_path = data_folder+'c40 target 1/'
c40t1_dict={'ga/': 'ga100.tif','gba/': 'gba100.tif','ndvi/': 'ndvi100.tif', 
            'mndvi/':'mNDVI100.tif'}

#if the correct file is in the correct folder, remove its suffix so that it's just Boston.tif for example
for key, value in c40t1_dict.items():
    
    # enumerate all the files in the directory
    files = os.listdir(c40t1_path+key)
    
    for f in files:
        if f.split('_')[1]==value:
            newname = f.split('_')[0]
            newname = newname+'.tif'
            print(newname) 
            os.rename(os.path.join(c40t1_path+key,f), os.path.join(c40t1_path+key,newname))
        else:
            break

### TARGET 2
#set up file pathway and dictionary with folder name and expected file suffix
c40t2_path = data_folder+'c40 target 2/'
c40t2_dict={'ga/': 'gat2.tif','gba/': 'bgat2.tif','ndvi/': 'ndvi10p.tif', 
            'mndvi/':'ns10p.tif', 'population/':'adultPop.tif'}

#if the correct file is in the correct folder, remove its suffix so that it's just Boston.tif for example
for key, value in c40t2_dict.items():
    
    # enumerate all the files in the directory
    files = os.listdir(c40t2_path+key)

    for f in files:
        if f.split('_')[1]==value:
            newname = f.split('_')[0]
            newname = newname+'.tif'
            print(newname) 
            os.rename(os.path.join(c40t2_path+key,f), os.path.join(c40t2_path+key,newname))
        else:
            break