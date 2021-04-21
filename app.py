import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

import json
import pandas as pd

########### Define your variables
color1='darkred'
color2='orange'
mytitle='UU Radar'
tabtitle='...'
myheading='Scope Emissions and Resilience Solutions Radar'


df1 = pd.read_csv('https://raw.githubusercontent.com/urban-us-co/uu-radar/main/radar_data.csv')
#details = pd.read_json(url)

#df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
print(df1)
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=df1.ids,
    labels=df1.labels,
    parents=df1.parents,
    customdata=df1.descriptions,
    name='',
    domain=dict(column=0),
    #hovertemplate = '<b>%{label} - %{customdata}</b><br>',
    insidetextorientation='radial'

))


fig.update_layout(
    grid= dict(columns=1, rows=1),
    margin = dict(t=0, l=0, r=0, b=0),
    clickmode='event+select',
    #uniformtext = dict(minsize=10, mode='hide')
)

#fig.show()

########### Initiate the app
#external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout


app.layout = html.Div(style={}, children=[
    html.Div(style={'width': '75%', 'height':'100%', 'float': 'left' }, children=[
        html.H2(myheading, style={'textAlign': 'center'}),
        dcc.Graph(
            id='uu-radar-chart',
            figure=fig
        ),
        html.A('About Scope Emissions', href='https://www.watershedclimate.com/blog/building-a-world-class-climate-program'),
        html.Br(),        
        html.A('About Urban Us', href='https://urban.us'),
        html.Br(),
        html.Br(), 
        html.Br(),
        html.H4('About this radar'),
        html.Br(),
        html.Strong('"What are the available solutions for reaching our climate goals and how can we impliment them?'), 
        html.Br(),        
        html.Br(),        
        "This is increasingly one of the most comon questions we get from industry partners and friends. We have now invested in dozens of solutions across different sides of the emissions equation, and many are either ready for wide adoption or already the Leader. We decided to build this radar as a reference but also an invitation to engage directly with these companies. And if you're a company or know a company we should invest in and list here, please let us know.",
        html.Br(),        
        html.Br(),      
        html.Strong('Why Resilience?'),
        html.Br(), 
        'The biggest opportunities we see on the horizon are solutions for adaptation to “baked in” warming and the related weather, systems, and asset risks. This includes how we build Infrastructure so is the biggest area of investment and ROI that weighs against some of the biggest costs of innaction. ',
        ]
    ), html.Div(children=[
            html.Div([
                    html.Br(),
                    html.Br(), 
                    dcc.Markdown("""
                        **How to use this chart**

                        Click on any part of the graph to get more information (shown here) and to zoom in and change the center of the graph. Click on the center of the graph to zoom back out.
                    """),
                    html.Br(), 
                    dcc.Markdown(id='show-data'),
                ], className='')
        
    ]) 
])

@app.callback(
    Output('show-data', 'children'),
    Input('uu-radar-chart', 'clickData'))
def display_click_data(clickData):
    print(clickData)
    print(1)
    return """ 



            ### """+clickData["points"][0]["label"]+"""

            """+clickData["points"][0]["customdata"]+"""
    """



if __name__ == '__main__':
    app.run_server()