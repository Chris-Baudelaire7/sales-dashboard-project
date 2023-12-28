import pandas as pd 
import datetime as dt
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash import Output, Input, callback, html, dcc
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess
from data_prep import df

from utils import *


colors = ["firebrick", "green", "royalblue"]


def filter_data(df, year, segment, mode):
    data = (df.copy())[df["Year"] == int(year)] if year in ["2015", "2016", "2017", "2018"] else df.copy()
    data = data[data["Segment"] == segment] if segment in list(df.Segment.unique()) else data.copy()
    data = data[data["Mode"] == mode] if mode in list(df.Mode.unique()) else data.copy()
    return data


@callback(
    Output("notifications-container", "children"),
    Input("ships", 'value'),
    prevent_initial_call=True,
)
def show(value):
    if value == "Sales":
        x = df[value].sum()
        unit = "$"
    else:
        x = len(df)
        unit = ""
    
    return dmc.Notification(
        title=f"{value}",
        id="simple-notify",
        action="show",
        autoClose=10000,
        icon=DashIconify(icon="ic:round-celebration"),
        message=html.Div(className="",children=[
            html.H4(f"Total {value}: {unit}{round(x, 2)}", style={"font-family": "serif"})
        ])
    )


@callback(
    Output('area-title', 'children'),
    Output('year-season-title', 'children'),
    Output('Daily-evolution-title', 'children'),
    Output('(sub)category-title', 'children'),
    Output('map-title', 'children'),
    Output('evolution-by-month-title', 'children'),
    Input("ships", 'value'),
    Input("category", 'value'),
)
def render_title(metric, cat): 
    
    def get_title(metric):
        if metric == "Sales":
            return "Sales by area", "Total sales by", "Daily evolution of total sales amount", \
                   f"Sales by {cat}", "Sales by state", "Total sales by month"
        else:
            return "Orders by area", "Total Orders", "Daily evolution of total Orders", \
                   f"Order by {cat}", "Orders by state", "Total orders by month"

    area_title, year_season_title, daily_evolution_title, category_title, map_title, month_ev_title = get_title(metric)
    
    return area_title, year_season_title, daily_evolution_title, category_title, map_title,month_ev_title



@callback(
    Output('timeseries', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
    Input("type_chart", 'value'),
)
def sales_recorded_func(year, segment, mode, ship, graph):
    data = filter_data(df, year, segment, mode)
    
    if ship == "Sales":
        col = "Sales"
        color = "firebrick"
        data = data.groupby("Month", as_index=False)[col].sum()
    else:
        col = "size"
        color="green"
        data = data.groupby("Month", as_index=False).size()
        
    data['Month'] = pd.Categorical(data['Month'], categories=month_order, ordered=True)
    data = data.sort_values('Month')

        
    fig = go.Figure()
    
    if graph == "bar":
        fig.add_bar(
            x=data["Month"],  y=data[col],
            name="Sales",
            marker_color=color,
            text=data[col], textposition="outside",
            texttemplate="%{text:.3s}", textfont=dict(size=15)
        )
    
    else:
        fig.add_scatter(
            x=data["Month"],  y=data[col],
            name="Sales", mode="lines+markers+text",
            text=data[col], textposition="top center",
            marker=dict(size=10),
            texttemplate="%{text:.3s}",
            marker_color=color, textfont=dict(size=15)
        )

    fig.update_layout(
        **update_layout_fig,
        height=300,
        margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
        yaxis=dict(visible=False),
        hovermode="x",
        xaxis=dict(color="black", title="Month"),
        font=dict(family="serif")
    )

    return fig



@callback(
    Output('year-season', 'figure'),
    Input("ships", 'value'),
    Input("ys", 'value'),
)
def update_graph_year_season(ship, ys):
    col = None
    data = df.copy()
    
    if ship == "Sales":
        col = "Sales"
        data = df.groupby(ys, as_index=False)[col].sum()
    else:
        col = "size"
        data = data.groupby(ys, as_index=False).size()
    
    fig = go.Figure()
    
    fig.add_bar(
        y=data[ys], x=data[col],
        orientation="h", marker_color="royalblue",
        text=data[col], 
        texttemplate="%{text:.2s}",
        hoverinfo="text", 
    )

    fig. update_layout(
        height=255,
        template="simple_white",
        hovermode="y",
        margin=dict(autoexpand=True, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="serif"),
        yaxis=dict(
            categoryorder='total ascending',
            title="Years",
            ticklen=6,
            tickfont=dict(family="serif", color="black", size=13),
        ),
        xaxis=dict(showgrid=True)
    )
    
    return fig



@callback(
    Output('sales-by-cat', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
    Input("category", 'value'),
)
def sales_by_category(year, segment, mode, ship, category):
    data = filter_data(df, year, segment, mode)
    
    if ship == "Sales":
        col = "Sales"
        data = data.groupby(category, as_index=False)[col].sum()
    else:
        col = "size"
        data = data.groupby(category, as_index=False).size()
    
    data = round(data, 2)
    
    if category == "Category":
        fig = go.Figure(
            go.Pie(
                labels=list(data[category]),
                values=list(data[col]),
                marker=dict(colors=colors),
                hoverinfo="label+value+percent",
                textinfo="label+value",
                texttemplate="%{label}<br>$%{value:,.2f}", 
                textposition="outside",
                hole=.57,
                rotation=60,
                insidetextorientation="radial"
            )
        )
        
        fig.update_layout(
            template="simple_white",
            margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
            height=300,
            font=dict(family="serif", size=14),
            legend=dict(orientation="h", x=0, y=0, bgcolor="rgba(0,0,0,0)"),
        )
        
    else:
        fig = go.Figure(
            go.Bar(
                y=data[category], 
                x=data[col],
                orientation='h',
                marker=dict(color="navy"),
                text=data[col]
            )
        )
        fig.update_layout(
            height=300,
            template="simple_white",
            margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
            hovermode="x",
            font=dict(family="serif", color="black"),
            yaxis=dict(categoryorder='total ascending'),
            xaxis=dict(
                showgrid=True,
                showline=True,
            )
        )
        
    return fig



@callback(
    Output('mapbox', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
)
def mapbox(year, segment, mode, value):
    col, color = None, None
    
    data = filter_data(df, year, segment, mode)
    
    if value == "Sales":
        data = data.groupby("State", as_index=False)["Sales"].sum()
        col = "Sales"
        color = "reds"
        title_colorbar = "USD"
    else:
        data = data.groupby("State", as_index=False).size()
        col = "size"
        color = "rdylbu_r"
        title_colorbar = "Orders"
        
    data = add_iso2_to_dataframe(data, "State")
    
    fig = go.Figure(data=go.Choropleth(
        locations=data['code'],
        z=data[col],
        locationmode='USA-states',
        colorscale=color,
        autocolorscale=False,
        marker_line_color='white',
        colorbar_title=title_colorbar,
        customdata=data
    ))

    fig.update_layout(
        height=400,
        margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'
        ),
    )
    
    return fig



@callback(
    Output("fig-city", "figure"),  # 
    Output("title-city-rank", "children"),
    Input("mapbox", "hoverData"),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
)
def city_rank(hoverData, year, segment, mode, ship):
    data = filter_data(df, year, segment, mode)
    
    if hoverData:
        state = hoverData["points"][0]["customdata"][0]
        title = f"Top by city in the state of {state}"
    else:
        state = "California"
        title = "Top by city in the state of California"
        
    col=None
    if ship == "Sales":
        col = "Sales"
        color = "firebrick"
        data = data.groupby(["State", "City"], as_index=False)[col].sum()
    else:
        data = data.groupby(["State", "City"], as_index=False).size()
        col = "size"
        color = "royalblue"
  
    data = round(data[data["State"] == state], 2)
    
    if len(data) > 10:
        data = data.nlargest(columns=col, n=10)
  
    fig = go.Figure(
        go.Bar(
            x=data[col], 
            y=data["City"],
            orientation='h',
            marker=dict(color=color),
            text=data[col]
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        hovermode="x",
        font=dict(family="serif", color="black"),
      
        yaxis=dict(
            categoryorder='total ascending',
          
        )
      
    )
  
    return fig, [title]




@callback(
    Output('area-graph', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("area", 'value'),
    Input("ships", 'value'),
)
def update_area_graph(year, segment, mode, area, ship):
    data = filter_data(df, year, segment, mode)
    
    col = None
    if area == "Region": col="Region"
    elif area == "State": col="State"
    else: col="City"
            
    if ship == "Sales":
        col2 = "Sales"
        data = data.groupby(col, as_index=False)[col2].sum()
    else:
        data = data.groupby(col, as_index=False).size()
        col2 = "size"
        
    data = data.nlargest(columns=col2, n=10)
    data = round(data, 2)
        
    fig = go.Figure(
        go.Bar(
            x=data[col2], 
            y=data[col],
            orientation='h',
            marker=dict(color="green"),
            text=data[col2]
        )
    )
    fig.update_layout(
        height=300,
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        hovermode="x",
        font=dict(family="serif", color="black"),
        yaxis=dict(categoryorder='total ascending'),
        xaxis=dict(
            showgrid=True,
            showline=True,
        )
    )
    
    return fig



@callback(
    Output('global', 'children'),
    Input("years", 'value'),
)
def update_global_div(value):
    if value == "2015":
        value = int(value)
        data = df[df.Year == value] 
        sales = round(data.Sales.sum(), 2)
        ship = len(data)
        
        children = [
            html.Span("Year 2015"),
            html.Div(className="d-flex justify-content-between", children=[
                html.P(f"Sales: {sales}"),
                html.P(f"Sales: {ship}"),
            ]) 
        ]
        
        return children
        
    elif value in ["2016", "2017", "2018"]:
        value = int(value)
        data = df[df.Year == value] 
        sales = round(data.Sales.sum(), 2)
        ship = len(data)
        
        children = [
            html.H4(f"Year {value}"),
            html.Div(className="d-flex justify-content-between mt-2", children=[
                html.H5(f"Sales: {sales}"),
                html.H5(f"Orders: {ship}"),
            ]) ,
            
            html.Div(className="d-flex justify-content-between", children=[
                html.H5(f"Taux de change:10 soit une augmentation de 50% par rapport à {value-1}"),
                html.H5(f"Taux de change:10 soit une augmentation de 50% par rapport à {value-1}"),
            ]),
            
            html.Div(className="d-flex justify-content-between", children=[
                html.H5(f"Taux de change:10 soit une augmentation de 50% par rapport à {value-1}"),
                html.H5(f"Taux de change:10 soit une augmentation de 50% par rapport à {value-1}"),
            ]) 
        ]
        
        return children
    
    else:
        return []
    
    
  
@callback(
    Output('timeseries-by-day', 'figure'),
    Input("years", 'value'),
    Input("ships", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("graph", 'value'),
) 
def timeseries_by_days(year, ship, segment, mode, graph):    
    if year in ["2015", "2016", "2017", "2018"]:
        data = (df.copy())[df["Year"] == int(year)]
        year = int(year)
    else:
        data = df.copy()
        year = 2218
        
    data = data[data["Segment"] == segment] if segment in list(df.Segment.unique()) else data.copy()
    data = data[data["Mode"] == mode] if mode in list(df.Mode.unique()) else data.copy()
    
    if ship == "Sales":
        col = "sum"
        data = data.groupby("dayofyear")["Sales"].agg([("mean", "mean"), ("sum", "sum")]).reset_index()
    else:
        data = data.groupby("dayofyear", as_index=False).size()
        col = "size"

    
    data["date"] = data["dayofyear"].apply(
        lambda x: dt.datetime(year, 1, 1) + dt.timedelta(days=x - 1)
    )
    
    smoothed_values = lowess(
        data[col],
        data["dayofyear"],
        is_sorted=True,
        frac=1 / 12,
    )

    data["Sales_lowess"] = smoothed_values[:, 1]
    
    trace = {
        "type": graph,
        "x": data["date"],
        "y": data[col],
        "marker_color": "green",
        "name": "Raw data"
    }
    
    fig = go.Figure(data=[trace])
    
    fig.add_scatter(
        x=data["date"], y=data["Sales_lowess"],
        line=dict(color="firebrick", width=2),
        name="Lowess"
    )

    months_with_days = {
        month: (
            dt.datetime(year, month, 1),
            dt.datetime(
                year, month, 28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31
            ),
        )
        for month in range(1, 13)
    }

    # Loop over months and add a shape for each month
    for month, days in months_with_days.items():
        # Define background color
        bg_color = "lightgrey" if (month % 2) == 0 else "white"

        fig.add_shape(
            type="rect",
            yref="paper",
            x0=days[0],
            x1=days[1],
            y0=0,
            y1=1,
            fillcolor=bg_color,
            layer="below",
            line_width=0,
        )


    fig.update_layout(
        height=300,
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        hovermode="x",
        font=dict(family="serif", color="black"),
        xaxis={
            "dtick": "M1", 
            "hoverformat": "%e %B", 
            "showgrid": False,
            "tickformat": "%B", 
            "ticklabelmode": "period",  
        },
        yaxis={"showgrid": False, "ticksuffix": "$",},
        legend=dict(
            orientation="h", x=.013, y=.87
        ),
    )
    
    fig.update_xaxes(rangeslider_visible=True)

    
    return fig



@callback(
    Output('repartition', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
    Input("repartition-type", 'value'),
    Input("repartition-graph", 'value'),
)
def sales_by_category(year, segment, mode, ship, repartition, graph):
    data = filter_data(df, year, segment, mode)
    
    if ship == "Sales":
        col = "Sales"
        t1 = "Solde total"
        data = data.groupby([repartition], as_index=False)[col].sum()
    else:
        t1 = "Orders"
        data = data.groupby(repartition, as_index=False).size()
        col = "size"
        
    if graph == "pie":
        fig = go.Figure(
            go.Pie(
                labels=list(data[repartition]),
                values=list(data[col]),
                marker=dict(colors=colors),
                hoverinfo="label+value+percent",
                textinfo="label+value+percent",
                textposition="outside",
                hole=.57,
                rotation=50,
                insidetextorientation="radial",
                sort=True,
            )
        )
        
        fig.update_layout(
            template="simple_white",
            margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
            height=300,
            font=dict(family="serif", size=14),
            showlegend=False,
            
            annotations=[dict(
                text=t1 + "<br>" + " " + repartition,
                showarrow=False,
                font=dict(size=16)
            )]
        )
        
    
    else:
        fig = go.Figure(
            go.Bar(
                y=data[repartition], 
                x=data[col],
                orientation='h',
                marker=dict(color="green"),
                text=data[col]
            )
        )
        fig.update_layout(
            height=300,
            template="simple_white",
            margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
            hovermode="x",
            font=dict(family="serif", color="black"),
            yaxis=dict(categoryorder='total ascending'),
            xaxis=dict(
                showgrid=True,
                showline=True,
            )
        )
        
    return fig





@callback(
    Output('proportion', 'figure'),
    Input("years", 'value'),
    Input("ships", 'value'),
    Input("repartition-type", 'value'),
    Input("repartition-type2", 'value'),
)
def proportion_by_month(year, ship, repartition, time):
    data = (df.copy())[df["Year"] == int(year)] if year in ["2015", "2016", "2017", "2018"] else df.copy()
    
    if time == "Year":
        l = [2015, 2016, 2017, 2018]
    elif time == "Month": 
        l = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    else:
        l = list(df.Region.unique())
    
    if ship == "Sales":
        data = pd.crosstab(index=data[time], columns=data[repartition],values=data["Sales"], aggfunc='sum', normalize="index")
    else:
        data = pd.crosstab(index=data[time], columns=data[repartition],values=data["Sales"], aggfunc='sum', normalize="index")

    data = data * 100
    data = round(data, 2)

    top_labels = data.columns.tolist()
    
    colorsscale = colors + ["orangered"]

    x_data = data.values.tolist()
    y_data = l

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                name=xd[i],
                marker=dict(
                    color=colorsscale[i],
                    line=dict(color="whitesmoke", width=2)
                )
            ))

    fig.update_layout(
        height=300,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.1, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        autosize=True,
        template='simple_white',
        margin=dict(t=30, l=0, b=0, r=0),
        showlegend=False,
    )


    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.1, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='serif', size=15,
                                        color='black'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='serif', size=14,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='serif', size=15,
                                        color='black'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='serif', size=14,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='serif', size=15,
                                        color='black'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig




@callback(
    Output('pie-duration', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("solde", 'value'),
)
def sales_by_category(year, segment, aggregation):
    data = df[df["Duree"] >= pd.Timedelta(0)]
    
    if aggregation == "mean":
        text = "Mean sale"
    else:
        text = "Total sales"

    data = data[data["Year"] == int(year)] if year in ["2015", "2016", "2017", "2018"] else df.copy()
    data = data[data["Segment"] == segment] if segment in list(df.Segment.unique()) else data.copy()
    
    bins = [0, 3, 7, 30, float('inf')]
    labels = ['Less than 3 days', 'Between 3 and 7 days', 'Between 1 week and 1 month', 'More than 1 month']
    data['Duration group'] = pd.cut(
        data['Duration in days'], bins=bins, labels=labels)

    ventes_moyennes = data.groupby('Duration group')['Sales'].agg(aggregation).reset_index()
    
    fig = go.Figure(
            go.Pie(
                labels=list(ventes_moyennes["Duration group"]),
                values=list(ventes_moyennes["Sales"]),
                marker=dict(colors=colors),
                hoverinfo="label+value+percent",
                textinfo="label+value+percent",
                textposition="outside",
                hole=.57,
                rotation=50,
                insidetextorientation="radial",
                sort=True,
            )
        )
        
    fig.update_layout(
        template="simple_white",
        margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
        height=300,
        font=dict(family="serif", size=14),
        showlegend=False,
        
        annotations=[dict(
            text=f"{text} <br>en dollars",
            showarrow=False,
            font=dict(size=16)
        )]
    )
    
    return fig






@callback(
    Output('timeseries-duration', 'figure'),
    Input("years", 'value'), # 
    Input("segment", 'value'),
    Input("graph-duration", 'value'),
)
def sales_by_category(year, segment, graph):
    data = df[df["Duree"] >= pd.Timedelta(0)]

    data = data[data["Year"] == int(year)] if year in ["2015", "2016", "2017", "2018"] else data.copy()
    data = data[data["Segment"] == segment] if segment in list(df.Segment.unique()) else data.copy()
    
    monthly_sales = data.set_index('Order_date').resample('M')[
        'Duration in days'].mean()
    
    if graph == "bar":
        fig = go.Figure(
            go.Bar(
                x=monthly_sales.index,
                y=monthly_sales.values,
                marker=dict(color="firebrick"),
            )
        )
        
    else:
        fig = go.Figure(
            go.Scatter(
                x=monthly_sales.index,
                y=monthly_sales.values,
                mode="lines",
                line=dict(shape="spline", smoothing=1, color="firebrick"),
                fill="tozeroy"
            )
        )

    fig.update_layout(
        height=300,
            template="simple_white",
            margin=dict(autoexpand=True, r=0, t=0, b=0),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="serif"),
            xaxis={
                "dtick": "M1", 
                "hoverformat": "%b %Y", 
                "showgrid": False,
                "tickformat": "%b %Y", 
            },
    )
    
    return fig



@callback(
    Output('product', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'), 
    Input("season", 'value'),
) 
def top_by_product(year, segment, mode, ship, season):
    data = (df.copy())[df["Year"] == int(year)] if year in ["2015", "2016", "2017", "2018"] else df.copy()
    data = data[data["Segment"] == segment] if segment in list(df.Segment.unique()) else data.copy()
    data = data[data["Mode"] == mode] if mode in list(df.Mode.unique()) else data.copy()
    data = data[data["Season"] == season] if season in list(df.Season.unique()) else data.copy()
    
    if ship == "Sales":
        col = "Sales"
        data = (data.groupby(["Product Name"], as_index=False)[col].sum()).nlargest(columns=col, n=9)
    else:
        data = ((data["Product Name"].value_counts(normalize=False)).reset_index()).nlargest(columns="count", n=9)
        col = "count"
            
    fig = go.Figure(
        go.Bar(
            x=data[col], y=data["Product Name"],
            orientation="h", 
            text=data["Product Name"],
            textfont=dict(family="serif", size=11),
            marker=dict(color="firebrick"),
        )
    )
    
    fig.update_layout(
        height=280,
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        hovermode="x",
        font=dict(family="serif", color="black"),
        xaxis=dict(showgrid=True, showline=True),
        yaxis=dict(categoryorder='total ascending', showticklabels=False)
    )
    
    return fig




@callback(
    Output('client', 'figure'),
    Input("years", 'value'),
    Input("segment", 'value'),
    Input("mode", 'value'),
    Input("ships", 'value'),
) 
def top_by_clientt(year, segment, mode, ship):
    data = filter_data(df, year, segment, mode)
    
    if ship == "Sales":
        col = "Sales"
        data = (data.groupby(["Customer Name"], as_index=False)[col].sum()).nlargest(columns=col, n=9)
    else:
        data = ((data["Customer Name"].value_counts(normalize=False)).reset_index()).nlargest(columns="count", n=9)
        col = "count"
    
    
    
    fig = go.Figure(
        go.Bar(
            x=data[col], y=data["Customer Name"],
            orientation="h",
            marker=dict(color="green"),
        )
    )
    
    fig.update_layout(
        height=300,
        template="simple_white",
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        hovermode="y",
        font=dict(family="serif", color="black"),
        yaxis=dict(categoryorder='total ascending'),
        xaxis=dict(
            showgrid=True,
            showline=True,
        )
    )
    
    return fig
