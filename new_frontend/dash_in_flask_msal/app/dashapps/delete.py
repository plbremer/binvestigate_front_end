import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash()
server = app.server

app.layout = html.Div([

    html.Div(id="image", children=[
        html.Img(src="http://placeimg.com/625/225/animals", height='100', width='100')
    ], style = {'display': 'block'}),

    html.Div(id='modal', children=[
        html.Img(
            src="http://placeimg.com/625/225/animals",
            height='500',
            width='500',
            style={
                'display':'block',
                'margin-left': 'auto',
                'margin-right': 'auto'
            })
    ], style={'display': 'none'})

])

@app.callback(Output('modal', 'style'),
              [Input('image', 'n_clicks')])
def display_image(n):
    if n % 2 == 0:
        return {'display': 'none'}
    else:
        return {
            'display': 'block',
            'z-index': '1',
            'padding-top': '100',
            'left': '0',
            'top': '0',
            'width': '100%',
            'height': '100%',
            'overflow': 'auto'
            }

if __name__ == '__main__':
    app.run_server(debug=True)