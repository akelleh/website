# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from plotting import traffic_plot
import flask


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                server=server)


def update_layout():
    return html.Div(children=[
                              html.H1(children='adamkelleher.com'),

                              html.Div(children=[html.H2(children="Traffic Over Time"),]),
                              traffic_plot()
                             ]
    )


app.layout = update_layout


if __name__ == '__main__':
    app.run_server(debug=False)
