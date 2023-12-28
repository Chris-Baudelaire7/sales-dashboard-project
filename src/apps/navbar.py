from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


navbar = html.Div(className="header container-fluid p-2", children=[
   html.Div(className="d-flex flex-column flex-lg-row align-items-center justify-content-center justify-content-md-between", children=[
       html.Div(className="d-flex flex-column flex-lg-row align-items-center", children=[
            html.Div(className="d-flex flex-column flex-md-row align-items-center justify-content-center", children=[
            
                html.Div(className="text-center", children=[
                    dbc.NavbarBrand(className="title", href="/", children=[
                        html.H1(className="d-flex align-items-center", children=[
                            html.Span("Analytics", className="text-white"),
                            html.Span("Paper", style={'color': 'red'}),
                            
                        ]),
                    ])
                ])
            ]),
        
        html.Div(className="ms ms-lg-2", children=[
            html.H1(" - Sales Analysis Dashboard", className="title-header text-lg-center"),
        ]),
     ]),
       
       html.Div(className="", children=[
            dbc.Nav(className="ms-auto d-flex flex-row align-items-center justify-content-center", navbar=True, children=[
                dmc.Tooltip(label="About AnalyticsPaper", position="bottom", className="tooltipp", children=[
                    dbc.Button(href="/About", className="btn", children=[
                        DashIconify(icon="flat-color-icons:about", width=30), " About the application"
                    ]),          
                ]),
                
                dmc.Tooltip(label="Source code", position="bottom", className="ms-3 tooltipp", children=[
                    dbc.Button(href="https://github.com/Chris-Baudelaire7/dashboard-vente", className="btn", children=[
                        DashIconify(icon="radix-icons:github-logo", width=30), " See on github"
                    ]),          
                ]),
                
            ])
       ])
   ])
])