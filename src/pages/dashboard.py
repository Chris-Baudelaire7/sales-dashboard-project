import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc

from filter_option import *
from callbacks import *


app_name = "sales-dashboard-analysis"

dash.register_page(__name__, path=f"/", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container", children=[    
        
    html.Div(className="row align-items-center", children=[
        
        html.Div(className="col-lg-4", children=[
            
            html.Div(className="card shadow-box", children=[filter_aside])
            
        ]),
        
        html.Div(className="col-lg-4 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5(id="area-title", className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="State", id="area", children=[
                        dmc.Chip(x, value=x) for x in ["Region", "State", "City"]
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="area-graph", config=dict(displayModeBar=False))),
                                
            ]),
        ]),
        
        html.Div(className="col-lg-4 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5(id="(sub)category-title", className="text-center mt-3 mb-1"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="Category", id="category", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Category", "Sub-Category"], ["Category", "Sub-Category"])
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="sales-by-cat", config=dict(displayModeBar=False))),                
                
            ]),
        ]),
        
    ]),
    
    
    html.Div(className="row align-items-center mt-3 mt-lg-5", children=[
        
        html.Div(className="col-lg-8 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Monthly sales rate", className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="Category", id="repartition-type", children=[
                        dmc.Chip(x, value=x) 
                        for x in ["Mode", "Segment", "Category"]
                    ]),
                    
                ]),
                
                dcc.Graph(id="proportion", config=dict(displayModeBar=False)),
                
                html.Div(className="selection d-flex justify-content-center mt-3", children=[
                    
                    dmc.ChipGroup(value="Year", id="repartition-type2", children=[
                        dmc.Chip(x, value=x) for x in ["Year", "Month", "Region"]
                    ]),
                ]),
                
            ]),
        ]),
        
        html.Div(className="col-lg-4", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Distribution by category",className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="pie", id="repartition-graph", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Pie chart", "Bar chart"], ["pie", "bar"])
                    ]),
                ]),
                
                dcc.Graph(id="repartition", config=dict(displayModeBar=False))
            ]),
        ]),
        
    ]),
    
    
    
    html.Div(className="row align-items-center mt-3 mt-lg-5", children=[
        
        html.Div(className="col-lg-4", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Top products", className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="Winter", id="season", children=[
                        dmc.Chip(x, value=x, size="xs") for x in list(df.Season.unique()) + ["All"]
                    ]),
                ]),
                   
                dcc.Graph(id="product", config=dict(displayModeBar=False))
            ]),
        ]),
        
        html.Div(className="col-lg-4", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Top Customer", className="text-center mt-3"),
                dcc.Graph(id="client", config=dict(displayModeBar=False))
            ]),
        ]),
        
        html.Div(className="col-lg-4 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5(id="year-season-title",
                        className="text-center mt-3"),

                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="Year", id="ys", children=[
                        dmc.Chip(x, value=x) for x in ["Year", "Season"]
                    ]),
                ]),

                dcc.Loading(dcc.Graph(id="year-season", config=dict(displayModeBar=False))),

            ])
        ]),
        
    ]),
    
    
    
    html.Div(id="div-map", className="row align-items-center mt-3 mt-lg-5", children=[
        
        html.Div(className="col-lg-8 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box div-map", children=[
                html.H5(id="map-title",className="text-center mt-3"),
                dcc.Graph(id="mapbox", config=dict(displayModeBar=False)),
            ])
        ]),
        
        html.Div(className="col-lg-4 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box div-map", children=[
                html.H5(id="title-city-rank", className="text-center mt-3"),
                html.I("Hover over the map to update the cities", className="text-center my-1"),
                dcc.Graph(id="fig-city", config=dict(displayModeBar=False))
            ])
        ])

        
    ]),
    
    
    html.Div(className="row align-items-center mt-3 mt-lg-5", children=[
        
        html.Div(className="col-lg-7", children=[
            html.Div(className="card shadow-box", children=[
                html.H5(id="Daily-evolution-title", className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="scatter", id="graph", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Line chart", "Bar chart"], ["scatter", "bar"])
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="timeseries-by-day", config=dict(displayModeBar=False)))            
                
            ]),
        ]),
        
        html.Div(className="col-lg-5 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5(id="evolution-by-month-title", className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="line_scatter", id="type_chart", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Bar chart", "Line + scatter"], ["bar", "line_scatter"])
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="timeseries", config=dict(displayModeBar=False)))
                    
            ]),
        ]),
    ]),
    
    
    
    html.Div(className="row align-items-center mt-3 mt-lg-5", children=[
        
        html.Div(className="col-lg-5 mt-3 mt-lg-0", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Sales based on delivery duration",className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="sum", id="solde", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Average sales balance", "Total sales balance"], ["mean", "sum"])
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="pie-duration", config=dict(displayModeBar=False))),    
                    
            ]),
        ]),
        
        html.Div(className="col-lg-7", children=[
            html.Div(className="card shadow-box", children=[
                html.H5("Monthly evolution of average shipping duration",
                        className="text-center mt-3"),
                
                html.Div(className="selection d-flex justify-content-center mb-3", children=[
                    dmc.ChipGroup(value="scatter", id="graph-duration", children=[
                        dmc.Chip(x, value=y) for x, y in zip(["Area chart", "Bar chart"], ["scatter", "bar"])
                    ]),
                ]),
                
                dcc.Loading(dcc.Graph(id="timeseries-duration", config=dict(displayModeBar=False)))            
                
            ])
        ])
    ]),
    
    
    html.Div(className="mt-5 pt-5")
  
])

