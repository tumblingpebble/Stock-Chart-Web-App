import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stock Chart Application"),
    html.Label("Ticker Symbol:"),
    dcc.Input(id="ticker-input", value="AAPL", type="text"),
    dcc.Graph(id="stock-chart"),
    html.Div([
        html.Button("1D", id="1d-button", n_clicks=0),
        html.Button("5D", id="5d-button", n_clicks=0),
        html.Button("1M", id="1m-button", n_clicks=0),
        html.Button("3M", id="3m-button", n_clicks=0)
    ])
])

@app.callback(
    Output("stock-chart", "figure"),
    [Input("ticker-input", "value"),
     Input("1d-button", "n_clicks"),
     Input("5d-button", "n_clicks"),
     Input("1m-button", "n_clicks"),
     Input("3m-button", "n_clicks")]
)
def update_chart(ticker, n1d, n5d, n1m, n3m):
    ctx = dash.callback_context

    if not ctx.triggered:
        return go.Figure()

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == '1d-button':
        range_period = '1d'
    elif button_id == '5d-button':
        range_period = '5d'
    elif button_id == '1m-button':
        range_period = '1mo'
    elif button_id == '3m-button':
        range_period = '3mo'
    else:
        range_period = '1d'

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={range_period}&interval=1d"
        response = requests.get(url)
        data = response.json()

        if 'chart' in data and 'result' in data['chart']:
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            ohlc = result['indicators']['quote'][0]

            fig = go.Figure(data=[go.Candlestick(
                x=[pd.to_datetime(ts, unit='s') for ts in timestamps],
                open=ohlc['open'],
                high=ohlc['high'],
                low=ohlc['low'],
                close=ohlc['close']
            )])
            return fig
        else:
            return go.Figure()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return go.Figure()

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
