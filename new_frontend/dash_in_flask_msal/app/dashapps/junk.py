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

# data = dict(
#     character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
#     parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
#     value=[10, 14, 12, 10, 2, 6, 6, 4, 4])
temp=pd.DataFrame(
    data={
        'binbase':['binbase' for x in range(0,7)],
        'species':['human','human','human','human','human','mouse','mouse'],
        'organ':['plasm','serum','serum','brain','lung','serum','tail'],
        'disease':['no','no','cancer','no','no','no','no'],
        'avg_intensity':[7,8,9,10,11,12,13]
    }
)

app.layout = html.Div([

    # html.Div(id="image", children=[
    #     html.Img(src="http://placeimg.com/625/225/animals", height='100', width='100')
    # ], style = {'display': 'block'}),

    # html.Div(id='modal', children=[
    #     html.Img(
    #         src="http://placeimg.com/625/225/animals",
    #         height='500',
    #         width='500',
    #         style={
    #             'display':'block',
    #             'margin-left': 'auto',
    #             'margin-right': 'auto'
    #         })
    # ], style={'display': 'none'})
    dcc.Graph(
        id='sunburst',
        figure=px.sunburst(
            # data,
            # names='character',
            # parents='parent',
            # values='value',
            data_frame=temp,
            path=['binbase','species','organ','disease'],
            values='avg_intensity'
        )
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