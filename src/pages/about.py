import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify



app_name = "About"

dash.register_page(__name__, path=f"/{app_name}", title=app_name, description=app_name, name=app_name)

layout = html.Div(id=app_name, className="container-fluid container-md bg-white p-1 p-md-5", children=[
    
    dmc.Anchor(
        [DashIconify(icon="eva:arrow-back-fill", width=30),
         " Back to the dashboard"],
        href="/",
    ),
        
    html.H1(className="d-flex align-items-center fw-bold display-1 mt-2", children=[
        html.Span("About Analytics",),
        html.Span("Paper", style={'color': 'red'}),
    ]),
    
    
    html.Div(className="row align-items-center mt-4", children=[
        html.Div(className="col-lg-8", children=[
            
            html.Div(className="app_name", children=[
                html.H4("Welcome and Introduction:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    Welcome to my Data Analytics application! This platform is designed to provide interactive insights into various datasets using a combination of Dash, Plotly, Matplotlib, Seaborn and a plethora of other technologies
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Tech stack:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    * Dash, Flask, and Django: for creating an interactive and dynamic user interface.
                    
                    * Matplotlib, Seaborn, Plotly: These libraries to create engaging and informative visualizations, offering a deep understanding of the data.
                    
                    * Pydeck, Folium, Basemap, plotly: For precise geospatial analysis and map visualization
                                        
                    * Pandas, NumPy, SciPy, Xarray: for efficient data processing, scientific computation, and manipulation of multidimensional arrays
                    
                    * TensorFlow, scikit-learn: For machine learning capabilities, predictive models and analyze trends
                    
                    * Scrapy, BeautifulSoup, Splash, Selenium: for data scraping
                    
                    
                    **Note**: *In this case, for this project, we only used Dash for the application and Plotly for the charts*
                    """
                )
            ]),
            
            
            html.Div(className="mt-4", children=[
                html.H4("Contact:", className="mb-3 fw-bold"),
                dcc.Markdown(
                    """ 
                    I invite you to connect with me on [LinkedIn](https://www.linkedin.com/in/chris-baudelaire-k-8284731a1/). For any inquiries, suggestions, or collaboration opportunities, please feel free to get in touch. I am open to discussions and look forward to hearing from you
                    
                    
                    Let's stay connected and build something great together!
                    """
                )
            ])
    
        ]),
        
        html.Div(className="col-lg-4", children=[
            
            html.Div(className="mt-4 text-center", children=[
                html.H4("About author:", className="mb-3 fw-bold"),
                html.P("Chris Baudelaire KOUDOU", className="fw-bold"),
                dcc.Markdown(
                    """ 
                    As a student immersed in the world of pure and Applied Mathematics, this application is more than just a project—it's a living manifestation of my passion for data science, analytics, and visualizations. Crafted at the intersection of mathematical rigor and technological innovation, this web application is an endeavor to transform theoretical concepts into dynamic, real-world solutions
                    
                    
                    #### Additional Dashboards:
                    
                    ...
                    
                    """
                )
            ]),   

            
        ]),
    ])
    
])

