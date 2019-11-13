# What Value? What Damage?
## DSI Project-5

### Problem 4: Extracting Building Values from Zillow
_Dylan Bailey, Albert Wong, Justin August_, General Assembly Data Science Immersive Fall 2019, SF Campus

1. [Problem Statement](#problem-statement)
2. [Data](#data)
3. [Damage Modeling](#damage-modeling)
4. [FLASK Implimentation](#flask-implementation)
4. [Known Issues](#known-issues)
5. [Future Features](#future-features)
6. [Media Links](#media-links)


## Problem statement

- During a disaster, it is important to model and estimate the potential or forecasted effect of the event, including the projected/forecasted damage.
- Existing indicators of forecasted damage include number of structures within the affected area, number of people in the area, number of households, demographics of the impacted population, etc.
- This project will add an additional indicator: the value of the properties in the affected area. Property values can be estimated according to the market price of houses.
- In this project, the students will leverage property market prices published in different real-estate websites (e.g. Zillow), according to zip codes.

## Prior Work
- [Github Link for DSI-ATL students' past work.](https://github.com/katychow/DSI_Project4_Zipcodes)
- [Github Link for DSI-BOS students' past work.](https://github.com/hixjas/Project-4-Zillow)
- [Github Link for DSI-DC students' past work.](https://github.com/tbacas/Zillow-Disaster-Estimates)
- [Github Link for DSI-DC (2) students' past work.](https://github.com/zeeemo/Disaster-Estimates)
- [Github Link for DSI-DC (3) students' past work.](https://github.com/jhuessy/ga_client_project_zillow)
- [Github Link for DSI-NYC students' past work.](https://github.com/cbratkovics/damage_estimator)
- [Github Link for DSI-NYC (2) students' past work.](https://github.com/rows317/DSI-8-Client-Project/blob/master/README.md)
- [Github Link for DSI-SEA students' past work.](https://github.com/dsteffan/mount_rainier_disaster_estimate)

## Data

###Sources
	
- [QUANDL](https://www.quandl.com/data/ZILLOW-Zillow-Real-Estate-Research) - QUANDL provides access to auto-calculated real-estate data for all zip codes that Zillow serves.
- [US Census](https://www.census.gov/data.html) - Shapefiles for every Zip Code Tabulated Area were obtained here.
- [`uszipcode` Python Module](https://uszipcode.readthedocs.io/index.html) - Provided population, density and occupied housing units.
	
	
### Fetching
	
Data is fetched dynamically from QUANDL based on the age of the data. QUANDL data is updated every week so if the data is older than a week, new data will be fetched.
	
Known Issues:
	- Some zip codes do not correspond to geographic shapes and those cannot be fetched.
	- Zip codes that Zillow does not have data for cannot be fetched
	
### Combining
GeoJSON Shapes are stored separately from the QUANDL Data, along with the other data from the `uszipcodes` module. As this data is relatively static it is not needed to be updated on a regular basis.
	
### Cleaning
	
Any `null()` values were due to mistakes in the data collection process. They were dropped and made up a very small percentage of the data.



## Damage Modeling
### Damage Functions

#### Hurricane Function

- Taken from [research paper](http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1119&context=crp_fac) by Michael R. Boswell, Robert E. Deyle, Richard A. Smith, and E. Jay Baker at Florida State University 
- Linear Regression model from historical hurricane damage costs and uses 20 independent variables from population, house value, geography and wind.
- Data for population in each zipcode from uszipcode
- Scale for wind was taken from the Saffir-Simpson Hurricane Scale

#### Flood Damage

- Created from [FEMA estimates from 2017 on flood damage estimates](https://www.fema.gov/media-library-data/1499290622913-0bcd74f47bf20aa94998a5a920837710/Flood_Loss_Estimations_2017.pdf)
- Uses table from FEMA estimates for the three categories of houses to calculate damage to each house
- Data for number of houses in each zip-code from us zip-code
- Damage is calculated for each type of house in the zip code (Assumes each house in a zip code is the same category of house.

#### Tornado Damage

- Damages are estimated from [fujita scale for tornados] (https://www.spc.noaa.gov/faq/tornado/f-scale.html)
- Percentage of damage to house estimated and multiplied by the average Zestimate of the houses in each tier.
- Percentage of zip code hit by a tornado is calculated from the area an average tornado covers (1.081 sq miles) divided by the sq miles of the zip code.
- Zestimate for low, medium, and top tier from Quandle based on Zillow data.
- Number of houses in each zip-code from us zip-code

## FLASK Implementation

We wanted to create a website to allow our user to input zip codes to generated a map with home values and damage estimates. This is where Flask comes in. We have all of our python scripts to generated our map with detail informations on zip codes, but we needed it in html format.

Flask allow us to run our scripts and integrate it into html templates we created. Anytime our user input zip codes they are sent to our python scripts on Flask, it is return back to Flask and sent into our html templates.

## Known Issues

- ZIP Codes without Zillow data are not displayed
- Folium limits access to Leaflet.js options
- Some metrics are naive


## Future Features
- Earthquake damage simulator
- Fire damage simulator
- “Drop a pin” functionality
- Improve existing metric functions
- More robust home data using multiple inputs
- Full Leaflet.js implementation
- Aggregate damage estimates for all zip codes


## Media Links
- [Demonstration Maps](map_demo.ipynb)
- [Watch a Video of the App in Action!](media/app_demo.mp4)
- Presentation
	- [Video](media/presentation.mp4)
	- [PDF](media/Damage%20Estimate%20by%20Zipcode.pdf)
	- [Slides](https://docs.google.com/presentation/d/1RO0ZZt118jAWgInrZFqbA0gMPzDycVqmgpj8uQTybpY/edit#slide=id.p)
