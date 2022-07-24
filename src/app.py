from datetime import date
import dataretrieval.nwis as nwis
import utils.param_codes as pc
from dash import dash, html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd
from utils import download

app = dash.Dash()

app.layout = html.Div(
    id="parent",
    children=[
        html.H1(
            id="H1",
            children="The QCinator, it's coming for your data!",
            style={"textAlign": "center", "marginTop": 40, "marginBottom": 40},
        ),
        html.Div(
            [
                "Station ID: ",
                dcc.Input(
                    id="station_ID",
                    value="12323840",
                    debounce=True,
                    inputMode="numeric",
                    autoFocus=True,
                    minLength=8,
                    placeholder="enter station",
                    type="text",
                ),
            ]
        ),
        dcc.DatePickerRange(
            id="date_range",
            start_date=date(2020, 3, 1),
            end_date=date(2020, 11, 1),
            min_date_allowed=date(2018, 1, 1),
            initial_visible_month=date(2020, 1, 1),
        ),
        html.Div(
            [
                "Select parameter by name: ",
                dcc.Dropdown(
                    id="param_select",
                    options=pc.param_labels,
                    value="p00400",
                ),
            ]
        ),
        dcc.Graph(id="scatter_plot"),
        html.Div(
            [
                "Select X axis parameter: ",
                dcc.Dropdown(
                    id="param_select_X",
                    options=pc.param_labels,
                    value="p00400",
                ),
            ]
        ),
        html.Div(
            [
                "Select Y axis parameter: ",
                dcc.Dropdown(
                    id="param_select_Y",
                    options=pc.param_labels,
                    value="p00400",
                ),
            ]
        ),
        dcc.Graph(id="plot_X_vs_Y", style={"display": "inline-block"}),
        dcc.Store(id="memory_data", storage_type="memory"),
    ],
)


@app.callback(
    Output("memory_data", "data"),
    [
        Input("station_ID", "value"),
        Input("date_range", "start_date"),
        Input("date_range", "end_date"),
    ],
)
def get_qw_data(site, start, end):
    df = nwis.get_record(sites=site, service="qwdata", start=start, end=end, access="3")
    return df.to_json()


@app.callback(
    Output("scatter_plot", "figure"),
    [
        Input("param_select", "value"),
        Input("memory_data", "data"),
    ],
)
def plot_parameter(param, data):
    df = pd.read_json(data)
    fig = go.Figure(
        [
            go.Scatter(
                mode="markers",
                x=df.index,
                y=df[param],
                name="pH",
            ),
        ],
    )
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title=pc.parameters.get(param),
    )
    return fig


@app.callback(
    Output("plot_X_vs_Y", "figure"),
    [
        Input("param_select_X", "value"),
        Input("param_select_Y", "value"),
        Input("memory_data", "data"),
    ],
)
def x_vs_y(param_x, param_y, data):
    df = pd.read_json(data)
    fig = go.Figure(
        [
            go.Scatter(
                mode="markers",
                x=df[param_x],
                y=df[param_y],
                name="pH",
            ),
        ],
    )
    fig.update_layout(
        title="",
        xaxis_title=pc.parameters.get(param_x),
        yaxis_title=pc.parameters.get(param_y),
    )
    fig.update_xaxes(
        constrain="domain",
    )
    if param_x == param_x:
        fig.update_xaxes(
            constrain="domain",
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
