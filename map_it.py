#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np

from uszipcode import SearchEngine

import geopandas as gpd
import folium

import json
#!pip install json2table
from json2table import convert
from IPython.display import display, HTML

import os

from shapely.geometry import mapping
from datafetching import *


# In[24]:


def make_map(geo_json, df):
    
    start_loc = (np.mean(df.loc[:,'lat']), np.mean(df.loc[:,'lng']))
    
    
    m = folium.Map(location=start_loc,
               crs = 'EPSG3857',
               control_scale = True,
               prefer_canvas = True,
                   max_bounds=True,
                   zoom_snap = .5,
                  tiles = 'OpenStreetMap',

                   
              )
    
#     population_bins = list(df['population_density'].quantile([0, 0.25, 0.5, 0.75, 1]))
    population = folium.Choropleth(
    geo_data = geo_json,
    data = df,
    key_on='properties.zip',
    columns=['zip','population_density'],
    fill_color='YlGnBu',
    nan_fill_color = 'white',
    highlight=True,
    name="Population Density (2015)",
    fill_opacity=0.7,
    line_opacity=0.2,
#     legend_name='Pop. Density',
#     bins=population_bins,
    overlay=True,
    ).add_to(m)
    

    population.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['zip','population','population_density','occupied_housing_units'],
            aliases = ['Zip Code',
                       'Population (2015)',
                       'Population Density (2015)',
                       'Occupied Housing Units (2015)'
                      ],
            sticky = False,
            localize = True,
                                      )
    )
        
        
    
#     real_estate_bins = list(df['mean'].quantile([0, 0.25, 0.5, 0.75, 1]))

    real_estate = folium.Choropleth(
        geo_data = geo_json,
        data=df,
        key_on='properties.zip',
        columns=['zip','hv_median'],
        fill_color='YlGn',
        nan_fill_color = 'white',
        highlight=True,
        name="Real Estate Info",
        fill_opacity=0.7,
        line_opacity=0.2,
#         legend_name='Mean Home Price ($USD)',
#         bins=real_estate_bins,
        show=False,
        overlay=True,
        ).add_to(m)

    real_estate.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['zip','hv_median','hv_lowtier','hv_midtier','hv_toptier'],
            aliases = ['Zip Code','Median Home Value','Low Tier Home Value','Mid Tier Home Value','Top Tier Home Value'],
            sticky = False,
            localize=True,
                                      )
    )
    
#     hurricane_bins = list(df['cat_2'].quantile([0, 0.25, 0.5, 0.75, 1]))
    hurricane = folium.Choropleth(
        geo_data = geo_json,
        data=df,
        key_on='properties.zip',
        columns=['zip','hurr_2'],
        fill_color='GnBu',
        nan_fill_color = 'white',
        highlight=True,
        name="Potential Hurricane Damage",
        fill_opacity=0.7,
        line_opacity=0.2,
#         legend_name='Damage Due to Hurricane',
#         bins=hurricane_bins,
        show=False,
        overlay=True,
        ).add_to(m)

    hurricane.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['zip','hurr_1','hurr_2','hurr_3','hurr_4','hurr_5'],
            aliases = ['Zip Code',
                       'Cat. 1 Damage Estimate',
                       'Cat. 2 Damage Estimate',
                       'Cat. 3 Damage Estimate',
                       'Cat. 4 Damage Estimate',
                       'Cat. 5 Damage Estimate',
                       
                      ],
            sticky = False,
            localize=True,
                                      )
    )
    
#     flood_bins = list(df['fl_6'].quantile([0, 0.25, 0.5, 0.75, 1]))
    flood = folium.Choropleth(
        geo_data = geo_json,
        data=df,
        key_on='properties.zip',
        columns=['zip','fl_6'],
        fill_color='GnBu',
        nan_fill_color = 'white',
        highlight=True,
        name="Flood Damage per Inches",
        fill_opacity=0.7,
        line_opacity=0.2,
#         legend_name='Damage Due to Flood',
#         bins=flood_bins,
        show = False,
        overlay=True,
        ).add_to(m)

    flood.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['zip',
             'fl_1','fl_2','fl_3','fl_4',
             'fl_5','fl_6','fl_7','fl_8',
             'fl_9','fl_10','fl_11','fl_12',
             'fl_24','fl_36','fl_48'],
            aliases = ['Zip Code',
                       '1" Flood Damage Estimate',
                       '2" Flood Damage Estimate',
                       '3" Flood Damage Estimate',
                       '4" Flood Damage Estimate',
                       '5" Flood Damage Estimate',
                       '6" Flood Damage Estimate',
                       '7" Flood Damage Estimate',
                       '8" Flood Damage Estimate',
                       '9" Flood Damage Estimate',
                       '10" Flood Damage Estimate',
                       '11" Flood Damage Estimate',
                       '12" Flood Damage Estimate',
                       '24" Flood Damage Estimate',
                       '36" Flood Damage Estimate',
                       '48" Flood Damage Estimate',
                       
                      ],
            sticky = False,
            localize=True,
                                      )
    )
    
    
    
    
#     tornado_bins = list(df['fl_6'].quantile([0, 0.25, 0.5, 0.75, 1]))
    tornado = folium.Choropleth(
        geo_data = geo_json,
        data=df,
        key_on='properties.zip',
        columns=['zip','tor_2_mt'],
        fill_color='GnBu',
        nan_fill_color = 'white',
        highlight=True,
        name="Tornado Damage by Level & Housing Tier",
        fill_opacity=0.7,
        line_opacity=0.2,
#         legend_name='Damage Due to Tornado',
#         bins=tornado_bins,
        show = False,
        overlay=True,
        ).add_to(m)

    tornado.geojson.add_child(
        folium.features.GeoJsonTooltip(
            ['zip',
             'tor_0_lt', 'tor_1_lt', 'tor_2_lt', 'tor_3_lt',
             'tor_4_lt', 'tor_5_lt', 'tor_0_mt', 'tor_1_mt', 
             'tor_2_mt', 'tor_3_mt', 'tor_4_mt', 'tor_5_mt',
             'tor_0_tt', 'tor_1_tt', 'tor_2_tt', 'tor_3_tt', 
             'tor_4_tt', 'tor_5_tt'],
            aliases = ['Zip Code',
                       'Level 0 Low Tier Damage',
                   'Level 1 Low Tier Damage',
                   'Level 2 Low Tier Damage',
                   'Level 3 Low Tier Damage',
                   'Level 4 Low Tier Damage',
                   'Level 5 Low Tier Damage',
                   'Level 0 Mid Tier Damage',
                   'Level 1 Mid Tier Damage',
                   'Level 2 Mid Tier Damage',
                   'Level 3 Mid Tier Damage',
                   'Level 4 Mid Tier Damage',
                   'Level 5 Mid Tier Damage',
                   'Level 0 Top Tier Damage',
                   'Level 1 Top Tier Damage',
                   'Level 2 Top Tier Damage',
                   'Level 3 Top Tier Damage',
                   'Level 4 Top Tier Damage',
                   'Level 5 Top Tier Damage'
                      ],
            sticky = False,
            localize=True,
        )
    )
    
   
    

    
    folium.LayerControl(collapsed=False).add_to(m)
    bounds = [
        (df.loc[:,'lat'].min() - .04, df.loc[:,'lng'].min() -.04),
        (df.loc[:,'lat'].max() + .3, df.loc[:,'lng'].max() +.3)
    ]
    m.fit_bounds(bounds)

    
    for key in m._children:
        if 'choropleth' in key:
            for child in m._children[key]._children:
                if child.startswith('color_map'):
                     del(m._children[key]._children[child])

            

    
    m.save('map.html')
    return(m)


# In[1]:


def make_df(zip_codes, geo):
    from_usazipcode = ['population', 'population_density', 'occupied_housing_units', 'lat', 'lng']
    dfs = []
    for zipcode in zip_codes:
        data_df = pd.read_csv(f'datasets/zips/data/{zipcode}.csv', dtype={'zip':'str'})
        search = SearchEngine(simple_zipcode=False)
        z_dict = search.by_zipcode(zipcode).to_dict()
        for col in from_usazipcode:
            data_df.loc[data_df['zip'] == zipcode, col] = z_dict[col]
        if geo:
            geo_df = gpd.read_file(f'datasets/zips/shapefiles/{zipcode}.geojson', dtype={'zip':'str'})
            dfs.append(pd.merge(left=data_df, right=geo_df, on='zip'))
        else:
            dfs.append(data_df)

    df = pd.concat(dfs)
    if geo:
        df = gpd.GeoDataFrame(df, geometry = 'geometry')
        
    return(df)


# In[34]:


def mapit(zip_codes):
    
    df = make_df(zip_codes, geo=True)
    geo_json = mapping(df)
    
    folium_map = make_map(geo_json=geo_json, df=df)
    return(folium_map)


# In[17]:


def tableit(zip_codes):

    pop = [
        ['population', 'population_density', 'occupied_housing_units'],
        ['Population', 'Population Density', 'Occupied Housing Units']
    ]
    hv = [
        ['hv_median', 'hv_lowtier', 'hv_midtier', 'hv_toptier'],
        ['Median Home Value', 'Median Home Value - High Tier', 'Median Home Value - Mid Tier', 'Median Home Value - Low Tier']
    ]
    hurr = [
        ['hurr_1', 'hurr_2', 'hurr_3', 'hurr_4', 'hurr_5'],
        ['Damage from Category 1 Hurricane',
         'Damage from Category 2 Hurricane',
         'Damage from Category 3 Hurricane',
         'Damage from Category 4 Hurricane',
         'Damage from Category 5 Hurricane' ]
    ]
    fl = [
        ['fl_1', 'fl_2', 'fl_3', 'fl_4', 'fl_5', 'fl_6', 'fl_7',
         'fl_8', 'fl_9', 'fl_10', 'fl_11', 'fl_12', 'fl_24',
         'fl_36', 'fl_48'],
        ['Damage from 1" of in-home Flood Water', 
        'Damage from 2" of in-home Flood Water', 
        'Damage from 3" of in-home Flood Water', 
        'Damage from 4" of in-home Flood Water', 
        'Damage from 5" of in-home Flood Water', 
        'Damage from 6" of in-home Flood Water', 
        'Damage from 7" of in-home Flood Water', 
        'Damage from 8" of in-home Flood Water', 
        'Damage from 9" of in-home Flood Water', 
        'Damage from 10" of in-home Flood Water', 
        'Damage from 11" of in-home Flood Water', 
        'Damage from 12" of in-home Flood Water', 
        'Damage from 24" of in-home Flood Water', 
        'Damage from 36" of in-home Flood Water', 
        'Damage from 48" of in-home Flood Water']
    ]
    tor = [
        ['tor_0_lt', 'tor_1_lt', 'tor_2_lt', 'tor_3_lt',
             'tor_4_lt', 'tor_5_lt', 'tor_0_mt', 'tor_1_mt', 
             'tor_2_mt', 'tor_3_mt', 'tor_4_mt', 'tor_5_mt',
             'tor_0_tt', 'tor_1_tt', 'tor_2_tt', 'tor_3_tt', 
             'tor_4_tt', 'tor_5_tt'],
        ['Category 0 Tornado Damage to Low Tier Houses',
        'Category 1 Tornado Damage to Low Tier Houses',
        'Category 2 Tornado Damage to Low Tier Houses',
        'Category 3 Tornado Damage to Low Tier Houses',
        'Category 4 Tornado Damage to Low Tier Houses',
        'Category 5 Tornado Damage to Low Tier Houses',
        'Category 0 Tornado Damage to Mid Tier Houses',
        'Category 1 Tornado Damage to Mid Tier Houses',
        'Category 2 Tornado Damage to Mid Tier Houses',
        'Category 3 Tornado Damage to Mid Tier Houses',
        'Category 4 Tornado Damage to Mid Tier Houses',
        'Category 5 Tornado Damage to Mid Tier Houses',
        'Category 0 Tornado Damage to Top Tier Houses',
        'Category 1 Tornado Damage to Top Tier Houses',
        'Category 2 Tornado Damage to Top Tier Houses',
        'Category 3 Tornado Damage to Top Tier Houses',
        'Category 4 Tornado Damage to Top Tier Houses',
        'Category 5 Tornado Damage to Top Tier Houses' ]
    ]
    
    to_table = [pop, hv, hurr, fl, tor]
    
    pop_rename = ['Population', 'Population Density', 'Occupied Housing Units']
    
    
    df = make_df(zip_codes, geo=False)
    
    
    html_dict = {}
   
    for zipcode in zip_codes:
        dicts = []
        for table_keys, table_newkeys in to_table:
           
            if [table_keys, table_newkeys] != to_table[0]:
                    new_dict = {table_newkeys[i]: '$' + str(place_value(int(df.loc[df['zip'] == zipcode, key].values[0]))) for i,key in enumerate(table_keys)}

                    dicts.append(new_dict)
            else:
                    new_dict = {table_newkeys[i]: df.loc[df['zip'] == zipcode, key].values[0] for i,key in enumerate(table_keys)}
                    dicts.append(new_dict)
                    
        

        html_list = []
        for d in dicts:
            html = convert(d, build_direction="LEFT_TO_RIGHT" )
            html_list.append(html)
        html_dict[zipcode] = html_list
    return(html_dict)


# In[ ]:




