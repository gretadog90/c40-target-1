#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:34:08 2022

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
from scipy import stats
from pygam import LinearGAM, s, f

#%% user inputs - #%% is how you section off code blocks in spyder
# data root folder path
data_folder = '/Users/gretam/Documents/data/c40 target1/'
prj_folder = '/Users/gretam/Documents/'

# file path for easier referencing 
ndvi_path=data_folder+'ndvi100/'
ga_path=data_folder+'ga100/'

# globals
globals()['c40_list']= [os.path.splitext(i)[0] for i in os.listdir(ndvi_path)  if not i.startswith('.')]
print(len(c40_list))

#%% load data

# loop through geotiffs to print out some info
for file in c40_list:
    ndvi=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    ga=rxr.open_rasterio(ga_path+file+'.tif',masked=True).squeeze()
    print("The crs of your data is:", ndvi.rio.crs)
    print("The nodatavalue of your data is:", ndvi.rio.nodata)
    print("The number of bands for your data is:", ndvi.rio.count)
    print("The shape of your data is:", ndvi.shape)
    print("The spatial resolution for your data is:", ndvi.rio.resolution())
    print(ndvi.rio.bounds())
    print(ndvi.rio.crs==ga.rio.crs)
    print(ndvi.rio.count==ga.rio.count)
    print(ndvi.rio.shape==ga.rio.shape)
    print(ndvi.rio.resolution()==ga.rio.resolution())
    print(ndvi.rio.bounds()==ga.rio.bounds())
    print("The metadata for your data is:", ndvi.attrs)
    print("The metadata for your data is:", ga.attrs)


#%% merge ndvi and ga together
d = {}
for city in c40_list:
    ndvi=rxr.open_rasterio(ndvi_path+city+'.tif',masked=True).squeeze()
    ndvi_df=ndvi.to_dataset(name='ndvi_df')
    ga=rxr.open_rasterio(ga_path+city+'.tif',masked=True).squeeze()
    ga_df=ga.to_dataset(name='ga_df')
    merged=xr.combine_by_coords([ndvi_df, ga_df])
    d[city]=merged
        
print(d)

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

x=chicago_nomiss['ndvi_df']
y=chicago_nomiss['ga_df']

gam = LinearGAM((x, y))
print(gam)
gam.plot
gam = LinearGAM(s(0) + s(1) + f(2)).fit(x, y)


#%% reg for ndvi v. %ga


print(x)
slope, intercept, r, p, std_err = stats.linregress(x, y)


def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()



ns_1 = dict()

    #loop through the c40 cities
    for file in us_cities:
        #open the water and ndvi files
        city=rxr.open_rasterio(version+file+'.tif',masked=True).squeeze()
        ns1 = city.stack(stacked=[...])
        ns1 = ns1.values
        ns_1[file] =ns1     

    ns_1 = pd.DataFrame(ns_1.items(), columns = ['City', 'ns_1'])

    ns_1 = ns_1.explode('ns_1')
    ns_1['ns_1'] = ns_1['ns_1'].astype('float')





#%% try to extract one of the city data frame to run regression on
city_summary = []
for file in c40_list:
    city=rxr.open_rasterio(ndvi_path+file+'.tif',masked=True).squeeze()
    print(city)
    city_name=file
    min=np.nanmin(city.data)
    max=np.nanmax(city.data)
    mean=np.nanmean(city.data)
    std=np.nanstd(city.data)
    total=np.size(city.data)
    city_summary.append((city_name, 
                 min, 
                 max, 
                 mean,
                 std,
                 total))


cols=['City','min','max','mean', 'std', 'total pixels']
ndvi_summary = pd.DataFrame(city_summary, columns=cols)

#buffer file summary
city_summary_buffer = []
for file in c40_list:
    city=rxr.open_rasterio(ndvi_path_buffer+file+'.tif',masked=True).squeeze()
    print(city)
    city_name=file
    min=np.nanmin(city.data)
    max=np.nanmax(city.data)
    mean=np.nanmean(city.data)
    std=np.nanstd(city.data)
    total=np.size(city.data)
    city_summary_buffer.append((city_name, 
                 min, 
                 max, 
                 mean,
                 std,
                 total))
    
cols=['City','min','max','mean', 'std', 'total pixels']
ndvi_summary_buffer = pd.DataFrame(city_summary_buffer, columns=cols)

#merge the two together for a ndvi summary file
ndvi_summary_merged=pd.merge(left=ndvi_summary, right=ndvi_summary_buffer, how='left', on='City', validate="1:1")
ndvi_summary_merged.to_csv(prj_folder+'output/city_ndvi_summary.csv')
 
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

