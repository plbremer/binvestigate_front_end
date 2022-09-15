import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from pprint import pprint

local_stylesheet = {
    "href": "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap",
    "rel": "stylesheet"
}

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[local_stylesheet, dbc.themes.BOOTSTRAP])

app.layout = html.Div([
        # this stuff appears on every page
        # we should have some logo stuff
        # and then some stuff that handles links (probably the top button navbar thing)
        #html.Div("Python Multipage App with Dash", style={'fontSize':50, 'textAlign':'center'}),


        dbc.Navbar(
            #,#+
            #[dbc.Container() for i in range(10)]+
            dbc.Container(
                children=[
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row([
                            dbc.Col(html.Img(src='https://avatars.githubusercontent.com/u/45467465?s=200&v=4', height="50px")),
                            dbc.Col(dbc.NavbarBrand(id="header", children="Binvestigate, a FiehnLab Production")),#, className="ms-2")),
                            ], 
                            align="center", #className="g-0",
                        ),
                        href="https://fiehnlab.ucdavis.edu/",
                        style={"textDecoration": "none"},
                    )
                ]+[dbc.NavItem(dbc.NavLink(page['name'], href=page['path'])) for page in dash.page_registry.values()],
                
                style={"height": "50px"}, 
            ), 
            color="dark", 
            dark=True,
            #links_left=True
        ),

        html.Hr(),



        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)