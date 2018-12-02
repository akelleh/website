from util import get_client
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


def traffic_plot():
    client = get_client()
    pageview_ts_df = client.get_pageview_ts()
    uv_ts_df = client.get_uv_ts()
    
    return dcc.Graph(
        id='Traffic',
        figure={
            'data': [go.Scatter(
                                {
                                 'x': pageview_ts_df.t,
                                 'y': pageview_ts_df.pageviews,
                                 'mode': 'lines',
                                 'name': 'Pageviews'
                                 }
                                ),
                     go.Scatter(
                                {
                                 'x': uv_ts_df.t,
                                 'y': uv_ts_df.uvs,
                                 'mode': 'lines',
                                 'name': 'Unique Visitors'
                                 }
                                ),
                     ],
            'layout': {
                        'title': 'Traffic Over Time'
                      }
        }
    )
