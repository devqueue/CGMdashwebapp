from dash import Dash, Input, Output
from . import dataprocessor
from . import layouts
import pathlib
import dash_bootstrap_components as dbc


def create_rapidexome(server):
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], server=server,
                suppress_callback_exceptions=True, url_base_pathname='/dashboard/flashexome/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()
    df = dataprocessor.clean_df(DATA_PATH)


    app.layout = layouts.page_layout(
        'Rapid Exome/ Flash exome Status', 'rapid', 're', df)


    # Populate the options of counties dropdown based on states dropdown

    @app.callback(
        Output(component_id='stats-re', component_property='options'),
        [Input(component_id='month-dropdown-re', component_property='value'),
        Input(component_id='start-month-dropdown-re', component_property='value'),
        Input(component_id='end-month-dropdown-re', component_property='value')
        ]
    )
    def get_stat_list(month, start_month, end_month):
        df_Rapid = df.loc['Flash Exome']

        option_list = layouts.populate_options(
            df_Rapid, month, start_month, end_month)
        return option_list

    # populate the list of all options


    @app.callback(
        Output(component_id='stats-re', component_property='value'),
        [Input(component_id='stats-re', component_property='options'),
        ]
    )
    def select_values(available_options):
        return [x['value'] for x in available_options]


    # main function for graph
    @app.callback(
        Output(component_id='rapid-bar', component_property='figure'),
        [Input(component_id='month-dropdown-re', component_property='value'),
        Input(component_id='start-month-dropdown-re', component_property='value'),
        Input(component_id='end-month-dropdown-re', component_property='value'),
        Input(component_id='stats-re', component_property='value')
        ]
    )
    def display_value(month, start_month, end_month, stats):

        df_Rapid = df.loc['Flash Exome']

        fig = layouts.display_graph(
            df_Rapid, month, start_month, end_month, stats)

        return fig

    @app.callback(
        Output("rapid-pie-chart", "figure"),
        [Input(component_id='stats-re', component_property='value')
        ])
    def generate_chart(stats):
        df_Rapid = df.loc['Flash Exome'].loc['All Months'].loc[stats]

        fig = layouts.generate_pie(df_Rapid)
        return fig
    
    return app.server