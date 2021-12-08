from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
from dash import callback_context

# Connect to main app.py file
from app import app
#from app import server
from apps import compound
from apps import species
from apps import organ
from apps import disease
from apps import additional_filters
from apps import result
# from apps import visualizations



app.layout = html.Div(
    [
        #storage_type='session',
        # '''
        dcc.Store(id='store_compound'),

        dcc.Store(id='store_from_species'),
        dcc.Store(id='store_to_species'),

        dcc.Store(id='store_from_organ'),
        dcc.Store(id='store_to_organ'),


        dcc.Store(id='store_from_disease'),
        dcc.Store(id='store_to_disease'),

        dcc.Store(id='store_additional'),

        # dcc.Store(id='store_aggregate'),
        # '''
        dbc.Row(
            #for the moment, we put all in one column
            #but maybe later put in separate columns
            #just put one of each link into a different column
            dbc.Col(
                html.Div(
                    children=[
                        dcc.Location(id='url',pathname='',refresh=False),
                        dcc.Link('Compound | ',href='/apps/compound'),
                        dcc.Link('Species | ',href='/apps/species'),
                        dcc.Link('Organ | ',href='/apps/organ'),
                        dcc.Link('Disease | ',href='/apps/disease'),
                        dcc.Link('Additional Filters | ',href='/apps/additional_filters'),
                        dcc.Link('Results | ',href='/apps/results'),
                        dcc.Link('Visualizations',href='/apps/visualizations')
                    ]
                ),
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='page_content',
                    children=[]
                )
            )
        )
    ]
)




@app.callback(
    [Output(component_id='page_content',component_property='children')],
    [Input(component_id='url',component_property='pathname')]
)
def display_page(temp_pathname):
    if temp_pathname == '/apps/compound':
        return [compound.layout]
    elif temp_pathname == '/apps/species':
        return [species.layout]
    elif temp_pathname == '/apps/organ':
        return [organ.layout]
    elif temp_pathname == '/apps/disease':
        return [disease.layout]
    elif temp_pathname == '/apps/additional_filters':
        return [additional_filters.layout]
    elif temp_pathname == '/apps/results':
        return [results.layout]
    elif temp_pathname == '/apps/visualizations':
        return [visualizations.layout]
    else:
        return 'under construction'


if __name__ == '__main__':
    app.run_server(debug=True)