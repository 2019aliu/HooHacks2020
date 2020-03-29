# Import the relevant libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Get the data from MongoDB atlas
import os
os.system('''mongoexport --host COVID2020-shard-0/covid2020-shard-00-00-k5vfm.mongodb.net:27017,covid2020-shard-00-01-k5vfm.mongodb.net:27017,covid2020-shard-00-02-k5vfm.mongodb.net:27017 --ssl --username admin --password admin --authenticationDatabase admin --db global --collection global_confirmed --type csv --out time_series_covid19_confirmed_global.csv --fields=Province/State,Country/Region,Lat,Long,1/22/20,1/23/20,1/24/20,1/25/20,1/26/20,1/27/20,1/28/20,1/29/20,1/30/20,1/31/20,2/1/20,2/2/20,2/3/20,2/4/20,2/5/20,2/6/20,2/7/20,2/8/20,2/9/20,2/10/20,2/11/20,2/12/20,2/13/20,2/14/20,2/15/20,2/16/20,2/17/20,2/18/20,2/19/20,2/20/20,2/21/20,2/22/20,2/23/20,2/24/20,2/25/20,2/26/20,2/27/20,2/28/20,2/29/20,3/1/20,3/2/20,3/3/20,3/4/20,3/5/20,3/6/20,3/7/20,3/8/20,3/9/20,3/10/20,3/11/20,3/12/20,3/13/20,3/14/20,3/15/20,3/16/20,3/17/20,3/18/20,3/19/20,3/20/20,3/21/20,3/22/20,3/23/20,3/24/20,3/25/20,3/26/20,3/27/20,3/28/20''')
country = pd.read_csv('time_series_covid19_confirmed_global.csv')
# reset index to still contain the country/region index
country_clean = country.groupby('Country/Region').sum().reset_index()
datesWithData = list(country_clean.columns)[3:]

# Generate world plots for Coronavirus
metricscale1=[[0, 'rgb(102,194,165)'], [0.05, 'rgb(102,194,165)'], [0.15, 'rgb(171,221,164)'], [0.2, 'rgb(230,245,152)'], [0.25, 'rgb(255,255,191)'], [0.35, 'rgb(254,224,139)'], [0.45, 'rgb(253,174,97)'], [0.55, 'rgb(213,62,79)'], [1.0, 'rgb(158,1,66)']]

dataSlider = []
for date in datesWithData:
    data_one_day = dict(
        name = date,
        type = 'choropleth',
        autocolorscale = False,
        colorscale = metricscale1,
        showscale = True,
        locations = country_clean['Country/Region'].values,
        z = np.log10(country_clean[date].values),
        # z = country_clean[date].values,
        locationmode = 'country names',
        # text = country_clean['Country/Region'].values,
        marker = dict(
            line = dict(color = 'rgb(250,250,225)', 
            width = 0.5)
        ),
        colorbar = dict(
            autotick = True, 
            tickprefix = '',
            title = 'Number of cases'
        )
    )
    dataSlider.append(data_one_day)

steps = []
for i in range(len(dataSlider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(dataSlider)],
                label=dataSlider[i]['name'])
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0,
                pad={"t": 100},
                steps=steps)] 

layout = dict(
    title = 'World Map of Global Confirmed Cases of Coronavirus since January 22, 2020',
    geo = dict(
        showframe = True,
        showocean = True,
        oceancolor = 'rgb(28,107,160)',
        #oceancolor = 'rgb(222,243,246)',
        projection = dict(
            type = 'orthographic',
                rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
            showgrid = False,
            gridcolor = 'rgb(102, 102, 102)'
        ),
        lataxis = dict(
            showgrid = False,
            gridcolor = 'rgb(102, 102, 102)'
        )
    ),
    sliders = sliders
)
fig = dict(data=dataSlider, layout=layout)
py.plot(fig, validate=False, filename='coronavirusWorld')
# py.savefig('worldmap2010.png')
# py.iplot(fig, validate=False, filename='worldmap2010')

####################################################################################################

# Unused code

# # Create our new list of countries that we want to plot for. This was done manually as I was lazy
# # to think of any clever tricks (eg text processing) to filter. 
# country_list = ['Afghanistan','Angola','Albania','Argentina','Armenia','Australia'
# ,'Austria','Azerbaijan','Burundi','Belgium','Benin','Burkina Faso','Bangladesh','Bulgaria'
# ,'Bahrain','Bosnia and Herzegovina','Belarus','Belize','Bolivia','Brazil','Barbados','Brunei Darussalam'
# ,'Bhutan','Botswana','Central African Republic','Canada','Switzerland','Chile','China','Cameroon'
# ,'Congo','Colombia','Comoros','Cabo Verde','Costa Rica','Cuba','Cyprus','Czech Republic','Germany'
# ,'Denmark','Dominican Republic','Algeria','Ecuador','Egypt','Spain','Estonia','Ethiopia','Finland','Fiji'
# ,'France','Gabon','United Kingdom','Georgia','Ghana','Guinea','Greece','Guatemala','Guyana','Hong Kong'
# ,'Honduras','Croatia','Haiti','Hungary','Indonesia','India','Ireland','Iran','Iraq','Iceland','Israel'
# ,'Italy','Jamaica','Jordan','Japan','Kazakhstan','Kenya','Cambodia','Korea, Rep.','Kuwait','Lebanon','Liberia'
# ,'Libya','Sri Lanka','Lesotho','Lithuania','Luxembourg','Latvia','Macao','Morocco','Moldova','Madagascar'
# ,'Maldives','Mexico','Macedonia','Mali','Malta','Myanmar','Montenegro','Mongolia','Mozambique','Mauritania'
# ,'Mauritius','Malawi','Malaysia','North America','Namibia','Niger','Nigeria','Nicaragua','Netherlands'
# ,'Norway','Nepal','New Zealand   ','Oman','Pakistan','Panama','Peru','Philippines','Papua New Guinea'
# ,'Poland','Puerto Rico','Portugal','Paraguay','Qatar','Romania','Russian Federation','Rwanda','Saudi Arabia'
# ,'Sudan','Senegal','Singapore','Solomon Islands','Sierra Leone','El Salvador','Somalia','Serbia','Slovenia'
# ,'Sweden','Swaziland','Syrian Arab Republic','Chad','Togo','Thailand','Tajikistan','Turkmenistan','Timor-Leste'
# ,'Trinidad and Tobago','Tunisia','Turkey','Tanzania','Uganda','Ukraine','Uruguay','United States','Uzbekistan'
# ,'Venezuela, RB','Vietnam','Yemen, Rep.','South Africa','Congo, Dem. Rep.','Zambia','Zimbabwe' 
# ]
# # Create a new dataframe with our cleaned country list
# # country_clean = country[country['Country/Region'].isin(country_list)]

# data = [ dict(
#     type = 'choropleth',
#     autocolorscale = False,
#     colorscale = metricscale1,
#     showscale = True,
#     locations = country_clean['Country/Region'].values,
#     z = np.log10(country_clean['3/28/20'].values),
#     # z = country_clean['3/28/20'].values,
#     locationmode = 'country names',
#     text = country_clean['Country/Region'].values,
#     marker = dict(
#         line = dict(color = 'rgb(250,250,225)', width = 0.5)),
#         colorbar = dict(
#             autotick = True, 
#             tickprefix = '', 
#             # tickvals = [0, 1, 10, 100, 1000, 10000, 100000, 1000000],
#             title = 'Number of cases')
# ) ]