import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

from pprint import pprint

app = dash.Dash()
server = app.server

labels=['binvestigate','human','rat','plasma','lung','plasma','no','no','no']
ids=['binvestigate','human','rat','human-plasma','human-lung','rat-plasma','human-plasma-no','human-lung-no','rat-plasma-no']
parents=['','binvestigate','binvestigate','human','human','rat','human-plasma','human-lung','rat-plasma']
values=[1 for i in range(len(labels))]
values=[3,2,1,1,1,1,1,1,1]

app.layout = html.Div([

    dcc.Graph(
        id='sunburst',
        figure =go.Figure(go.Sunburst(
            # labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
            # parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
            # values=[10, 14, 12, 10, 2, 6, 6, 4, 4],
            labels=labels,
            parents=parents,
            values=values,
            branchvalues='total',
            ids=ids

        ))
    ),
    html.H6(
        id='h6',
    )
])


@app.callback(
    [Output('h6','n_clicks')],
    [Input('sunburst','clickData')],
    [State('sunburst','figure')]
)
def test(click_data,sunburst_figure):
    print('-------------------------------------')
    print(click_data)

    #pprint(sunburst_figure)
    return [3]
# @app.callback(Output('modal', 'style'),
#               [Input('image', 'n_clicks')])
# def display_image(n):
#     if n % 2 == 0:
#         return {'display': 'none'}
#     else:
#         return {
#             'display': 'block',
#             'z-index': '1',
#             'padding-top': '100',
#             'left': '0',
#             'top': '0',
#             'width': '100%',
#             'height': '100%',
#             'overflow': 'auto'
#             }



if __name__ == '__main__':
    app.run_server(debug=True)