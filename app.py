import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import pandas as pd

########### Define your variables
color1='darkred'
color2='orange'
mytitle='UU Radar'
tabtitle='...'
myheading='Scope Emissions and Resilience Solutions Radar'


df1 = pd.read_csv('https://storage.googleapis.com/uu_public/radar_data8.csv')

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=df1.ids,
    labels=df1.labels,
    parents=df1.parents,
    customdata=df1.descriptions,
    name='',
    domain=dict(column=0),
    hovertemplate = '<b>%{label} - %{customdata}</b><br>'
))


fig.update_layout(
    grid= dict(columns=2, rows=1),
    margin = dict(t=0, l=0, r=0, b=0),
    uniformtext = dict(minsize=10, mode='hide')
)

#fig.show()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(style={'width': '100%'}, children=[
    html.Div(style={'width': '75%', 'height':'100%', 'float': 'left' }, children=[
        html.H1(myheading),
        dcc.Graph(
            id='uu-radar',
            figure=fig
        ),
        html.A('About Scope Emissions', href='https://www.watershedclimate.com/blog/building-a-world-class-climate-program'),
        html.Br(),        
        html.A('About Urban Us', href='https://urban.us'),
        html.Br(),
        html.Br(), 
        html.Strong('Why Resilience?'),
        html.Br(), 
        'The biggest opportunities we see on the horizon are solutions for adaptation to “baked in” warming and the related weather, systems, and asset risks. This includes how we build Infrastructure so is the biggest area of investment and ROI that weighs against some of the biggest costs of innaction. ',
        ]
    ), html.Div(style={'margin-left': '25%' }, children=[
        html.Br(),
        html.H4('About this radar'),
        html.Br(),
        html.Strong('"What are the available solutions for reaching our climate goals and how can we impliment them?'), 
        html.Br(),        
        html.Br(),        
        "This is increasingly one of the most comon questions we get from industry partners and friends. We have now invested in dozens of solutions across different sides of the emissions equation, and many are either ready for wide adoption or already the Leader. We decided to build this radar as a reference but also an invitation to engage directly with these companies. And if you're a company or know a company we should invest in and list here, please let us know.",
    ]) 
])

if __name__ == '__main__':
    app.run_server()