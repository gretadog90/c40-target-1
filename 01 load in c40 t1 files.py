#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 11:21:29 2023

@author: gretam
"""

#%% load modules
import rasterio as rio
from rasterio.plot import show
import xarray as xr
import rioxarray as rxr
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
prj_folder = '/Users/gretam/Documents/'
data_folder = '/Users/gretam/Documents/data/c40 target 1/'
ndvi_path=data_folder+'ndvi/'
ga_path=data_folder+'ga/'
mndvi_path=data_folder+'mndvi/'
gba_path=data_folder+'gba/'

# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(ndvi_path)  if not i.startswith('.')]
print(len(c40_list))

#%% load data and just do some basic checks that info is as we expect and that 
# all the data sets for each city share the same shape, resolution, bounds, etc.ß

# loop through geotiffs to print out some info
for file in c40_list:
    ndvi=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    ga=rxr.open_rasterio(ga_path+file+'.tif',masked=True).squeeze()
    mndvi=rxr.open_rasterio(mndvi_path+file+'.tif',masked=True).squeeze()
    gba=rxr.open_rasterio(gba_path+file+'.tif',masked=True).squeeze()
    print(file)
    print("The crs of your data is:", ndvi.rio.crs)
    print("The nodatavalue of your data is:", ndvi.rio.nodata)
    print("The number of bands for your data is:", ndvi.rio.count)
    print("The shape of your data is:", ndvi.shape)
    print("The spatial resolution for your data is:", ndvi.rio.resolution())
    print(ndvi.rio.bounds())
    #should all be same for ga
    print(ndvi.rio.crs==ga.rio.crs)
    print(ndvi.rio.shape==ga.rio.shape)
    print(ndvi.rio.resolution()==ga.rio.resolution())
    print(ndvi.rio.bounds()==ga.rio.bounds())
    #should all be same for mndvi
    print(ndvi.rio.crs==mndvi.rio.crs)
    print(ndvi.rio.shape==mndvi.rio.shape)
    print(ndvi.rio.resolution()==mndvi.rio.resolution())
    print(ndvi.rio.bounds()==mndvi.rio.bounds())
    #should all be same for gba
    print(ndvi.rio.crs==gba.rio.crs)
    print(ndvi.rio.shape==gba.rio.shape)
    print(ndvi.rio.resolution()==gba.rio.resolution())
    print(ndvi.rio.bounds()==gba.rio.bounds())
    #get name of of variable where data stored
    print("The metadata for your data is:", ndvi.attrs)
    print("The metadata for your data is:", ga.attrs)
    print("The metadata for your data is:", mndvi.attrs)
    print("The metadata for your data is:", gba.attrs)

#%% store info on city and corresponding ndvi, ga, mndvi, and gba in one dictionary 
d = {}
for city in c40_list:
    #load in ndvi and then create df
    ndvi=rxr.open_rasterio(ndvi_path+city+'.tif',masked=True).squeeze()
    ndvi_df=ndvi.to_dataset(name='ndvi')
    #load in ga and then create df
    ga=rxr.open_rasterio(ga_path+city+'.tif',masked=True).squeeze()
    ga_df=ga.to_dataset(name='ga')
    #load in mndvi and then create df
    mndvi=rxr.open_rasterio(mndvi_path+city+'.tif',masked=True).squeeze()
    mndvi_df=ndvi.to_dataset(name='mndvi')
    #load in ga and then create df
    gba=rxr.open_rasterio(gba_path+city+'.tif',masked=True).squeeze()
    gba_df=gba.to_dataset(name='gba')
    merged=xr.combine_by_coords([ndvi_df, ga_df, mndvi_df, gba_df])
    d[city]=merged
        
print(d)

#%% store summary info from this dictionary to an excel file
c40_t1_summary = []
for key, value in d.items():
    #save city name 
    city=key
    #store ndvi summary stats
    ndvi_mean=np.nanmean(value.ndvi)
    ndvi_min=np.nanmean(value.ndvi)
    ndvi_max=np.nanmean(value.ndvi)
    ndvi_std=np.nanmean(value.ndvi)
    ndvi_total=np.count_nonzero(np.isnan(value.ndvi))
    #store ga summary stats
    ga_mean=np.nanmean(value.ga)
    ga_min=np.nanmean(value.ga)
    ga_max=np.nanmean(value.ga)
    ga_std=np.nanmean(value.ga)
    ga_total=np.count_nonzero(np.isnan(value.ga))
    #store mndvi summary stats
    mndvi_mean=np.nanmean(value.mndvi)
    mndvi_min=np.nanmean(value.mndvi)
    mndvi_max=np.nanmean(value.mndvi)
    mndvi_std=np.nanmean(value.mndvi)
    mndvi_total=np.count_nonzero(np.isnan(value.mndvi))
    #store gba summary stats
    gba_mean=np.nanmean(value.gba)
    gba_min=np.nanmean(value.gba)
    gba_max=np.nanmean(value.gba)
    gba_std=np.nanmean(value.gba)
    gba_total=np.count_nonzero(np.isnan(value.gba))
    #append all these variables together in a DF 
    c40_t1_summary.append((city, ndvi_mean, ndvi_std, ndvi_min, ndvi_max, ndvi_total,
                       ga_mean, ga_std, ga_min, ga_max, ga_total,    
                       mndvi_mean, mndvi_std, mndvi_min, mndvi_max, mndvi_total,
                       gba_mean, gba_std, gba_min, gba_max, gba_total)) 
 

#cols=['City','min','max','mean', 'std', 'total pixels']
c40_target1 = pd.DataFrame(c40_t1_summary)
c40_target1.to_csv(prj_folder+'output/c40_target1_summary.csv')

#%% extract Chicago data frame to plot
Chicago=d['Chicago']
print(Chicago)
Chicago.ga_df.plot.hist()
Chicago.ndvi_df.plot.hist()
Chicago.plot.scatter(x='ndvi_df', y='ga_df')

chicago=Chicago.to_dataframe()
print(chicago.isnull().sum())

# there are differing amounts of missingness in ndvi & ga due to different 
#definitions of water (from GSW or from land cover map). will keep where both
#are not missing

#create df with no missingness for GAM
chicago_nomiss = chicago.dropna().reset_index() 

y=chicago_nomiss['ndvi_df']



#%% plot city NDVI using matplotlib
# smod plots
for file in c40_list:
    #open the .tif file
    city=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    
    #create NDVI map of city
    f, ax = plt.subplots()
    city.plot(cmap="Greens", #change color scheme to green
              ax=ax)
    ax.set_title('Normalized Difference Vegetation Index- '+file) 
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    plt.show() # show the plot in the ipython console
    filename=prj_folder+'output/'+file+'.png' 
    f.savefig(filename ,dpi=300)
    plt.clf()
    
    #create historgram of NDVI
    filename_hist=prj_folder+'output/histogram_'+file+'.png'
    city.plot.hist()
    plt.title(file)
    plt.savefig(filename_hist)
    plt.clf()

#buffer plots
for file in c40_list:
    #open the .tif file
    city=rxr.open_rasterio(ndvi_path_buffer+file+'.tif',masked=True).squeeze()
    
    #create NDVI map of city
    f, ax = plt.subplots()
    city.plot(cmap="Greens", #change color scheme to green
              ax=ax)
    ax.set_title('Normalized Difference Vegetation Index- '+file) 
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    plt.show() # show the plot in the ipython console
    filename=prj_folder+'output/'+file+'_buffer.png' 
    f.savefig(filename ,dpi=300)
    plt.clf()
    
    #create historgram of NDVI
    filename_hist=prj_folder+'output/histogram_'+file+'.png'
    city.plot.hist()
    plt.title(file)
    plt.savefig(filename_hist)
    plt.clf()

