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
myheading='Urban Us Radar'


df1 = pd.read_csv('https://storage.googleapis.com/uu_public/radar_data4.csv')

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=df1.ids,
    labels=df1.labels,
    parents=df1.parents,
    domain=dict(column=0),
    insidetextorientation='radial'
))


fig.update_layout(
    grid= dict(columns=2, rows=1),
    margin = dict(t=0, l=0, r=0, b=0)
)

#fig.show()

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='uu-radar',
        figure=fig
    ),
    html.A('Urban Us', href='https://urban.us'),
    html.Br(),
    ]
)

if __name__ == '__main__':
    app.run_server()