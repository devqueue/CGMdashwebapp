from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from . import dataprocessor

def sidebar():
    # styling the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "17rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # padding for the page content
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }


    sidebar = html.Div(
        [
            html.H2("CGM Statistics Dashboard", className="display-7"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Oncomine Comprehensive",href="/apps/oncomine", active="exact"),
                    dbc.NavLink("Prenatal Targeted", href="/apps/prenatal", active="exact"),
                    dbc.NavLink("Familial Segregation", href="/apps/familial", active="exact"),
                    dbc.NavLink("Targeted Mutation", href="/apps/targeted", active="exact"),
                    dbc.NavLink("Exome Sequencing", href="/apps/exome", active="exact"),
                    dbc.NavLink("Flash Exome Sequencing", href="/apps/rapidexome", active="exact"),
                    dbc.NavLink("Uploaded Data", href="/", active="exact")
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

    layout = html.Div([
        dcc.Location(id="url"),
        sidebar,
        content
    ])

    return layout


def page_layout(title, metric, id_suffix, df):

    layout = html.Div([
        html.Br(),
        html.H1(title, style={"textAlign": "center"}),
        html.Br(),
        html.Br(),
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id=f"{metric}-pie-chart"),
            ],className="d-flex justify-content-center"),

            html.Div(children=[
                dcc.Graph(id=f'{metric}-bar', figure={}),
            ],className="d-flex justify-content-center")

            ]),

        html.Div([
            html.Div([
                html.Pre(children="Month", style={"fontSize": "100%"}),
                dcc.Dropdown(
                    id=f'month-dropdown-{id_suffix}', value='All Months', clearable=False,
                    persistence=True, persistence_type='session',
                    options=[{'label': x, 'value': x} for x in df.columns] +
                    [{'label': 'Between', 'value': 'between'}]

                )
            ], className='col s12 m6', style={"margin-left": "15px", "margin-right": "15px"}),

            html.Br(),
            html.Br(),

            html.Div(children=[
                        html.Div([
                            html.Pre(children="\nStart Month",
                                    style={"fontSize": "100%"}),
                            dcc.Dropdown(
                                id=f'start-month-dropdown-{id_suffix}', clearable=False,
                                persistence=True, persistence_type='session',
                                options=[{'label': x, 'value': x}
                                        for x in df.columns]
                            )
                        ], className='col s12 m6', style={"margin-left": "15px"}),

                        html.Div([
                            html.Pre(children="\nEnd month",
                                    style={"fontSize": "100%"}),
                            dcc.Dropdown(
                                id=f'end-month-dropdown-{id_suffix}', clearable=False,
                                persistence=True, persistence_type='session',
                                options=[{'label': x, 'value': x}
                                        for x in df.columns]
                            )
                        ], className='col s12 m6', style={"margin-left": "15px"}),

            ], className='row', style={'display': 'flex'}),

            html.Div(children=[
                        html.Pre(children="\nStatistics",
                                 style={"fontSize": "100%"}),
                        dcc.Dropdown(id=f'stats-{id_suffix}',
                                    options=[],
                                    multi=True,
                                    searchable=True,  # allow user-searching of dropdown values
                                    search_value='',  # remembers the value searched in dropdown
                                    placeholder='Select...', # gray, default text shown when no option is selected
                                    clearable=True,
                        )
                        
            ], className='col s12 m6', style={"margin-left": "15px", "margin-right": "15px"})

        ], className='row'),

        
        html.Br(),
        html.Br(),
    ],style={"height": "100vh","overflow-y": "scroll","margin-bottom": "50px"})

    return layout



def populate_options(df_metric, month, start_month, end_month):

    if month == 'between':
        filtered = df_metric.loc[start_month:end_month]
        df_filtered = dataprocessor.combine_between(filtered)
        return [{'label': x, 'value': x} for x in list(df_filtered.index)]
    else:
        mask = month
        df_filtered = df_metric.loc[mask]
        return [{'label': x, 'value': x} for x in list(df_filtered.index)]


def generate_pie(df_metric):
    fig = go.Figure(data=[go.Pie(labels=df_metric["Total"].index,
                                values=df_metric["Total"].values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value',
                    marker=dict(line=dict(color='#000000', width=1)),
                    )
    fig.update_layout(title = {'text': "Total", 'y': 0.95,
                            'x': 0.5, 'xanchor': 'center',
                            'yanchor': 'top'}, 
                            autosize=False,
                        width=500,
                        height=600,
                        )
                
    return fig


def display_graph(df_metric, month, start_month, end_month, stats):

    if month == 'between':
        filtered = df_metric.loc[start_month:end_month]
        title = f'Between {start_month} and {end_month}'
        df_filtered = dataprocessor.combine_between(filtered)
        df_filtered = df_filtered.loc[stats]
        cols, total = df_filtered.columns.tolist()[1:], df_filtered.columns.tolist()[0]
        cols_re = dataprocessor.rearranage_columns(cols) + [total]
        df_filtered = df_filtered[cols_re]
        df_filtered = df_filtered.transpose()
        fig = go.Figure(data=[go.Bar(name=colname, x=df_filtered.index, y=df_filtered[colname],
                                     text=df_filtered[colname]) for colname in df_filtered.columns])

    elif month == "All Months":
        title = month
        mask = month
        df_filtered = df_metric.loc[mask]
        df_filtered = df_filtered.loc[stats]
        cols, total = df_filtered.columns.tolist()[1:], df_filtered.columns.tolist()[0]
        cols_re = dataprocessor.rearranage_columns(cols) + [total]
        df_filtered = df_filtered[cols_re]
        df_filtered = df_filtered.transpose()

        fig = go.Figure(data=[go.Bar(name=colname, x=df_filtered.index, y=df_filtered[colname], text=df_filtered[colname]) 
                              for colname in df_filtered.columns],

                        )


    else:
        title = month
        mask = month
        df_filtered = df_metric.loc[mask]
        df_filtered = df_filtered.loc[stats]
        
        fig = px.bar(df_filtered, x=df_filtered.index,
                    y=df_filtered.iloc[:, 0],
                    text=df_filtered.iloc[:, 0],
                    color=df_filtered.index,
                    labels={'x': 'Status', 'y': 'Count'})

    fig.update_layout(title = {'text': title, 'y': 0.95,
                            'x': 0.5, 'xanchor': 'center',
                            'yanchor': 'top'}, 
                            autosize=False,
                            # margin=dict(l=20, r=20, t=20, b=20),
                        width=1000,
                        height=600,
                        )

    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return fig