from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import flask
import json
import folium
from folium import plugins
from PIL import Image
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import geopandas as gpd
import pmdarima as pm
import matplotlib.pyplot as plt
import statsmodels.api as sm
import requests
from statsmodels.tsa.arima.model import ARIMA
import warnings 
import matplotlib
import os
from io import BytesIO
import time
import dash
from tempfile import NamedTemporaryFile
warnings.filterwarnings('ignore')

plt.style.use('bmh')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 10
matplotlib.rcParams['ytick.labelsize'] = 10
matplotlib.rcParams['text.color'] = 'k'
plt.style.context('bmh')
plt.rcParams["font.family"] = "Times New Roman"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

theme_switch = ThemeSwitchAIO(
    aio_id="theme", themes=[dbc.themes.COSMO, dbc.themes.CYBORG]
),

# EDICC, WASCAL,UJKZ picture
#pil_image = Image.open('/home/adzavon/Documents/MSC_Data_Analysis/Dash/assets/Screenshot from 2023-02-10 00-23-20.png') # replace with your own image

# Analysing temperature data

#All_temperature = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/Temperature/All_temperature.xls")
#All_temperature_fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# leaflet map
#url = "https://pkgstore.datahub.io/core/geo-countries/countries/archive/23f420f929e0e09c39d916b8aaa166fb/countries.geojson"
#Read in GeoJSON files for Burkina Faso's administrative boundaries

server = app.server
# country_geojson = json.load(open('/home/adzavon/Documents/MSC_Data_Analysis/study area maping/country.geojson'))
# regions_geojson = json.load(open('/home/adzavon/Documents/MSC_Data_Analysis/study area maping/regions.geojson'))
# province_geojson = json.load(open('/home/adzavon/Documents/MSC_Data_Analysis/study area maping/province.geojson'))
# commune_geojson = json.load(open('/home/adzavon/Documents/MSC_Data_Analysis/study area maping/commune.geojson'))

#country_geojson = json.load(open('https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/country.geojson'))

url_country = 'https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/country.geojson'
response = requests.get(url_country)
country_geojson = json.loads(response.text)


#regions_geojson = json.load(open('https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/regions.geojson'))
url_region = 'https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/regions.geojson'
response = requests.get(url_region)
regions_geojson = json.loads(response.text)


#province_geojson = json.load(open('https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/province.geojson'))
url_province = 'https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/province.geojson'
response = requests.get(url_province)
province_geojson = json.loads(response.text)


#commune_geojson = json.load(open('https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/commune.geojson'))
url_commune = 'https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/study%20area%20maping/commune.geojson'
response = requests.get(url_commune)
commune_geojson = json.loads(response.text)

# Create a Folium map object centered on Burkina Faso
m = folium.Map(location=[10.2, -1.8], zoom_start=7)
plugins.MiniMap().add_to(m)
plugins.Geocoder().add_to(m)

# Add GeoJSON layers for each administrative boundary level to the map
folium.GeoJson(country_geojson, name="Country").add_to(m)
folium.GeoJson(regions_geojson, name="Regions").add_to(m)
folium.GeoJson(province_geojson, name="Provinces").add_to(m)
folium.GeoJson(commune_geojson, name="Communes").add_to(m)

# Add tile layers from different map providers
folium.TileLayer('Open Street Map').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('CartoDB Dark_Matter').add_to(m)
folium.TileLayer('CartoDB Positron').add_to(m)

# Add a layer control to the map to allow the user to toggle different layers on and off
folium.LayerControl().add_to(m)

# Average Temperature for the three afro climatic zone 


url = "https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/MSC_Data_Analysis/Temperature_1/All_temperature.csv"
response = requests.get(url)

if response.status_code == 200:
    Temp_data = pd.read_csv(url)

    # Now you can use Temp_data for further processing
else:
    print("Failed to download the CSV file. Status code:", response.status_code)


Temp_data_na = Temp_data.dropna()
fig_temp = px.scatter(Temp_data_na, x="Date", y="Temperature(°C)",              
                facet_col="Location",  
                #template = 'plotly_dark',
                trendline = 'ols',
                trendline_color_override='darkblue',
                #trendline_scope="overall",
                title = "Monthly Average Temperature for a representative climatique")
fig_temp.update_traces(mode='lines')
#fig_temp.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)
#fig_temp.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)
fig_temp.update_layout(

    plot_bgcolor='white',
    paper_bgcolor='#FFC9C9',
    )

# Average precipitation for the three afro climatic zone 

Precip_data= pd.read_csv("https://raw.githubusercontent.com/davidadzavon/Msc_thesis_webapp/main/MSC_Data_Analysis/Precipitation/All_precipitation.csv")
fig_precip = px.scatter(Precip_data, x="Date", y="Precipitation(mm)",              
                facet_col="Location",  
                #template = 'plotly_dark',
                trendline = 'ols',
                trendline_color_override='darkblue',
                #trendline_scope="overall",
                title = "Monthly Average Precipitation for a representative climatique",
                
                )
fig_precip.update_traces(mode='lines')
fig_precip.update_layout(

    plot_bgcolor='white',
    paper_bgcolor='lightblue',
    )

# #fig_precip.update_xaxes(showline = True, 
#                         linecolor = 'black', 
#                         linewidth = 1,
#                         row = 1, 
#                         col = 1)
# #fig_precip.update_yaxes(showline = True, 
#                         linecolor = 'black', 
#                         linewidth = 1, 
#                         row = 1, 
#                         col = 1)



# Import the working  for the Internal displacements
import plotly.express as px
dataset_IDP = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/Migration_IDP/Sum_months_IDP.xlsx")
IDP_figure = px.scatter(dataset_IDP,
                    x="Date", 
                    y="Internal Displced People",
                    trendline = 'ols',
                    trendline_color_override='darkblue')

# Internal Displacement by regions
Region_IDP_total = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/Migration_IDP/Regions_months_IDP.xlsx")

Region_IDP = px.scatter(Region_IDP_total,
                    x="Regions", 
                    y="Internal Displced People")



#sum of the conflicts

sum_conflicts_data = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/conflicts/conflicts_sum.xlsx")
sum_conflicts_data["month"]=sum_conflicts_data["Date of Events"].dt.month
conflicts_sum_fig = px.bar(sum_conflicts_data, x="Date of Events", y="Number of Conflicts", 
                color='month' ,text='Number of Conflicts'  )

conflicts_sum_fig.update_layout(
            margin={"r":0,"t":30,"l":10,"b":10},
            coloraxis_colorbar={
                'title':'Month of Events'})

# Conflicts data analysis per month
# year_conflict = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/conflicts/conflicts.xlsx")
# year_conflict["EVENT_DATE"] = pd.to_datetime(year_conflict["EVENT_DATE"])
# year_conflict["Year"] = year_conflict["EVENT_DATE"].dt.year

# new_data = year_conflict.groupby(["Year","ADMIN1","EVENT_TYPE"]).size().reset_index(name="Total_conflicts")
year_conflict = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/conflicts/conflicts.xlsx")
year_conflict["EVENT_DATE"] = pd.to_datetime(year_conflict["EVENT_DATE"])
# year_conflict["Year"] = year_conflict["EVENT_DATE"].dt.year
# year_conflict["month"] = year_conflict["EVENT_DATE"].dt.year
year_conflict['Date'] = year_conflict['EVENT_DATE'].dt.strftime('%b-%y')
year_conflict
year_conflict_drop = year_conflict.drop(columns=["EVENT_DATE"])
year_conflict_drop
new_data = year_conflict_drop[["Date","ADMIN1","EVENT_TYPE"]]
new_data["Total_conflicts"] = 1
new_data


color_discrete_sequence = ['#ec7c34']*len(new_data)
color_discrete_sequence[5] = '#609cd4'
all_conflict_fig = px.bar(new_data, 
                          x="Date", y="Total_conflicts",
                          color='EVENT_TYPE', barmode='group',
                category_orders= {"EVENT_TYPE":['Battles', 'Protests', 'Strategic developments', 'Riots',
       'Violence against civilians', 'Explosions/Remote violence']},
       color_discrete_map={'Battles' : "red",
                           'Protests':"blue", 
                           'Strategic developments':"pink",
                            'Riots':"grey",
                            'Violence against civilians':"green", 
                            'Explosions/Remote violence':"orange"}
)


# conflicts occurence by regions

region_bar_fig = px.bar(new_data, x="ADMIN1", y="Total_conflicts",color='EVENT_TYPE', barmode='group'
                #color='month' ,text='Number of Conflicts'
)
# region_bar_fig.update_layout(
#             margin={"r":0,"t":30,"l":10,"b":10},
#             coloraxis_colorbar={
#                 'title':'Annual conflict cases'})

#region_bar_fig.show()
# last  = new_data.groupby(["Date","EVENT_TYPE"]).sum()
# last.to_excel("conflicts_by_event.xlsx")

# re_import = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/conflicts/conflicts_by_event.xlsx")

#######################

# plot the conflicts zone on map

dataset = pd.read_csv("/home/adzavon/Documents/MSC_Data_Analysis/map_for conflicts/conflicts_true.csv")
dataset['Region'] = dataset['Region'].replace(['Hauts-Bassins'], 'Haut-Bassins')
dataset['Region'] = dataset['Region'].replace(['sahel'], 'Sahel')
dataset['Region'] = dataset['Region'].replace(['boucle du Mouhoun'], 'Boucle du Mouhoun')

# merge shapefile and csv
shapefile = gpd.read_file("/home/adzavon/Documents/MSC_Data_Analysis/study area maping/gadm36_BFA_shp/gadm36_BFA_shp/gadm36_BFA_1.shp")
shapefile_map = shapefile[["NAME_1","geometry"]]
merged = shapefile_map.merge(dataset, left_on="NAME_1", right_on="Region")
simplify_merge_old = merged[["Year","Region","EVENT_TYPE","SUM_CONFLICTS","geometry"]]
simplify_merge = simplify_merge_old.set_index("Region")



##########################

# Analysis of extreme event in burkina kaso

disaster = pd.read_excel("/home/adzavon/Documents/MSC_Data_Analysis/Diseaster/Conasur_disaster_data.xlsx",)
disaster["Province"].unique()

# change the wrong wrinting to the right one
disaster["Region"] = disaster["Region"].replace(["NAMENTENGA"],"Centre-Nord")
disaster["Region"] = disaster["Region"].replace(["GANZOURGOU"],"Plateau-Central")
disaster["Region"] = disaster["Region"].replace(["BAM"],"Centre-Nord")
disaster["Region"] = disaster["Region"].replace(["BOUGOURIBA"],"Sud-Ouest")
disaster["Region"] = disaster["Region"].replace(["KOURWEOGO"],"Plateau-Central")
disaster["Region"] = disaster["Region"].replace(["BAZEGA"],"Centre-Sud")
disaster["Region"] = disaster["Region"].replace(["YATENGA"],"Nord")
disaster["Region"] = disaster["Region"].replace(["LOROUM"],"Nord")
disaster["Region"] = disaster["Region"].replace(["BANWA"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["NAYALA"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["HOUET"],"Haut-Bassins")
disaster["Region"] = disaster["Region"].replace(["KENEDOUGOU"],"Haut-Bassins")
disaster["Region"] = disaster["Region"].replace(["SISSILI"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["GOURMA"],"Est")
disaster["Region"] = disaster["Region"].replace(["KOSSI"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["IOBA"],"Sud-Ouest")
disaster["Region"] = disaster["Region"].replace(["NOUMBIEL"],"Sud-Ouest")
disaster["Region"] = disaster["Region"].replace(["OUDALAN"],"Sahel")
disaster["Region"] = disaster["Region"].replace(["SOUM"],"Sahel")
disaster["Region"] = disaster["Region"].replace(["SANGUIE"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["ZONDOMA"],"Nord")
disaster["Region"] = disaster["Region"].replace(["SENO"],"Sahel")
disaster["Region"] = disaster["Region"].replace(["SANMATENGA"],"Centre-Nord")
disaster["Region"] = disaster["Region"].replace(["YAGHA"],"Sahel")
disaster["Region"] = disaster["Region"].replace(["SOUROU"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["PASSORE"],"Nord")
disaster["Region"] = disaster["Region"].replace(["NAHOURI"],"Centre-Sud")
disaster["Region"] = disaster["Region"].replace(["KOURITTENGA"],"Centre-Est")
disaster["Region"] = disaster["Region"].replace(["TUY"],"Haut-Bassins")
disaster["Region"] = disaster["Region"].replace(["OUBRITENGA"],"Plateau-Central")
disaster["Region"] = disaster["Region"].replace(["KADIOGO"],"Centre")
disaster["Region"] = disaster["Region"].replace(["BOULGOU"],"Centre-Est")
disaster["Region"] = disaster["Region"].replace(["COMOE"],"Cascades")
disaster["Region"] = disaster["Region"].replace(["BOULKIEMDE"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["BALE"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["TAPOA"],"Est")
disaster["Region"] = disaster["Region"].replace(["ZIRO"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["ZOUNDWEOGO"],"Centre-Sud")
disaster["Region"] = disaster["Region"].replace(["MANGA"],"Centre-Sud")
disaster["Region"] = disaster["Region"].replace(["MOUHOUN"],"Boucle du Mouhoun")
disaster["Region"] = disaster["Region"].replace(["PONI"],"Sud-Ouest")
disaster["Region"] = disaster["Region"].replace(["Boulkiemdé"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["Centre"],"Centre")
disaster["Region"] = disaster["Region"].replace(["Koudougou"],"Centre-Ouest")
disaster["Region"] = disaster["Region"].replace(["Boromo"],"Boucle du Mouhoun")
disaster["Event_type"] = disaster["Event_type"].replace(["Inondations"],"Floods")
disaster["Event_type"] = disaster["Event_type"].replace(["Vents violents"],"Storms")
disaster["Event_type"] = disaster["Event_type"].replace(["Vent violent"],"Storms")

# organisation and class the data too be counted at each extreme event

disasters = disaster[["Date","Region","Event_type"]]
disasters["Total_disaster"] = 1
disasters["Year"]=disasters["Date"].dt.year

fig_event_region = px.bar(disasters,x="Region",y="Total_disaster",color="Event_type"#,barmode="group"
             )
fig_event_region.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)
fig_event_region.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)

fig_event_region.update_layout(
    title={
        'text': "Climate extreme events by Region",
        'font': {'family': 'Times New Roman', 'size': 24, 'color': 'black'},
        'x': 0.5,
        'xanchor': 'center'},
    xaxis_title={
        'text': "Region",
        'font': {'family': 'Times New Roman', 'size': 18, 'color': 'black'}},
    yaxis_title={
        'text': "Number of extreme events registered",
        'font': {'family': 'Times New Roman', 'size': 18, 'color': 'black'}},
    font=dict(family="Times New Roman", size=14, color='black')
)
# fig_event_region.update_layout(
#             margin={"r":0,"t":30,"l":10,"b":10},
#             coloraxis_colorbar={
#                 'title':'Annual conflict cases'})

#fig_event_region.show()

# having the date in a goog format
disasters
disasters["Date"] = pd.to_datetime(disasters["Date"])
disasters = disasters[["Date","Region","Event_type","Total_disaster"]]
disasters['Date'] = disasters['Date'].dt.strftime('%Y-%m')

disaster_s = disasters.groupby(["Date","Region","Event_type"]).sum()

fig_event_date = px.bar(disasters,x="Date",
                        y="Total_disaster",
                        color="Event_type",#barmode="group"
             )
fig_event_date.update_xaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)
fig_event_date.update_yaxes(showline = True, linecolor = 'black', linewidth = 1, row = 1, col = 1,)

fig_event_date.update_layout(
    title={
        'text': "Climate extreme events (2018 - 2022)",
        'font': {'family': 'Times New Roman', 'size': 24, 'color': 'black'},
        'x': 0.5,
        'xanchor': 'center'},
    xaxis_title={
        'text': "Date",
        'font': {'family': 'Times New Roman', 'size': 18, 'color': 'black'}},
    yaxis_title={
        'text': "Number of extreme events registered",
        'font': {'family': 'Times New Roman', 'size': 18, 'color': 'black'}},
    font=dict(family="Times New Roman", size=14, color='black')
)
# fig_event_date.update_layout(
#             margin={"r":0,"t":30,"l":10,"b":10},
#             coloraxis_colorbar={
#                 'title':'Annual conflict cases'})

#fig_event_date.show()


##############################################

# add the forecasting

data0 = pd.read_csv("/home/adzavon/Documents/MSC_Data_Analysis/merge for forecasting/causality_and_var.csv",
                   index_col='Date', parse_dates=True)

# distribution of the data

data_Idp = data0[["Idp"]] 

#Split data into training and testing sets
train = data0[:'2022-05-01']
test = data0['2022-06-01':]

# Fit ARIMA model to training data
model = ARIMA(train['Idp'], order=(5, 2, 2))
model_fit = model.fit()

# Generate forecasts for the next six months
forecast = model_fit.get_forecast(steps=31)

# Extract the forecasted values and confidence intervals
pred_values = forecast.predicted_mean
pred_ci = forecast.conf_int()

def animate_text(text):
  number_of_characters=1
  while True:
    print("\n")
    print(text[0:number_of_characters])
    number_of_characters += 1
    if number_of_characters > len(text):
      number_of_characters = 0
    time.sleep(0.2)
    os.system('clear')  
  
  
#Main Program Starts Here....
#animate_text("Hello World!")

app.layout = html.Div([

     #Title of the web application
   
    html.Br(),
    html.H1( id='animated-text',  # Add an id to the H1 element
       #children = "YOU ARE ALL WELCOME TO MY MASTER RESEARCH THESIS DEFENSE",
            className="bg-success text-white p-2 mb-3 text-center",
            style = {'textAlign':'center','marginTop':20,
            'marginBottom':40,
            'fontSize': '70px'}),

         dcc.Interval(
            id='interval-component',
            interval=200,  # Update interval in milliseconds
            n_intervals=0
        ),

    html.Br(),
    html.Div(
        className='d-flex justify-content-center',
        children=[
            dbc.Spinner(color="primary", type="grow"),
            dbc.Spinner(color="secondary"),
            dbc.Spinner(color="success", type="grow"),
            dbc.Spinner(color="warning"),
            dbc.Spinner(color="danger", type="grow"),
            dbc.Spinner(color="info"),
            dbc.Spinner(color="purple", type="grow"),
            dbc.Spinner(color="dark"),
        ]
    ),
    html.Br(),

    # EDICC, WASCAL,UJKZ picture
    
    html.Img(src="assets/Screenshot from 2023-02-10 00-23-20.png",
    style={ "margin-left": 150, "margin-right": "auto"}
    ),
    html.Br(),
    html.Br(),
    html.Div(
        className='d-flex justify-content-center',
        children=[
            dbc.Spinner(color="primary"),
            dbc.Spinner(color="secondary", type="grow"),
            dbc.Spinner(color="success"),
            dbc.Spinner(color="warning", type="grow"),
            dbc.Spinner(color="danger"),
            dbc.Spinner(color="info", type="grow"),
            dbc.Spinner(color="purple"),
            dbc.Spinner(color="dark", type="grow"),
        ]
    ),
    html.Br(),
    
    html.Div(children="Web Application to show the results", 
            className="text-decoration-underline",
            style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
    html.Br(), 
    
    # The sudy area writing

    html.H1(children = "Study Area",
            className="bg-secondary text-white p-2 mb-3 text-center",

            #style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
    html.Br(),

    # The leaflet map
    html.Iframe(
            id='map',
            srcDoc=m._repr_html_(),
            width='100%',
            height='600'
        ),

    #html.Img(src="assets/istockphoto-1283061834-612x612.jpg",
    #   style={ "margin-left": 20, "margin-right": "auto"})
    # dl.Map(children=[dl.TileLayer(), dl.GeoJSON(url=url)],
    #                     style={'width': '100%', 'height': '50vh',
    #                     'margin': "auto", "display": "block"}),
    # html.Br(),
    html.Br(),
    html.Br(),


    # Temperature of the tree climatic zone
    html.H1(children = "Temperature",
            className="bg-danger text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    ),


    dcc.Graph(
        id='Temperature',
        figure=fig_temp
    ),

    html.Br(),
    html.Br(),
    dcc.Markdown('''
        #### Description of temperature trends in the study area

        Burkina Faso has three climatic zones. In the north of
        the country, the first is the **Sahelian zone**. In the 
        center, the **Sudano-Sahelian zone**, and in the south of 
        the country, the **Sudanian zone**. In this study, we used 
        representative synoptic stations to characterize the 
        climate in these three climatic zones. In the north, 
        the Dori station; in the center, the Ouagagougou 
        station (the capital); and in the south, the Bobo Dioulasso 
        station. From these three graphs, we can see that 
        average monthly temperatures vary according to climatic zone. 
        The northern zone is the hottest. In the Sahelian zone, 
        the average monthly temperature is between 34 and 37°C 
        during hot spells, and as low as 21 and 24°C during cool 
        spells. On the other hand, in the central Sudano-Sahelian 
        zone, the average monthly temperature varies between 32 
        and 35°C in the hot season and between 22 and 25°C in the 
        cool season. Finally, the southern zone, the Sudanian, has 
        an average monthly temperature of between 27 and 31°C in hot 
        periods, sometimes reaching 23 and 25°C in cool periods.  
        This analysis shows that the Sahelian zone has more temperature 
        extremes than the others, depending on weather changes. 
        Temperatures in the Southern Zone are not very sensitive 
        to seasonal or periodic changes. However, we can see that 
        temperatures in all three climatic zones have an upward 
        trend, which means that despite the monthly variability 
        observed, temperatures within the zone generally increase 
        over time, even if the slope is not very steep.

        For more detailed information click [`here`](https://www.donneesmondiales.com/afrique/burkina-faso/climat-boucle-du-mouhoun.php).

        '''),

    
    # Precipitation of the tree climatic zone
    html.H1(children = "Precipitation", 
            className="bg-info text-white p-2 mb-3 text-center",
            style={'text-align':'right','marginTop':60,'fontSize': '30px'}
            ),

    dcc.Graph(
        id='Precipitation',
        figure=fig_precip
    ),

    html.Br(),
    html.Br(),
    dcc.Markdown('''
        #### Description of Precipitation trends in the study area

        Precipitation is a really important climatic variable. In Burkina
        Faso there are only two seasons. A dry one and a rainy one, 
        each lasting six months. Over the last thirty years, Burkina 
        Faso has seen an increase in the amount of rainfall recorded 
        per month.  This increase is slight and can be seen over time. 
        The dry season begins in November and ends in April, while the 
        rainy season begins in May and ends in October. In terms of a 
        comparative analysis of these three climatic zones, the Sahelian 
        zone receives the least rainfall. Thus, the Sudanian zone receives 
        a lot of rain per month compared with the other zones.  It varies 
        from month to month, with some months, such as July, August and 
        September, receiving more rain than others. Agriculture in Burkina 
        faso, even when it has begun to apply irrigation, remains fairly 
        dependent on rainfall. Moreover, the regions located in the 
        Sudanianne zone have a more productive agriculture than other 
        regions, as is the case of the Hauts Bassins and Cascades regions.


        For more detailed information click [`here`](https://climateknowledgeportal.worldbank.org/country/burkina-faso/climate-data-historical#:~:text=Three%20climate%20zones%20split%20the,the%20southern%20more%20humid%20Sudanian).

        '''),


    html.Br(),

    html.Br(),
    html.H4(children = 'Analyse of the extreme events over the time',className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),

    html.Div(className='row', children=[
       
       html.Div(className='col-md-6', children=[\
            dcc.Graph(id="Sum of_conflicts",
                      figure=fig_event_date,
                      className='plot')]),


        html.Div(className='col-md-6', children=[
           
            html.Div(children="Description of extreme events over time", 
            className="text-decoration-underline",
            style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
            html.Hr(),

            dcc.Markdown('''
            This graph shows how extreme events have evolved over time. 
            Our study focused on two environmental disasters: floods and 
            high winds. This graph shows occurrence by month of the year. 
            The red represents the storms and the blue the floods recorded 
            in each month. The longer the bar graph, the greater the number 
            of extreme events. On this graph, we can see that in 2022, all 
            recorded events are floods. In addition, floods, which can only 
            occur during rainy periods, are periodic on our graph. They usually 
            occur between May and November. On the other hand, cases of violent 
            winds are present in rainy periods or in the dry season, which really 
            begins in December and ends in April or May. We can see that there 
            are more floods than storms, but 2018, 2020 and 2021 in particular 
            were years in which storms occurred more frequently. The highest peak 
            in flooding was in 2018, but in 2021 and 2022 there are also a number 
            of recorded floods that deserve special attention. Storms generally 
            arrive in periods of more or less the same month, so it's likely that 
            the rains will also arrive with violent winds in Burkina faso.
            
          '''),
          html.Hr()
        ], style={'backgroundColor':'#c5d9ed',})
    ]),


   html.Br(),

     html.H4(children = 'Analyse of the extreme events by region',className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
        html.Br(),
        dcc.Graph(
        id='Sum of conflicts',
        figure=fig_event_region),
    html.Br(),

     # Internal displacement analysis
    html.H1(children = "Internal Displacement over the years",className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    ),
    html.Div(className='row', children=[
        html.Div(className='col-md-6', children=[
            dcc.Graph(id="Internal Displacement over the years",
                      figure=IDP_figure,
                      className='plot')

        ]),
        html.Div(className='col-md-6', children=[
            html.Br(),

            html.Div(children="Description of internal disaplacement over time", 
            className="text-decoration-underline",
            style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),

            html.Hr(),
            dcc.Markdown('''
            
                Internal displacement in Burkina Faso has 
                made great strides and is becoming a well-known 
                phenomenon on the national territory. At the 
                beginning of 2018, the number of people was 
                really low and did not require any particular 
                attention. But towards the middle of 2018, 
                everything changed. The number of internally 
                displaced persons in the country has been rising 
                steadily. Up until 2020, the situation became 
                worrying, to the point where the number of 
                internally displaced people exceeded one million. 
                Today, it continues to rise, and is approaching 
                2 million. However, this upsurge has drawn our 
                attention in order to carry out a specific study 
                on the issue of internally displaced people and to 
                propose approaches or opportunistic policies so that 
                this number can be reduced in the coming years. 
                        
         '''),
            html.Hr(),
              
        ],style={'backgroundColor':'#fcf0f1'})
    ]),

    # dcc.Graph(
    #     id="Internal Displacement over the years",
    #     figure=IDP_figure
    #         ),
    html.Br(),

       # Internal displacement analysis
    html.H1(children = "Internal Displacement Data by Regions", className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    ),

    # dcc.Graph(
    #     id="Internal Displacement Data by Regions",
    #     figure=Region_IDP
    #         ),
    html.Br(),
    html.Div(className='row', children=[
        html.Div(className='col-md-6', children=[
            dcc.Graph(id="nternal Displacement Data by Regions",
                      figure=Region_IDP,
                      className='plot')

        ]),
        html.Div(className='col-md-6', children=[
            html.Br(),
           html.Div(children="Description of internal disaplacement over time", 
            className="text-decoration-underline",
            style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
        html.Hr(),

    dcc.Markdown('''

        Here, we're interested in the region of origin 
        of internal transferees. Through this analysis 
        of their regions of origin, we found that many 
        of these people would have come from the Centre-Nord 
        region, the Sahel region, the Nord and the Est. In 
        the Centre-Nord region, there are almost 700,000 
        internally displaced persons, followed by the Sahel 
        region, which also has almost 600,000 internally 
        displaced persons. The North and East regions follow, 
        with 250,000 and 200,000 people respectively. On the 
        other hand, there are areas with low levels of internal 
        displacement. These areas are the Centre region, with almost
        1,000 internally displaced people, and the Centre-Sud region, 
        with almost 9,000 people considered internally displaced. 
        In the other regions, however, the number of internally 
        displaced people is between 35,000 and 100,000 thousand. 
        These are the regions around the center.
                       
         '''),
         html.Hr(),
        ], style={'backgroundColor':'#F1F1F1'})
    
    ]),

    # conflicts analysis (sum)
    html.H1(children = "Sum of conflicts", className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    ),
    
    dcc.Graph(
        id='Sum_of_conflicts',
        figure=conflicts_sum_fig),

    html.Br(),

    # All conflicts over the years
    html.H1(children = "All the type of conflicts over the Year", className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    ),

    dcc.Graph(
        id='All the type of conflicts over the Year',
        figure= all_conflict_fig,
        
    ),
    html.Br(),

    # conflict vizualisation by month

    html.Div([
        html.H4('Events by year (2018 - 2022)'),
        dcc.Dropdown(
            id="dropdown_events",
            options=[{'label':year , 'value':year} 
                        for year in sorted(new_data["Date"].unique())],
            value=[],
            clearable=False,
            multi=True,
            placeholder="Select your dates"
        ),
        html.Br(),
        dcc.Graph(id="graph_events"),
    ]),
# conflicts vizualisation by region in plot
    # html.H1(children = "All the type of conflicts over the Regions",className="bg-primary text-white p-2 mb-3 text-center",
    # style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    #         ),

    # dcc.Graph(
    #     id='All the type of conflicts over the Regions',
    #     figure=region_bar_fig,className="m-4"
    # ),
    # html.Br(),
# To plot conflict area spatially
  
    html.H4(children = 'Spatial and temporal analysis of conflicts',className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
    html.P("Select an event type:"),
    dcc.RadioItems(
        id='EVENT_TYPE', 
        options=[{"label": "Battles", "value": "Battles"}, 
                 {"label": "Explosions/Remote violence", "value": "Explosions/Remote violence"},
                 {"label": "Protests", "value": "Protests"},
                 {"label": "Riots", "value": "Riots"},
                 {"label": "Strategic developments", "value": "Strategic developments"}],
        value="Battles",
    ),
    html.P("Select a year:"),
    
    dcc.RadioItems(
        id='Year', 
        options=[{"label": str(year), "value": year} for year in sorted(simplify_merge['Year'].unique())],
        value=2018,
    ),
    dcc.Graph(id="graph"),

    # html.Br(),
    # html.H4(children = 'Analyse of the extreme events over the time',className="bg-primary text-white p-2 mb-3 text-center",
    # style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    #         ),
    #     dcc.Graph(
    #     id='Sum of_conflicts',
    #     figure=fig_event_date),

    # html.Br(),

    #  html.H4(children = 'Analyse of the extreme events by region',className="bg-primary text-white p-2 mb-3 text-center",
    # style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
    #         ),
    #     dcc.Graph(
    #     id='Sum of conflicts',
    #     figure=fig_event_region),

    html.Br(),

    ##### forecasting 

     html.H1(children = 'Internal Displacement forecasting',className="bg-primary text-white p-2 mb-3 text-center",
    style={'textAlign':'center','marginTop':60,'fontSize': '30px'}
            ),
    html.Br(),
    html.H1(children = 'Montly Internal Displacement forecasting for 2025'),
    html.Br(),
        html.Label("Select Number of month you want to forecast", htmlFor="my-slider"),
        dcc.RangeSlider(min=0, max=31, step=1, value=[0,1],id="my-slider",
                        marks={
        i: {
            "label": f"Month {i}",
            "style": {"transform": "rotate(45deg)", "white-space": "nowrap"},
        }
        for i in range(1, 32)
    },),
     html.Br(),
    dcc.Graph(id='our-graph',
              style = {'margin':'auto','width': "50%"} ),
    

#####################
#   put the futher at the tail
#####################

dbc.Tabs([
        dbc.Tab([

            html.Div(className = "row", children = [
                html.Div(className = "col-md-4", children = [
            html.Ul([
                html.Br(),
                html.H3( 
                "Student",
                
                style={"font-size": "20px", "text-decoration": "underline"},
            ),
            html.Img(src="assets/david.png", width="100", height="100"
    
            ), 
            html.Br(),
            html.Br(),
            html.Li('Dr. Koffi Doh David ADZAVON'),

             html.H3(
                "Contact information",
                style={"font-size": "20px", "text-decoration": "underline"},
            ),

            dcc.Markdown('''

            +228 92463792 / +226 07666825
            
            '''),
        html.Li(['LinkedIn: ', html.A('hhttps://www.linkedin.com/in/koffi-doh-david-adzavon-821a9723b/',href='https://www.linkedin.com/in/koffi-doh-david-adzavon-821a9723b/')]),
        html.Br(),
            
        ]),
    ]),

    html.Div(className="col-md-4", children=[
        html.Br(), 

             html.H3(
                "Supervisor",
                style={"font-size": "20px", "text-decoration": "underline"},
            ),
            html.Img(src="assets/315807014_2653030521495265_2179227970308179347_n.jpg",
                      width="100", 
                      height="100"),
            html.Br(),
            html.Br(),
            html.Li('Dr. Kwami Ossadzifo WONYRA'),

             html.H3(
                "Contact information",
                style={"font-size": "20px", "text-decoration": "underline"},
            ),

            dcc.Markdown('''

            +228 90013209
            
            '''),
        html.Li(['LinkedIn: ', html.A('https://www.linkedin.com/in/kwami-ossadzifo-wonyra-7b5b8943/?originalSubdomain=tg',href='https://www.linkedin.com/in/kwami-ossadzifo-wonyra-7b5b8943/?originalSubdomain=tg')]),
        html.Br(),
         

    ]),


    html.Div(className="col-md-4", children=[
        html.Br(), 

             html.H3(
                "Supervisor",
                style={"font-size": "20px", "text-decoration": "underline"},
            ),
            html.Img(src="assets/342045109_892702281794164_819791163060069082_n.jpg",
                      width="100", 
                      height="100"),
            html.Br(),
            html.Br(),
            html.Li('Dr. Safietou SANFO'),

             html.H3(
                "Contact information",
                style={"font-size": "20px", "text-decoration": "underline"},
            ),

            dcc.Markdown('''

            +226 79264850
            
            '''),
        html.Br(),
         

    ]),

       
         

    ]),

        #         html.Li('ADZAVON Koffi Doh David'),
        #         html.Br(),
        #          html.H3(
        #         "Contact information",
        #         style={"font-size": "20px", "text-decoration": "underline"},
        #     ),

        #     dcc.Markdown('''

        #     +228 92463792 / +226 07666825
            
        #     '''),
        # html.Li(['LinkedIn: ', html.A('hhttps://www.linkedin.com/in/koffi-doh-david-adzavon-821a9723b/',href='https://www.linkedin.com/in/koffi-doh-david-adzavon-821a9723b/')]),
        # html.Br(),
######### for the student
            #     html.H3(
            #     "Supervisor",
            #     style={"font-size": "20px", "text-decoration": "underline"},
            # ),
            # html.Li('Dr. Kwami Ossadzifo WONYRA'),
    
######## for the first supervisor
        #     html.H3(
        #         "Supervisor",
        #         style={"font-size": "20px", "text-decoration": "underline"},
        #     ),
        #     html.Li('Dr. Safietou SANFO'),
        #  html.Br(),


    ], label="Reference Persons", ),

    dbc.Tab([
       
       
       html.Br(),
       html.H1(
          "The sources of the different data used for this study",
                style={"font-size": "20px", "text-decoration": "underline"},        
        ),
        html.Br(), 
    
    html.Br(), 
    html.Div(className = "row", children = [
                html.Div(className = "col-md-12", children = [
                   dcc.Markdown('''

            The data of environemental disasters, and of 
            internal dispalced are provided 
            by SP/CONASUR and from the Fire Service in Burkina Faso.
            However, We can follow the 
            link [`here`](https://twitter.com/spconasur) 
            and [`here`](http://www.conasur.gov.bf/)
            to access more informations. In case of very accurate information we can contact them.
            
            '''),
            html.Br(), 
                ]),]),

    html.Div(className = "row", children = [
                html.Div(className = "col-md-12", children = [
                   dcc.Markdown('''

            The data of conflicts are gathered from The Armed 
            Conflict Location & Event Data Project (ACLED) the 
            information can be accessed through the 
            link [`here`](https://acleddata.com/)
            for more informations.
            
            '''),
            html.Br(), 
                ]),]),

    ],label="Data Source",),

    
    ], #1e1e1e),
)
    # dbc.Tab([
    #     html.Ul([
    #         html.Br(),
    #         html.Li('Book title: Interactive Dashboards andData Apps with Plotly and Dash'),
    #         html.Li(['GitHub repo: ', html.A('https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash',href='https://github.com/PacktPublishing/Interactive-Dashboards-and-Data-Apps-with-Plotly-and-Dash')]) 
    
    # ])
    # ], label='Project Info')


 ],
 style={ "margin-left": 70, "margin-right": 70,"font-family": "Arial"})

## make animation


@app.callback(
    dash.dependencies.Output('animated-text', 'children'),
    dash.dependencies.Input('interval-component', 'n_intervals')
)
def update_animated_text(n):
    text = " YOU ARE WELCOME TO OUR DASHBOARD FOR CLIMATE EXTREME EVENTS, CONFLICTS AND INTERNAL DISPALCEMENT FORECASTING"
    return text[0:n % len(text)]

# call back to analyse conflict data
@app.callback(
    Output("graph_events", "figure"), 
    Input("dropdown_events", "value"))
def update_bar_chart(years):
    if not years:
        return {"data":[]}
    data = new_data[new_data["Date"].isin(years)]
    
    fig = px.histogram(data, x="Date", 
                        y="Total_conflicts", 
                        color='EVENT_TYPE',
                        barmode='group',
                        category_orders= {"EVENT_TYPE":['Battles', 'Protests', 'Strategic developments', 'Riots',
       'Violence against civilians', 'Explosions/Remote violence']},
       color_discrete_map={'Battles' : "red",
                           'Protests':"blue", 
                           'Strategic developments':"pink",
                            'Riots':"grey",
                            'Violence against civilians':"green", 
                            'Explosions/Remote violence':"orange"})
    return fig

# To plot the conflicts area spatialy

@app.callback(
    Output("graph", "figure"),
    Input("EVENT_TYPE", "value"),
    Input("Year", "value"))
def display_choropleth(event_type, year):
    for index, types in enumerate(event_type):
        df = simplify_merge[(simplify_merge["EVENT_TYPE"] == event_type) & (simplify_merge["Year"] == year)]

        fig = px.choropleth_mapbox(df, geojson=df.geometry, 
                        locations=df.index, 
                        color="SUM_CONFLICTS",
                        color_continuous_scale="Reds",
                        range_color=(0, None),
                        mapbox_style="carto-positron",
                        zoom=5, center = {"lat": 12.2383, "lon": -1.5616},
                        opacity=1,
                        labels={'SUM_CONFLICTS':'Sum'},
                        )
        #fig.update_geos(fitbounds="locations")
        fig.update_geos(fitbounds="locations")
        fig.update_layout(
            title = {"text" : f'Map of {event_type} for {year}',
                        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
        ),

        fig.update_yaxes(type="log")
        fig.update_layout(
            margin={"r":0,"t":30,"l":10,"b":10},
            coloraxis_colorbar={
                'title':'Annual conflict cases'})

    return fig

@app.callback(
    Output("our-graph", "figure"),
    Input("my-slider", "value"),
     prevent_initial_call=True)
def update_figure(month_range):
    start_month = month_range[0]
    end_month = month_range[1]

    # Adjust the number of steps based on the selected month range
    steps = end_month - start_month + 1

    # Generate forecasts for the selected range of months
    forecast = model_fit.get_forecast(steps=steps)
    pred_values = forecast.predicted_mean
    pred_ci = forecast.conf_int()

    # Create the figure
    fig_forecast = go.Figure()

    # Add the training data
    fig_forecast.add_trace(go.Scatter(
        x=train.index,
        y=train['Idp'],
        mode='lines',
        name='IDP Training'
    ))

    # Add the testing data
    # fig_forecast.add_trace(go.Scatter(
    #     x=test.index,
    #     y=test['Idp'],
    #     mode='lines',
    #     name='IDP Testing'
    # ))

    # Add the forecasted values
    fig_forecast.add_trace(go.Scatter(
        x=pred_values.index,
        y=pred_values,
        mode='lines',
        name='Forecast of IDP',
        line=dict(color='black')
    ))

    # Add the confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=pred_ci.index,
        y=pred_ci.iloc[:, 0],
        mode='lines',
        name='95% Lower bound of the confidence Interval',
        line=dict(color='purple')
    ))

    fig_forecast.add_trace(go.Scatter(
        x=pred_ci.index,
        y=pred_ci.iloc[:, 1],
        mode='lines',
        name='95% Upper bound of the confidence Interval',
        line=dict(color='purple')
    ))

    # Fill the area between the upper and lower bands of the confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=pred_ci.index,
        y=pred_ci.iloc[:, 1],
        mode='lines',
        name='95% Confidence Interval',
        fill='tonexty',
        fillcolor='rgba(173, 216, 230, 0.5)',  # Blue light color with transparency
        line=dict(color='purple', width=0),
        showlegend=False
    ))

    # Fill the area between the forecasted values and the lower band of the confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=pred_values.index,
        y=pred_ci.iloc[:, 0],
        mode='lines',
        name='Forecast Interval',
        fill='tonexty',
        fillcolor='rgba(173, 216, 230, 0.5)',  # Blue light color with transparency
        line=dict(color='black', width=0),
        showlegend=False
    ))

    # Update layout
    fig_forecast.update_layout(
        title='Internal Migration Forecast for 2025',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Idp'),
        legend=dict(x=0, y=1),
        showlegend=True,
        plot_bgcolor="lightyellow",
        hovermode='x',
        font=dict(family='New Time Roman'),
        title_x=0.5,
        width=1000, height=400
       
    )

    # Display the figure
    return fig_forecast



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
