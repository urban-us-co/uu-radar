"""

TODO
https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/
https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

"""


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
mytitle='Urban Us Climate Solutions Radar'
tabtitle='Urban Us Climate Solutions Radar'
myheading='Climate Solutions Radar'


df1 = pd.read_csv('https://raw.githubusercontent.com/urban-us-co/uu-radar/main/radar_data.csv')
#details = pd.read_json(url)

new_graph_data = pd.DataFrame(columns=['ids', 'labels', 'parents', 'descriptions', 'website_1', 'jobs_id'])

#df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

df_dict = df1.to_dict(orient='records')

companies_dict = dict()
companies_list = []
companies_options = []

for i in df_dict:
    companies_dict[i['labels']] = i['website_1']
    if len(i['website_1']) > 2 and i['labels'] not in companies_list:
        companies_list.append(i['labels'])
        companies_options.append({'label': i['labels'], 'value': i['labels']})

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


########### Initiate the app
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_scripts = ['//js.hs-scripts.com/1697558.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server
app.title=tabtitle


######### draw initial graph

def draw_graph(graph_data):
    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        ids=graph_data.ids,
        labels=graph_data.labels,
        parents=graph_data.parents,
        customdata=graph_data.descriptions,
        name='',
        domain=dict(column=0),
        #hovertemplate = '<b>%{label} - %{customdata}</b><br>',
        insidetextorientation='radial',
    ))


    fig.update_layout(
        grid= dict(columns=1, rows=1),
        margin = dict(t=0, l=0, r=0, b=0),
        clickmode='event+select',
        #uniformtext = dict(minsize=10, mode='hide')
    )

    return fig


########## Custom index to enable google analytics and other things
app.index_string = '''<!DOCTYPE html>
<html>
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-BCGG6BZ7VB"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-BCGG6BZ7VB');
        </script>
    <!-- End Global Google Analytics -->
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''



########### Set up dropdown

dropdown = html.Div([
    dcc.Dropdown(
        id='startup-dropdown',
        options=companies_options,
        value=[],
        multi=True,
        placeholder='You can also select startups to filter the chart...'
    ),
    html.Div(id='dd-output-container')
])


########### Set up the layout

info_card =  dbc.Row(dbc.Col([
        html.Div([
                    html.Br(),
                    html.Br(), 
                    dcc.Markdown("""
                        **How to use this chart**

                        Click on any part of the graph to get more information (shown below) and to zoom in and change the center of the graph. Click on the center of the graph to zoom back out.
                    """),
                    html.Br(), 
                    dropdown,
                    html.Br(),
                ], className=''),
        dbc.Col(id='show-data'),
    ]),
)

copy_text = dbc.Row(dbc.Col(
        html.Div([
                    
            html.A('About Scope Emissions', target='_blank', href='https://www.watershedclimate.com/blog/building-a-world-class-climate-program'),
            html.Br(),        
            html.A('About Urban Us', target='_blank', href='https://urban.us'),
            html.Br(),
            html.Br(), 
            html.Br(),
            html.H4('About this radar'),
            html.Br(),
            html.Strong('What are the available solutions for reaching our climate goals and how can we implement them?'), 
            html.Br(),        
            html.Br(),        
            "This is increasingly one of the most common questions we get from industry partners and friends. We've invested in dozens of solutions across all sides of the emissions equation, and many are either ready for wide adoption or already the market leader. We built this radar as a reference but also as an invitation to engage with these companies. And if you're a company or know a company we should invest in and list here, ",
            html.A('please let us know.', target='_blank', href='https://share.hsforms.com/1SNKBwhDaTjGHU5BAO2cFZQ10due'),
            html.Br(),        
            html.Br(),      
            html.Br(),        
            html.Br(),  
        ], className='')
    ),
)


        

           

app.layout = dbc.Container(
    [
        html.H1(myheading, style={'textAlign': 'center'}),
        html.Hr(),

        dbc.Row(
            [                
                dbc.Col(
                    dcc.Graph(
                        id='uu-radar-chart',
                    ),md=8),
                dbc.Col(info_card, md=4),
            ],
            align="center",
        ),
        dbc.Row(
            [                
                dbc.Col([
                    html.Br(),
                    html.Br(), 
                ], md=8),
            ]
        ),
        dbc.Row(
            [                
                dbc.Col(copy_text, md=8),
            ],
            align="center",
        ),
        dbc.Row(
            [                
                dbc.Col([
                    html.Br(), 
                    html.Br(),
                    html.Footer(children=[
                        "© 2021 ",
                        html.A('Urban Us.', target='_blank', href='https://urban.us/'),
                        " All Rights Reserved.",
                    ]) 
                ], md=8),
            ],
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('show-data', 'children'),
    Input('uu-radar-chart', 'clickData'))
def display_click_data(clickData):
    #print(1)
    url_text = ""
    url_link = ""
    jobs_text = ""
    jobs_link = ""
    contact_text = ""
    contact_link = ""
    if not clickData: 
        return ""
    item_id = clickData["points"][0]["id"]
    item_name = clickData["points"][0]["label"]
    item_desc = clickData["points"][0]["customdata"]
    listGroup = ""

    #print(companies_dict[item_name])
    if len(companies_dict[item_name])>2:
        url_text = companies_dict[item_name]
        url_link = companies_dict[item_name]
        jobs_text = "Jobs at "+item_name
        jobs_link = "https://jobs.urban.us/?q="+item_name
        contact_text = "Get in touch with us about "+item_name
        contact_link = "https://share.hsforms.com/1SNKBwhDaTjGHU5BAO2cFZQ10due?what_would_you_like_to_discuss_="""+item_name
        listGroup = dbc.ListGroup(
                            [
                                dbc.ListGroupItem(html.A(url_text, target='_blank', href=url_link)),
                                dbc.ListGroupItem(html.A(jobs_text, target='_blank', href=jobs_link)),
                                dbc.ListGroupItem(html.A(contact_text, target='_blank', href=contact_link)),
                            ]
                        )

    return_card = dbc.Card(
        [

        dbc.CardBody(
                    [
                        html.H4(item_name, className="card-title"),
                        html.P(item_desc,
                            className="card-text",
                        ),
                        html.Br(),
                        listGroup,
                    ]
                ),
        ],
        body=True,
    )

    #print(item_name)
    #print(clickData)

    return return_card


@app.callback(
    dash.dependencies.Output('uu-radar-chart', 'figure'),
    [dash.dependencies.Input('startup-dropdown', 'value')])
def update_graph(value):
    graph_data = df1
    if len(value) == 0:
        return draw_graph(graph_data)
    else:
        print("Reload graph data....")

    #Index(['ids', 'labels', 'parents', 'descriptions', 'website_1', 'jobs_id'], dtype='object')

    parents = []
    current_parent = ""
    #print(graph_data)
    for v in value:
        #print(v)
        parents.append(v)
        this_row_parent = ""
        this_row_parent = graph_data.loc[graph_data['ids']==v, 'parents'].item()
        #print(this_row_parent)
        this_id = ""
        while len(this_row_parent) > 1:
            this_id = graph_data.loc[graph_data['ids']==this_row_parent, 'ids'].item()
            parents.insert(0, this_id)
            this_row_parent = ""
            this_row_parent = graph_data.loc[graph_data['ids']==this_id, 'parents'].item()
            #print(str(this_row_parent))
            if str(this_row_parent) == "nan":
                this_row_parent = "" 
            this_id = ""
            #print(this_row_parent)
    #print(parents)
    new_graph_data = graph_data[graph_data["ids"].isin(parents)]
    #print(new_graph_data)

    #print(parents)

    return draw_graph(new_graph_data)
    #return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server()