import dash_bootstrap_components as dbc
from dash import html
from data_prep import *
from filter_option import *


filter_aside = html.Div(className="", children=[
    
    html.Div(className="", children=[
        html.P("Select year"),
            dbc.Select(
                id="years",
                options=[
                    {"label": year, "value": year} for year in ["All years"] + ["2015", "2016", "2017", "2018"]
                ],
                value="All years"
            )
        ]),
                        
        html.Div(className="mt-4", children=[
            html.P("Segment"),
            dbc.Select(
                id="segment",
                options=[
                    {"label": segment, "value": segment}
                    for segment in ["All segments"] + list(df.Segment.unique())
                ],
                value="All segments"
            )
        ]),
        
        html.Div(className="mt-4", children=[
            html.P("Mode"),
            dbc.Select(
                id="mode",
                options=[
                    {"label": mode, "value": mode}
                    for mode in ["All modes"] + list(df["Mode"].unique())
                ],
                value="All modes"
            )
        ]),
        
        html.Div(className="mt-4", children=[
            html.P("Orders/Sales"),
            dbc.Select(
                id="ships",
                options=[
                    {"label": ship, "value": ship}
                    for ship in ["Orders", "Sales"]
                ],
                value="Orders"
            )
        ])
    
])