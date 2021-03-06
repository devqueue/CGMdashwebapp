from dash import Dash, Input, Output
from . import dataprocessor
from . import layouts
import pathlib
import dash_bootstrap_components as dbc



def create_familial(server):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server,
                suppress_callback_exceptions=True, url_base_pathname='/dashboard/familial/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


    # get path to data folder
    DATA_PATH = dataprocessor.get_data_path("DATA_PATH")
    df = dataprocessor.clean_df(DATA_PATH)

    app.layout = layouts.page_layout(
        'Familial Segregation Status', 'familial', 'f', df)


    # Populate the options of counties dropdown based on states dropdown

    @app.callback(
        Output(component_id='stats-f', component_property='options'),
        [Input(component_id='month-dropdown-f', component_property='value'),
        Input(component_id='start-month-dropdown-f', component_property='value'),
        Input(component_id='end-month-dropdown-f', component_property='value')
        ]
    )
    def get_stat_list(month, start_month, end_month):
        df_familial = df.loc['Familial Segregation']

        option_list = layouts.populate_options(df_familial, month, start_month, end_month)
        return option_list

    # populate the list of all options


    @app.callback(
        Output(component_id='stats-f', component_property='value'),
        [Input(component_id='stats-f', component_property='options'),
        ]
    )
    def select_values(available_options):
        return [x['value'] for x in available_options]


    # main function for graph
    @app.callback(
        Output(component_id='familial-bar', component_property='figure'),
        [Input(component_id='month-dropdown-f', component_property='value'),
        Input(component_id='start-month-dropdown-f', component_property='value'),
        Input(component_id='end-month-dropdown-f', component_property='value'),
        Input(component_id='stats-f', component_property='value')
        ]
    )
    def display_value(month, start_month, end_month, stats):

        df_familial = df.loc['Familial Segregation']

        fig = layouts.display_graph(
            df_familial, month, start_month, end_month, stats)

        return fig

    @app.callback(
        Output("familial-pie-chart", "figure"),
        [Input(component_id='stats-f', component_property='value')
        ])
    def generate_chart(stats):
        df_exome = df.loc['Familial Segregation'].loc['All Months'].loc[stats]

        fig = layouts.generate_pie(df_exome)
        return fig

    return app.server