from dash import Dash, Input, Output
from . import dataprocessor
from . import layouts
import pathlib
import dash_bootstrap_components as dbc


def create_oncomine(server):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server,
                suppress_callback_exceptions=True, url_base_pathname='/dashboard/oncomine/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()
    df = dataprocessor.clean_df(DATA_PATH)


    app.layout = layouts.page_layout('Oncomine Comprehensive Status', 'oncomine', 'oc', df)


    # Populate the options of counties dropdown based on states dropdown
    @app.callback(
        Output(component_id='stats-oc', component_property='options'),
        [Input(component_id='month-dropdown-oc', component_property='value'),
        Input(component_id='start-month-dropdown-oc', component_property='value'),
        Input(component_id='end-month-dropdown-oc', component_property='value')
        ]
    )
    def get_stat_list(month, start_month, end_month):
        df_oncomine = df.loc['Oncomine Comprehensive']
        option_list = layouts.populate_options(df_oncomine, month, start_month, end_month)
        return option_list

    # populate the list of all options
    @app.callback(
        Output(component_id='stats-oc', component_property='value'),
        [Input(component_id='stats-oc', component_property='options'),
        ]
    )
    def select_values(available_options):
        return [x['value'] for x in available_options]



    @app.callback(
        Output(component_id='oncomine-bar', component_property='figure'),
        [Input(component_id='month-dropdown-oc', component_property='value'),
        Input(component_id='start-month-dropdown-oc', component_property='value'),
        Input(component_id='end-month-dropdown-oc', component_property='value'),
        Input(component_id='stats-oc', component_property='value')
        ]
    )
    def display_value(month, start_month, end_month, stats):
        df_oncomine = df.loc['Oncomine Comprehensive']

        fig = layouts.display_graph(df_oncomine, month, start_month, end_month, stats)

        return fig

    @app.callback(
        Output("oncomine-pie-chart", "figure"),
        [Input(component_id='stats-oc', component_property='value')
        ])
    def generate_chart(stats):
        df_oncomine = df.loc['Oncomine Comprehensive'].loc['All Months'].loc[stats]

        fig = layouts.generate_pie(df_oncomine)
        return fig
    
    return app.server
