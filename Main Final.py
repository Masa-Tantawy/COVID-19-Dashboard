import pandas as pd
import os

import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import json

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
from datetime import date, datetime


df_UK = pd.read_csv(os.path.join("Data", "df_UK.csv"))
df_US=pd.read_csv(os.path.join("Data","df_US.csv"))
df_Brazil=pd.read_csv(os.path.join("Data","df_Brazil.csv"))
df_world = pd.read_csv(os.path.join("Data","df_world.csv"))
df_continents = pd.read_csv(os.path.join("Data","df_continents.csv"))

df_UK['date'] = pd.to_datetime(df_UK['date'], utc=False)
df_world['date'] = pd.to_datetime(df_world['date'], utc=False)
df_continents['date'] = pd.to_datetime(df_continents['date'], utc=False)


load_figure_template("Litera")
virus_pic= os.path.join('assets',"COVID pic.png")
uk_pic= os.path.join('assets',"UK Pic (1).png")
# df.head()
# df.tail()['date']
# df['location'].value_counts()[:20]

#Theme = 'Quartz.css'
#app = dash.Dash(__name__)
#app=dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app.title = 'DSCI Project 2'

# Stat Cards
# for ICU stat card
#df_UK["icu_patients"]=df_UK["icu_patients"].fillna(0)


#################################### STATS CARDS
daily = len(df_UK)
# for ICU stat card
#df_UK["icu_patients"]=df_UK["icu_patients"].fillna(0)
df_UK = df_UK.fillna(method='ffill')
cards = dbc.Row(
    [
        dbc.Col(dbc.Card([
            html.H5((df_UK['new_cases'][daily - 1:]).to_string(index=False),
                        className="card-title", style={'textAlign': 'center'}),
            html.P(
                "New confirmed cases of COVID-19",
                className="card-text",
                style={'textAlign': 'center'},
            ),
            ], color="info")),

        dbc.Col(dbc.Card([
            html.H5((df_UK['new_deaths'][daily - 1:]).to_string(index=False),
                        className="card-title", style={'textAlign': 'center'}),
            html.P(
                "New deaths attributed to COVID-19",
                className="card-text",
                style={'textAlign': 'center'},
            ),
            ], color="danger")),

        dbc.Col(dbc.Card([
            html.H5((df_UK["icu_patients"][daily - 1:]).to_string(index=False),
                    className="card-title", style={'textAlign': 'center'}),
            html.P(
                "COVID-19 Intensive Care Unit Admissions",
                className="card-text",
                style={'textAlign': 'center'},
            ),
        ], color="warning")),

        dbc.Col(dbc.Card(
            [
            html.H5((df_UK['new_vaccinations'][daily - 2: daily - 1]).to_string(index=False),
                        className="card-title", style={'textAlign': 'center'}),
            html.P(
                "New COVID-19 vaccination doses administered",
                className="card-text",
                style={'textAlign': 'center'},
                ),
            ], color="secondary")),
    ],
    className="mb-4",
)


fig = px.line(df_UK, x=df_UK["date"].dt.day, y="new_cases", title='New Cases in the United Kingdom',
              hover_data={"date": "|%B %d, %Y",
                          "country": df_UK['location']})
fig.update_xaxes(title='Date', dtick="M1", tickformat="%b\n%Y")
fig.update_yaxes(title='New COVID-19 Cases')


# reading the Json file
with open(os.path.join('Data','world.geo.json')) as json_file:
    geojson = json.load(json_file)

# UK
df_UK['people_fully_vaccinated'] = df_UK['people_fully_vaccinated'].fillna(method='ffill')
UK_vaccine_percentage = df_UK['people_fully_vaccinated'][df_UK.index[-1]] / df_UK['population'][df_UK.index[-1]]
UK_no_vaccine = 1 - UK_vaccine_percentage

UK_total = [['Fully Vaccinated', UK_vaccine_percentage], ['Not Fully Vaccinated', UK_no_vaccine]]

UK_smalldf = pd.DataFrame(UK_total, columns=['Type', 'Proportion'])

fig3a = px.pie(UK_smalldf, values='Proportion',
               title='United Kingdom Full Vaccination Proportion ', names='Type')

# USA
df_US['people_fully_vaccinated'] = df_US['people_fully_vaccinated'].fillna(method='ffill')
US_vaccine_percentage = df_US['people_fully_vaccinated'][df_US.index[-1]] / df_US['population'][df_US.index[-1]]
US_no_vaccine = 1 - US_vaccine_percentage

US_total = [['Fully Vaccinated', US_vaccine_percentage], ['Not Fully Vaccinated', US_no_vaccine]]

US_smalldf = pd.DataFrame(US_total, columns=['Type', 'Proportion'])

fig3b = px.pie(US_smalldf, values='Proportion',
               title='United Kingdom Full Vaccination Proportion ', names='Type')
# Brazil
df_Brazil['people_fully_vaccinated'] = df_Brazil['people_fully_vaccinated'].fillna(method='ffill')
B_vaccine_percentage = df_Brazil['people_fully_vaccinated'][df_Brazil.index[-1]] / df_Brazil['population'][
    df_Brazil.index[-1]]
B_no_vaccine = 1 - B_vaccine_percentage

B_total = [['Fully Vaccinated', B_vaccine_percentage], ['Not Fully Vaccinated', B_no_vaccine]]

B_smalldf = pd.DataFrame(B_total, columns=['Type', 'Proportion'])

fig3c = px.pie(B_smalldf, values='Proportion',
               title='United Kingdom Full Vaccination Proportion ', names='Type')


df_UK = df_UK[df_UK["new_cases"] >= 0]

fig4 = px.line(df_UK, x="total_vaccinations_per_hundred", y="new_cases",
               hover_data={"date": "|%B %d, %Y",
                           "country": df_UK['location']})

fig4.update_traces(marker=dict(size=13,
                               line=dict(width=1,
                                         color="#E05194")),
                   selector=dict(mode='markers'))

# modifying legend position and scatter plot dimensions
fig4.layout = go.Layout(
     plot_bgcolor="#FFF",  # Sets background color to white
     xaxis=dict(  # Sets color of X-axis line
         showgrid=False  # Removes X-axis grid lines
     ),
     yaxis=dict(  # Sets color of Y-axis line
         showgrid=False,  # Removes Y-axis grid lines
     )
 )

fig4.update_layout(
                    font=dict(size=16, color="black"), legend=dict(
         orientation="h",
         yanchor="bottom",
         y=1.02,
         xanchor="right",
         x=1))

# changing x-axes step, font size and assigning label
fig4.update_xaxes(tick0=0, dtick=20, zeroline=True, zerolinewidth=2, zerolinecolor="Black",
                  title_text="Vaccinations (per hundred)",
                  title_font={"size": 20},
                  title_font_family="Times New Roman",
                  title_standoff=25)

# changing y-axes font size and assigning label

fig4.update_yaxes(showline=True, linewidth=2, linecolor='black', tick0=0, dtick=100000, zeroline=True, zerolinewidth=2,
                  zerolinecolor="Black",
                  title_text="New COVID-19 Cases",
                  title_font={"size": 20},
                  title_font_family="Times New Roman",
                  title_standoff=25)
#fig4.update_traces(line_color='#E05194')



#############################     APP LAYOUT
app.layout = dbc.Container([
    # dbc.Row([html.Div(children=[
    # html.H1(
    #     children='United Kingdom Covid-19 Dashboard',
    #     style={
    #        'textAlign': 'center'
    #      })])

    #]),
    dbc.Row([html.Div(
        html.H3(children='United Kingdom Covid-19 Dashboard', style={
            'textAlign': 'center', 'color': 'white', 'fontSize': 35, 'height': '250px','width':"1350px",
            #'background-image': 'url(https://ak.picdn.net/shutterstock/videos/1035248879/thumb/1.jpg)'
            #'background-image':'url(https://thumbs.dreamstime.com/b/uk-flag-big-ben-british-union-jack-clock-tower-parliament-house-city-westminster-background-votes-to-leave-94886154.jpg)'
            'background-image':'url("/assets/UK Pic (1).png")'
    }))
    ]),

    dbc.Row([html.Div([cards])]),
    dbc.Row([
       dbc.Col([ html.Div(children = [
         html.H4(children="The daily reported COVID-19 cases over time (31 Jan 2020 - Present Day)"),

         dcc.Dropdown(id="mydropdown",
        options=[{"label": x, "value": x}
        for x in pd.unique(df_world.location)],
         value=["United Kingdom","United States","Brazil"],
         multi=True
     ),
         dcc.Graph(id='Fig1', figure={})
         ]),

       ],
           width={"size":9}),

        dbc.Col(dbc.Card([
            dbc.CardImg(src=virus_pic, top=True),
            html.H3("Did you know?", style={'textAlign': 'center'}, className="card-title"),
            html.P("The highest recorded number of reported COVID cases since the start of the pandemic around the world was",
                   style={'textAlign': 'center'}),
            html.H5("414,188 cases", style={'textAlign': 'center', 'color': 'red', 'fontSize': 18,}),
            html.P("in just one day. This was in India on the 6th of May in 2020.", style={'textAlign': 'center'})
        ], color="warning", outline=True),
            width={"size":3}, align='center')
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            html.H4('Want to know more about your country?',  style={'textAlign': 'center'}),
            html.H6('Choose where you are from to get a summary of the pandemic state there.'),

            dcc.Dropdown(id="Summary Dropdown",
                         options=[{"label": x, "value": x} for x in pd.unique(df_world.location)],
                         value="Egypt", multi=False
                         ),
            html.H6(id='Stat Date', style={'textAlign': 'center'}),
            dbc.Card([
                html.H5(id='Summary1 card', className="card-title", style={'textAlign': 'center'}),
                html.P(
                    "New confirmed cases of COVID-19",
                    className="card-text",
                    style={'textAlign': 'center'},
                ),
            ], color="info", className="mb-3"),

            dbc.Card([
                html.H5(id='Summary2 card', className="card-title", style={'textAlign': 'center'}),
                html.P(
                    "New deaths attributed to COVID-19",
                    className="card-text",
                    style={'textAlign': 'center'},
                ),
            ], color="danger",  className="mb-3"),

            dbc.Card([
                html.H5(id='Summary3 card', className="card-title", style={'textAlign': 'center'}),
                html.P("New COVID-19 vaccination doses administered", className="card-text",
                       style={'textAlign': 'center'}),
            ], color="warning",  className="mb-3")
        ], width=4),

        dbc.Col([html.Div(children=[
            html.H4(children="New COVID-19 Cases VS Vaccinations in the UK"),

            dcc.Dropdown(id="fig4dropdown",
                         options=[{"label":x,"value":x}
                         for x in pd.unique(df_world.location)],
                         value=["United Kingdom","France","Italy"],
                         multi=True
        ),
            dcc.Graph(id="Fig4",figure={}),
        ])
         ],width={"size":8})

              ], className="mb-24"),
    dbc.Row([
        dbc.Col([html.Div(children=[
         html.H4('Proportions of Full Vaccinations for each Country'),
            dbc.Row([
    dbc.Col([
        dcc.Dropdown(id="f3dropdown1",
                         options=[{"label": x, "value": x}
                                     for x in pd.unique(df_world.location)],
                         value="United Kingdom",multi=False),
        html.H6(id= '3a country', style={'textAlign': 'center'}),
        dcc.Graph(id='Fig3a', figure={})
    ],
    width= 4),
    dbc.Col([
       dcc.Dropdown(id="f3dropdown2",
                         options=[{"label": x, "value": x}
                                     for x in pd.unique(df_world.location)],
                         value="United States", multi= False),
        html.H6(id= '3b country', style={'textAlign': 'center'}),
        dcc.Graph(id='Fig3b', figure={})
    ],
    width= 4),
    dbc.Col([
        dbc.Row([dcc.Dropdown(id="f3dropdown3",
                         options=[{"label": x, "value": x}
                                     for x in pd.unique(df_world.location)],
                         value="Brazil", multi= False)]),
        dbc.Row([
            html.H6(id= '3c country', style={'textAlign': 'center'}),
            dcc.Graph(id='Fig3c', figure={})])
    ],
    width= 4),

])

        ],)#,width={"size":6})
    ])]),

    dbc.Row([
        dbc.Col(width= 4 ),
        dbc.Col(html.H3("Have a look at the entire world!", style= {'color': 'blue', 'fontSize': 22}),
                width= 7)#style={'height': 'px'})
    ], align="center"),


   dbc.Row([
        dbc.Col([html.Div(children=[
            html.H4("Covid-19 Heatmap"),
            html.H6("New Cases Per Day Around the World"),

            dcc.DatePickerSingle(id="date-picker-single",
                                 min_date_allowed=date(2020, 2, 24),
                                 max_date_allowed=df_world.date.iloc[-1],
                                 date= datetime.date(df_world.date.iloc[-1]),
                                 display_format='MMM Do, YY', ),
            html.H6(id='Printed Date'),
            html.P("Kindly note that countries coloured in white have no data available."),
            dcc.Graph(id='Fig2'),

        ])], width={"size": 6}),

        dbc.Col([html.Div(children=[
             html.H4("How is the pandemic going around the world?",style={'textAlign': 'center'}, className="mb-5"),
            dcc.Checklist(id="fig5 checklist",
                          options=[{"label":x,"value":x} for x in pd.unique(df_continents.location)],
                          value=["Africa"],
                          labelStyle = {'display': 'inline-block', 'cursor': 'pointer', 'margin-left':'20px'}, className="mb-4"
            ),

            dcc.Graph(id="Fig5",figure={}),
         ])
        ],width={"size":6}),
    ])
    ])

################################################## CALLBACK FUNCTIONS

######### Figure 1 callback
@app.callback(
    Output("Fig1", "figure"),
    [Input("mydropdown", "value")])

def update_fig(value):
    df_subset = df_world.loc[df_world["location"].isin(value)]

    fig1 = px.line(df_subset, x=df_subset["date"].dt.day, y="new_cases", color='location',
                  range_y=[0, df_subset['new_cases'].max()], range_x= [df_subset.date.iloc[0], df_subset.date.iloc[-1]],
                  animation_frame=df_subset['date'].dt.strftime("%b-%Y"), animation_group='location')
    #fig.update_xaxes(title='Date', dtick="M1", tickformat="%b\n%Y")
    fig1.update_xaxes(title='Date', range=[1, 30], dtick="M1")
    fig1.update_yaxes(title='New COVID-19 Cases')
    return fig1

######### Figure 2 callback
@app.callback(
    [Output('Fig2', 'figure')],
    [Output('Printed Date', 'children')],
    [Input('date-picker-single', 'date')])

def map_covid(date_value):
    # Selecting data only for the specified date
    filtered_df = df_world[df_world.date == date_value]
    fig2 = px.choropleth_mapbox(filtered_df,color='new_cases', geojson=geojson, locations='iso_code', featureidkey='properties.iso_a3',
                                center={'lat': 40.52, 'lon': 34.34}, zoom=0 , mapbox_style='carto-positron',
                                range_color=(0, filtered_df['new_cases'].max()), color_continuous_midpoint= 40000,
                                hover_data= {'location':True, 'new_cases':True, 'iso_code': False, 'new_deaths':True})
    #date_value = datetime.date(date_value)

    return (fig2,'Selected Date: {}'.format(date_value))

######### Figure 3 callback
## 3a
@app.callback(
    [Output("Fig3a", "figure")],
    [Output('3a country', 'children')],
    [Input("f3dropdown1", "value")])
def proportion_pie(value):
    df_subvaccine = df_world[df_world["location"] == value]
    df_subvaccine['people_fully_vaccinated'] = df_subvaccine['people_fully_vaccinated'].fillna(method='ffill')
    vaccine_percentage = df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]
    no_vaccine = 1 - df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]

    total = [['Fully Vaccinated', vaccine_percentage], ['Not Fully Vaccinated', no_vaccine]]
    smalldf = pd.DataFrame(total, columns=['Type', 'Proportion'])
    fig3a = px.pie(smalldf, values='Proportion', names="Type")
    return (fig3a, 'Vaccinations in {}'.format(value))
##3b
@app.callback(
    [Output("Fig3b", "figure")],
    [Output('3b country', 'children')],
    [Input("f3dropdown2", "value")])
def proportion_pie(value):
    df_subvaccine = df_world[df_world["location"] == value]
    df_subvaccine['people_fully_vaccinated'] = df_subvaccine['people_fully_vaccinated'].fillna(method='ffill')
    vaccine_percentage = df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]
    no_vaccine = 1 - df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]


    total = [['Fully Vaccinated', vaccine_percentage], ['Not Fully Vaccinated', no_vaccine]]
    smalldf = pd.DataFrame(total, columns=['Type', 'Proportion'])
    fig3b = px.pie(smalldf, values='Proportion', names='Type')
    return (fig3b, 'Vaccinations in {}'.format(value))
##3c
@app.callback(
    Output("Fig3c", "figure"),
    [Output('3c country', 'children')],
    [Input("f3dropdown3", "value")])
def proportion_pie(value):
    df_subvaccine = df_world[df_world["location"] == value]
    df_subvaccine['people_fully_vaccinated'] = df_subvaccine['people_fully_vaccinated'].fillna(method='ffill')
    vaccine_percentage = df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]
    no_vaccine = 1 - df_subvaccine['people_fully_vaccinated'][df_subvaccine.index[-1]] / df_subvaccine['population'][df_subvaccine.index[-1]]


    total = [['Fully Vaccinated', vaccine_percentage], ['Not Fully Vaccinated', no_vaccine]]
    smalldf = pd.DataFrame(total, columns=['Type', 'Proportion'])
    fig3c = px.pie(smalldf, values='Proportion', names='Type')
    return (fig3c, 'Vaccinations in {}'.format(value))

######### Figure 4 callback
@app.callback(
    Output("Fig4","figure"),
    [Input("fig4dropdown", "value")])
def fig4_update(value):
    df_subset=df_world.loc[df_world["location"].isin(value)]
    df_subset = df_subset[df_subset["new_cases"] >= 0]

    fig4 = px.line(df_subset, x="total_vaccinations_per_hundred", y="new_cases",color="location",
                   hover_data={"date": "|%B %d, %Y",
                               "country": df_subset['location']})
    fig4.update_layout(
        font=dict(size=14, color="black"), legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1))
    # changing x-axes step, font size and assigning labels
    fig4.update_xaxes(title_text="Vaccinations (per hundred)")

    # changing y-axes font size and assigning label
    fig4.update_yaxes(title_text="New COVID-19 Cases")

    return fig4

########### Figure 5 callback
@app.callback(
    Output("Fig5","figure"),
    [Input("fig5 checklist", "value")])

def fig5_update(value):
    df_subset = df_continents.loc[df_continents["location"].isin(value)]
    df_subset = df_subset[df_subset["new_cases"] >= 0]

    fig5 = px.area(df_subset, x="date", y="new_cases", color="location", title="New Cases in each continent")
    fig5.update_xaxes(title='Date', dtick="M1", tickformat="%b\n%Y")
    fig5.update_yaxes(title='New COVID-19 Cases')
    fig5.update_layout(hovermode="x unified")
    return fig5

###### Summary stat cards callback
@app.callback(
    [Output('Summary1 card', 'children')],
    [Output('Summary2 card', 'children')],
    [Output('Summary3 card', 'children')],
    [Output('Stat Date', 'children')],
    Input('Summary Dropdown', 'value')
)
def stat_cards_update(value):
    df_subset = df_world[df_world["location"] == value]
    daily= len(df_subset)
    df_subset = df_subset.fillna(method='ffill')
    num1= (df_subset['new_cases'][daily - 1:]).to_string(index=False)
    num2= (df_subset['new_deaths'][daily - 1:]).to_string(index=False)
    num3= (df_subset['new_vaccinations'][daily - 1:]).to_string(index=False)
    date= (df_subset['date'][daily - 1:]).to_string(index=False)
    return (num1, num2, num3, date)






if __name__ == "__main__":
    app.run_server(debug=False,use_reloader=True)

