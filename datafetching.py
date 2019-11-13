#!/usr/bin/env python
# coding: utf-8

# #!pip install zipcodes
# #!pip install xmltodict
# #!pip install geopandas
# #!pip install uszipcode

# In[4]:


import pandas as pd
import numpy as np
import geopandas as gpd

import requests
import json
import time
from time import sleep
import os
from pathlib import Path
from urllib.request import urlopen
import sqlalchemy as sal
import copy

from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=False)


# ## Fetching Functions:
# 
# - `get_addresses` looks up addresses from the [OpenAddresses.io](https://openaddresses.io) database based on the zip code someone wants to check
# - `fetch_data_zillow` takes those addresses and gets the XML for each address it can find data for
# - `get_zests` filters that data for the `zestimate` for each address
# - `make_df` takes those values and calculates min(), mean(), max(), etc and creates a PANDAS DataFranme
# - `df_to_csv` updates our existing database with new values, drops the old values if the zip code is repeated and rewrites the csv, outputting the new database as `df`, a PANDAS dataframe

# In[5]:


def place_value(number): 
    return ("{:,}".format(number)) 


# In[6]:


def wkb_hexer(line):
    return line.wkb_hex
    # https://stackoverflow.com/a/38363154


# In[7]:


def indic_loop(indics):
    for indic in indics:
        q_code = 'Z' + zipcode + '_' + indic
        ftype = '.json'
        params = {
                'api_key' : api_key,
            }
        get_url = base_url+q_code+ftype
        res = requests.get(get_url,params)
        zip_code_data[indic] = res.json()


# In[8]:


def get_quandl(zipcode):
    indics = ['ZHVIAH', 'ZHVIBT', 'ZHVIMT', 'ZHVITT', "MVALFAH"]
    base_url = 'https://www.quandl.com/api/v3/datasets/ZILLOW/'
    api_key = 'DFQTn_jyXtRoxLZra1wY'
    zip_code_data = {}
    for indic in indics:
        q_code = 'Z' + zipcode + '_' + indic
        ftype = '.json'
        params = {
                'api_key' : api_key,
            }
        get_url = base_url+q_code+ftype
        res = requests.get(get_url,params)
        zip_code_data[indic] = res.json()
#         for key in zip_code_data[indic].keys():
#             if key == 'quandl_error':
#                 if zip_code_data[indic]['quandl_error'] == 'QELx02':
#                     print()
#             zip_code_data[indic] = res.json()
        
    return(zip_code_data)


# In[9]:


def hurricane_damage(zipcode, disaster_level):
    try: 
        level = {
            1: 119, 2: 154, 3: 178, 4:209, 5: 252
        }

    except:
        pass
    search = SearchEngine(simple_zipcode=False)
    z_dict = search.by_zipcode(zipcode)
    if z_dict.zipcode_type == 'PO Box':
        population = 0
    else:
        population = z_dict.population
    
    damage = -976532 + 2.22*(level[disaster_level])**3 + 9.81e-10*(population)**3
    damage = np.round(damage,2)
    return(damage)   


# In[10]:


def flood_loss(zip_code, water_inches, avg_sq_ft):
    
    # getting number of houses in zipcode. setting to n_houses
    search = SearchEngine(simple_zipcode=False)
    z_dict = search.by_zipcode(zip_code)
    if z_dict.zipcode_type == 'PO Box':
        n_houses = 0
    else:
        n_houses = z_dict.housing_units
    
    water_inches = round(water_inches)
    
    inches = [13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47]
    
    if water_inches in inches:
        print(f'Not data for flood of {water_inches} inches')
        return
    elif water_inches > 48:
        print("No data for flood over 48 inches")
        return

    
    if avg_sq_ft < 1000:
    
        small_home = {1: 9550, 2: 9620, 3: 9820, 4: 12730, 5: 12780,
                      6: 15300, 7: 15508, 8: 15717, 9: 15925, 10: 16133,
                      11: 16342, 12: 16550, 24: 19500, 36: 21100, 48: 23400} 
        damage = small_home[water_inches] * n_houses
    
    
    elif avg_sq_ft >= 1000 and avg_sq_ft < 5000:
    
        average_home = {1: 23635, 2: 23720, 3: 24370, 4: 31345, 5: 31425, 
                        6: 37260, 7: 37691, 8: 38122, 9:38553, 10: 38983,
                        11: 39414, 12: 39845, 24: 44325, 36: 47905, 48: 53355}
        damage = average_home[water_inches] * n_houses
    
    
    elif avg_sq_ft > 5000:
    
        large_home = {1: 47110, 2: 47220, 3: 48620, 4: 62370, 5: 62500, 6: 73860,
                      7: 74662 , 8: 75463, 9: 76265, 10: 77067, 11: 77868, 12: 78670,
                      24: 85700, 36: 92580, 48: 103280}
        damage = large_home[water_inches] * n_houses
        
    else:
        
        print("Square footage not found")
   
    
#     print(f'{zip_code} occured ${place_value(damage)} in damage from {water_inches} inches of flooding inside homes.')
    return(damage)


# In[11]:


# An average tornado covers 1.081 square miles
# Percentage in values of dictionary are percentage of home value lost
# category of tornados: 0,1,2,3,4,5
# function = amount of damage in dollars * number of houses * percent of area hit by tornado

def tornado_damage(zipcode, category, low_zest, mid_zest, top_zest):
    search = SearchEngine(simple_zipcode=False)
    z_dict = search.by_zipcode(zipcode)
    if z_dict.zipcode_type == 'PO Box':
        sq_miles = 0
        n_houses = 0

        percent_hit = 0
    else:
        
        sq_miles = z_dict.land_area_in_sqmi
        n_houses = z_dict.housing_units

        percent_hit = 1.081/sq_miles
    
#     low_zest = define low_zest here
#     mid_zest = define mid_zest here
#     top_zest = define top_zest here
    
    if category == 0:
        
        houses = {'low_zest': low_zest*.002,
                 'mid_zest': mid_zest*.002,
                 'top_zest': top_zest*.002}
    
    elif category == 1:
        
        houses = {'low_zest': low_zest*.008,
                 'mid_zest': mid_zest*.008,
                 'top_zest': top_zest*.008}
        
    elif category == 2:
        
        houses = {'low_zest': low_zest*.016,
                 'mid_zest': mid_zest*.016,
                 'top_zest': top_zest*.016}
        
    elif category == 3:
    
        houses = {'low_zest': low_zest*.3,
                 'mid_zest': mid_zest*.3,
                 'top_zest': top_zest*.3}
    
    elif category == 4:
        
        houses = {'low_zest': low_zest*.70,
                 'mid_zest': mid_zest*.70,
                 'top_zest': top_zest*.70}
        
    elif category == 5:
    
        houses = {'low_zest': low_zest*1,
                 'mid_zest': mid_zest*1,
                 'top_zest': top_zest*1}
    
    else:
        
        print("Acceptable tornado categories: 0, 1, 2, 3, 4, 5.")
    
    
    # damage function for each house tier
    damage_low_tier = houses['low_zest']*n_houses*percent_hit
    damage_mid_tier = houses['mid_zest']*n_houses*percent_hit
    damage_top_tier = houses["top_zest"]*n_houses*percent_hit
    
    
#     print(place_value(damage_low_tier))
#     print(place_value(damage_mid_tier))
#     print(place_value(damage_top_tier))
    return(damage_low_tier, damage_mid_tier, damage_top_tier)


# In[12]:


def get_dict(zipcode):
    
    quandl = get_quandl(zipcode)
    search = SearchEngine(simple_zipcode=False)
    zdict = search.by_zipcode(zipcode).to_dict()
    for key in quandl['ZHVIAH'].keys():
        if key == 'quandl_error':
            zest = zdict['median_home_value']
            if type(zest) != float:
                zest = 0
            pp_sqft = 100
            low_zest = zest * .33
            mid_zest = zest *.51
            top_zest = zest * 1.66
            
        else:
            zest, low_zest, mid_zest, top_zest, pp_sqft = [quandl[key]['dataset']['data'][0][1] for key in quandl.keys()]

        
        
    avg_sqft = zest / pp_sqft
    hurr_1, hurr_2, hurr_3, hurr_4, hurr_5 = [hurricane_damage(zipcode, disaster_level=cat) for cat in range(1,6)]
    flood_inches = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48)
    cats = range(0,6)
    tor_0, tor_1, tor_2, tor_3, tor_4, tor_5 = [tornado_damage(zipcode, cat, low_zest, mid_zest, top_zest) for cat in cats]
    
    
    
    zip_dict = {'zip' : zipcode,
                   'hv_median' : zest,
                   'hv_lowtier' : low_zest,
                   'hv_midtier' : mid_zest,
                   'hv_toptier' : top_zest,
                   'hurr_1' : hurr_1,
                   'hurr_2' : hurr_2,
                   'hurr_3' : hurr_3,
                   'hurr_4' : hurr_4,
                   'hurr_5' : hurr_5,
                   'fl_1' : flood_loss(zipcode, 1, avg_sqft),
                   'fl_2' : flood_loss(zipcode, 2, avg_sqft),
                   'fl_3' : flood_loss(zipcode, 3, avg_sqft),
                   'fl_4' : flood_loss(zipcode, 4, avg_sqft),
                   'fl_5' : flood_loss(zipcode, 5, avg_sqft),
                   'fl_6' : flood_loss(zipcode, 6, avg_sqft),
                   'fl_7' : flood_loss(zipcode, 7, avg_sqft),
                   'fl_8' : flood_loss(zipcode, 8, avg_sqft),
                   'fl_9' : flood_loss(zipcode, 9, avg_sqft),
                   'fl_10' : flood_loss(zipcode, 10, avg_sqft),
                   'fl_11' : flood_loss(zipcode, 11, avg_sqft),
                   'fl_12' : flood_loss(zipcode, 12, avg_sqft),
                   'fl_24' : flood_loss(zipcode, 24, avg_sqft),
                   'fl_36' : flood_loss(zipcode, 36, avg_sqft),
                   'fl_48' :  flood_loss(zipcode, 48, avg_sqft),
                   'tor_0_lt' : tor_0[0],
                   'tor_1_lt' : tor_1[0],
                   'tor_2_lt' : tor_2[0],
                   'tor_3_lt' : tor_3[0],
                   'tor_4_lt' : tor_4[0],
                   'tor_5_lt' : tor_5[0],
                   'tor_0_mt' : tor_0[1],
                   'tor_1_mt' : tor_1[1],
                   'tor_2_mt' : tor_2[1],
                   'tor_3_mt' : tor_3[1],
                   'tor_4_mt' : tor_4[1],
                   'tor_5_mt' : tor_5[1],
                   'tor_0_tt' : tor_0[2],
                   'tor_1_tt' : tor_1[2],
                   'tor_2_tt' : tor_2[2],
                   'tor_3_tt' : tor_3[2],
                   'tor_4_tt' : tor_4[2],
                   'tor_5_tt' : tor_5[2],
                'last_updated' : time.time()
               }
    print(f'Gathered stats for {zipcode}.')
    return(zip_dict)


# In[13]:


def zip_to_csv(zipcode):
    try:
        stat = os.stat(f'datasets/zips/data/{zipcode}.csv')
        if time.time() - stat.st_mtime >= 6: #04800:
            update = True
    except:
        update = True
    
    if update == True:
            import csv
            dict_for_df = get_dict(zipcode)
            with open(f'datasets/zips/data/{zipcode}.csv', 'w') as f:
                w = csv.DictWriter(f, dict_for_df.keys())
                w.writeheader()
                w.writerow(dict_for_df)
                print(f'CSV data written for {zipcode}.')
    else:
        print(f"CSV for {zipcode} up to date.")


# In[14]:


def zip_to_sql(zipcode):
    drop = False
    update = True
    exists = False
    sql_complete = False
    host = "localhost"
    dbname = "zip_codes"
    user = "justinaugust"
    port =  5432
    table_name = 'data'
    
    engine = sal.create_engine(f'postgresql://{user}@{host}:{port}/{dbname}')


    with engine.connect() as conn, conn.begin():
        check_exist = f"""select last_updated from data where zip = {zipcode};"""
        last_updated = conn.execute(check_exist)
        time_diff = -1
        for row in last_updated:
            last_updated = row[0]
        if (type(last_updated) == float):
            time_diff = last_updated - time.time()

        
            if (time_diff > 604800):
                del_cmd = sal.sql.text(f"""DELETE FROM data WHERE "zip" = {zipcode}""")
                del_ = conn.execute(del_cmd)
                if conn.execute("commit"):
                    print(f'Deleted outdated data')
            else:
                update = False

        if update == True:
            dict_for_sql = get_dict(zipcode)
            keys = '"' + '", "'.join([key for key in dict_for_sql.keys()]) + '"'
            vals = ', '.join([str(val) for val in dict_for_sql.values()])
            insert_command = sal.sql.text(f"""INSERT INTO data({keys}) VALUES({vals});""")
            commit = conn.execute(insert_command)
            if conn.execute("commit"):
                print(f'SQL updated for {zipcode}.')
        else:
            print(f'SQL doesn\'t need to be updated for {zipcode}.')
        conn.close()


# In[15]:


## based on code from https://stackoverflow.com/a/3964691

def get_fetched():    
    return([file.strip('.csv') for file in os.listdir("datasets/zips/data")])

def check_zips(zip_codes):
    fetched = get_fetched()
    
    in_db = [zipcode for zipcode in zip_codes if zipcode in fetched]
    not_in_db = [zipcode for zipcode in zip_codes if zipcode not in fetched]
    
    return(not_in_db, in_db)

def have_geojson():
    return([file.strip('.geojson') for file in os.listdir("datasets/zips/shapefiles") if file.endswith('.geojson')])


# In[16]:


def update_zip(zipcode):
    zip_to_csv(zipcode)
#     zip_to_sql(zipcode)


# In[2]:


def process_zips(zip_codes):
    if (type(zip_codes) == str):
            zip_codes = [zip_code.strip() for zip_code in zip_codes.split(",")]
    zip_codes = [str(zipcode) for zipcode in zip_codes]
    zip_codes = list(set(zip_codes))
    
    search = SearchEngine(simple_zipcode=False)
    
    have_shapes = have_geojson()
    zip_codes = [zipcode for zipcode in zip_codes if zipcode in have_shapes]
    zip_codes = [zipcode for zipcode in zip_codes if search.by_zipcode(zipcode).to_dict()['zipcode_type'] != 'PO Box']
    not_fetched, fetched = check_zips(zip_codes)
    
    

    for zipcode in not_fetched:
        fetched = []
        attempted = []
        try:
            update_zip(zipcode)
            print(f'Fetched {zipcode}')
            fetched.append(zipcode) 
            attempted.append(zipcode)
        except:
            print(f'could not fetch for {zipcode}')
            attempted.append(zipcode)
          
        if (len(attempted) % 10000 == 0):
            print('You\'ll have to wait one day to get more information.')
#             for i in range(86400):
#                 sleep(1)
#                 if i % 1000 == 0:
#                     print(f'only {(86400 - i)/60} more minutes to wait... ', end='')
    
    print(' Done!')
    not_fetched, zip_codes = check_zips(zip_codes)
    return(zip_codes)


# In[20]:


host = "localhost"
dbname = "zip_codes"
user = "justinaugust"
port =  5432
table_name = 'shapes'
have_shapes = have_geojson()

engine = sal.create_engine(f'postgresql://{user}@{host}:{port}/{dbname}')
# filling the empty table with data!
def shapes_to_sql():
    for zipc in have_shapes:
    #     try:
        df = gpd.read_file(f"datasets/zips/shapefiles/{zipc}.geojson")
        df['geometry'] = df['geometry'].map(wkb_hexer)
        with engine.connect() as conn, conn.begin():
            df.to_sql(table_name,
                     con = conn,
                     if_exists = 'append',
                     index = False)
    #     except:
    #         print(f'{zipc} not in SQL')


# In[21]:


# with engine.connect() as conn, conn.begin():
#     # Convert the `'geom'` column back to Geometry datatype, from text
#     sql = sal.sql.text("""ALTER TABLE schema_name.shapes
#                ALTER COLUMN geometry TYPE Geometry(LINESTRING, <SRID>)
#                  USING ST_SetSRID(geometry::Geometry, <SRID>)""")
#     run_sql = conn.execute(sql)
#     conn.execute("commit")
        


# In[ ]:




