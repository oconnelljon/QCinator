from datetime import date
import dataretrieval.nwis as nwis
import utils.param_codes as pc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

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
                "station_ID: ",
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
        dcc.Dropdown(
            id="param_select",
            options=pc.param_labels,
            value="p00400",
        ),
        dcc.Graph(id="scatter_plot"),
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
    df = nwis.get_record(sites=site, service="qwdata", start=start, end=end)
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
                x=df.index,
                y=df[param],
                line=dict(color="firebrick", width=4),
                name="pH",
            ),
        ],
    )
    fig.update_layout(title="", xaxis_title="Date", yaxis_title=pc.parameters.get(param))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
