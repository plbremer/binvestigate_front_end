

import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

#df = px.data.gapminder()

layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=3),
                dbc.Col(
                    children=[
                        html.H3('In the past decade, the field of metabolomics has transformed from an obscure specialty into a major “-omics” platform for studying metabolic processes and biomolecular characterization. However, as a whole the field is still very fractured, as the nature of the instrumentation and of the information produced by the platform essentially creates incompatible “islands” of datasets. This lack of data coherency results in the inability to accumulate a critical mass of metabolomics data that has enabled other –omics platforms to make impactful discoveries and meaningful advances.\n-Titus Mak'),
                        html.Br(),
                        html.Br(),
                        html.H3('Here is a webapp that enables the exploration of A database query interface across 160,000 metabolomic samples in GC-TOF mass spectrometryon a 160,000-sample dataset from the UC Davis/West Coast Metabolomics Center. We enable common techniques such as venn, sunburst, and differential diagrams.'),
                        html.Br(),
                        html.Br(),
                        html.H3('We also enable “ontologically-grouped differential analysis”. The user only needs to express a comparison query involving groups (e.g., “Human Gut” vs. “Bacterial Cells”) and they will receive tabular and visual results that describe the trends coming from all of the studies involving those sample metadata. This is made possible by using ontologies to transform generic terms like “Bacterial” into sets of species for which we have data.')
                    ],
                    width=6
                ),
                dbc.Col(width=3)
            ]
        )
    ]
)