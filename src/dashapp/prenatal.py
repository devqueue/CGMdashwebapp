from dash import Dash, Input, Output
from . import dataprocessor
from . import layouts
import pathlib
import dash_bootstrap_components as dbc



def create_prenatal(server):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server,
                suppress_callback_exceptions=True, url_base_pathname='/dashboard/prenatal/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

    # get path to data folder
    DATA_PATH = dataprocessor.get_data_path("DATA_PATH")
    df = dataprocessor.clean_df(DATA_PATH)

    app.layout = layouts.page_layout(
        'Prenatal Targeted Status', 'prenatal', 'p', df)
    # print(layout)

    # Populate the options of counties dropdown based on states dropdown

    @app.callback(
        Output(component_id='stats-p', component_property='options'),
        [Input(component_id='month-dropdown-p', component_property='value'),
        Input(component_id='start-month-dropdown-p', component_property='value'),
        Input(component_id='end-month-dropdown-p', component_property='value')
        ]
    )
    def get_stat_list(month, start_month, end_month):
        df_prenatal = df.loc['Prenatal Targeted']
        option_list = layouts.populate_options(
            df_prenatal, month, start_month, end_month)
        return option_list

    # # populate the list of all options


    @app.callback(
        Output(component_id='stats-p', component_property='value'),
        [Input(component_id='stats-p', component_property='options'),
        ]
    )
    def select_values(available_options):
        return [x['value'] for x in available_options]


    # main function for graph
    @app.callback(
        Output(component_id='prenatal-bar', component_property='figure'),
        [Input(component_id='month-dropdown-p', component_property='value'),
        Input(component_id='start-month-dropdown-p', component_property='value'),
        Input(component_id='end-month-dropdown-p', component_property='value'),
        Input(component_id='stats-p', component_property='value')
        ]
    )
    def display_value1(month, start_month, end_month, stats):

        df_prenatal = df.loc['Prenatal Targeted']
        
        fig = layouts.display_graph(df_prenatal, month, start_month, end_month, stats)
        return fig

    @app.callback(
        Output("prenatal-pie-chart", "figure"),
        [Input(component_id='stats-p', component_property='value')
        ])
    def generate_chart(stats):
        df_prenatal = df.loc['Prenatal Targeted'].loc['All Months'].loc[stats]

        fig = layouts.generate_pie(df_prenatal)
        return fig
    
    return app.server