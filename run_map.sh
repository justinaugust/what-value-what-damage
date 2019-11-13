jupyter-nbconvert --to script 1-data.ipynb 
mv 1-data.py datafetching.py
jupyter-nbconvert --to script 2-make_map.ipynb 
mv 2-make_map.py map_it.py
jupyter-nbconvert --to script 3-map_launch_flask.ipynb
python3 3-map_launch_flask.py
