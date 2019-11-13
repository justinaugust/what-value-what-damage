#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=False)

import geopandas as gpd
import folium

import os
from flask import Flask, request
from shapely.geometry import mapping
from datafetching import *
from map_it import *
from IPython.display import display, HTML


# In[2]:


html_top = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Map the Pre-Damage Values</title>


</head>

<body id="home">

	<h1>What Zipcodes?</h1>
    <h2>Enter a list of zipcodes to estimate pre-damage statistics for</h2>
    <div width="100%" height="100%" align="center">
            <form method="post">
                <input type="text" name="zip_codes" />
                <br>
                <input type="submit" value="Map It!" />
            </form>
        </div>
        <div width="66%" align="center">
'''
html_bottom = '''
</div>
</body>
</html>
'''


# In[ ]:


from flask import Flask, request
import folium

# create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        html = html_top + html_bottom
        return(html)
    
    elif request.method == 'POST':
        
        zip_codes = request.form.get('zip_codes')
        
        zip_codes = process_zips(zip_codes)  
        map_it = mapit(zip_codes)._repr_html_()
        print(map_it)# turn this to a html
        table_dict = tableit(zip_codes)

        html = html_top + map_it

        for zipcode in zip_codes:
            html += f"<h1>{zipcode}</h1>"
            for i in range(len(table_dict[zipcode])):
                html += table_dict[zipcode][i]

        html += html_bottom 
        
        return(html)

# run app
if __name__ == '__main__':
    app.run(host='0.0.0.0')


# In[ ]:




