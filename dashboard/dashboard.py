# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from util import generate_table

import numpy as np
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  # ['https://www.buzzfeed.com/static-assets/solid/solid.2.10.6.css']  #

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

N = 100
df = pd.DataFrame({'$x_1$': np.random.normal(size=N), '$x_2$': np.random.normal(size=N)})

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),
    html.Div(children=[html.H1(children="Test Table"),
                       generate_table(df)])
])

if __name__ == '__main__':
    app.run_server(debug=True)