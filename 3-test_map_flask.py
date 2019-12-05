import pandas as pd
import numpy as np


from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=False)

import geopandas as gpd
import folium

import os
from flask import Flask, request, render_template
from shapely.geometry import mapping
from datafetching import *
from map_it import *
from IPython.display import display, HTML

# create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # show html form
        return render_template('home2.html')
    
    elif request.method == 'POST':
        
        zip_codes = request.form.get('zip_codes')
        
        zip_codes = process_zips(zip_codes)  
        
        map_it = mapit(zip_codes)._repr_html_() # turn this to a html
        table_dict = tableit(zip_codes)

        html = ""
        css = ""
        id = ['pop', 'home', 'hur', 'flood', 'tor']
        colors = ['red', 'green', 'blue', 'red', 'green']
        ziptabs = ""
        for zipcode in zip_codes:
            ziptabs += f"""<button class="tablink2" onclick="openZip('{zipcode}', this, 'red')">{zipcode}</button>"""
            html += f"""<div id="{zipcode}", class="tabcontent2">
                    
                    <button class="tablink" onclick="openPage('pop_{zipcode}', this, 'red')">Population Stats</button>
                    <button class="tablink" onclick="openPage('home_{zipcode}', this, 'green')" id="defaultOpen">Home Value</button>
                    <button class="tablink" onclick="openPage('hur_{zipcode}', this, 'blue')">Hurricane Damage Estimates</button>
                    <button class="tablink" onclick="openPage('flood_{zipcode}', this, 'red')">Flood Damage Estimates</button>
                    <button class="tablink" onclick="openPage('tor_{zipcode}', this, 'green')">Tornado Damage Estimates</button>
                    
                    """

            for i in range(len(table_dict[zipcode])):
                html += f'<div id="{id[i]}_{zipcode}" class="tabcontent" style="background-color: {colors[i]}">'
                html += table_dict[zipcode][i]
                html += '</div>'
           
            html += '</div>'
        return render_template('home2.html', map=map_it, html=html, ziptabs=ziptabs)


# run app
if __name__ == '__main__':
    app.run()