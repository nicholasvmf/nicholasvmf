import yfinance as yf
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Input, Output
import plotly.express as px


# get the data
ticker = yf.Tickers('AAPL NVDA TSLA META HOLO MSFT')  # stock codes
data_stocks = ticker.history(period="1mo")  # history for the day
data_stocks.reset_index(inplace=True) # reset index for compatibility with dash
# print(data_stocks.columns)

# flatten multiIndex columns
data_stocks.columns = [''.join(col).strip() if isinstance(col, tuple) else col for col in data_stocks.columns]


# initialize the app
app = Dash()

# app layout
app.layout = html.Div([
    html.H1(children='Stock Price Lookup', style={'textAlign': 'center'}),
    html.Hr(),
    # Dropdown for selecting stock
    dcc.Dropdown(
        options=[
            {'label': 'Apple (AAPL)', 'value': 'CloseAAPL'},
            {'label': 'NVIDIA (NVDA)', 'value': 'CloseNVDA'},
            {'label': 'Tesla (TSLA)', 'value': 'CloseTSLA'},
            {'label': 'Meta (META)', 'value': 'CloseMETA'},
            {'label': 'MicroCloud (HOLO)', 'value': 'CloseHOLO'},
            {'label': 'Microsoft (MSFT)', 'value': 'CloseMSFT'}
        ],
        value='CloseAAPL',
        id='controls-and-dropdown'
    ),

    # DataTable
    dash_table.DataTable(
        data=data_stocks.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in data_stocks.columns],
        page_size=10
    ),

    # Graph
    dcc.Graph(
        figure=px.line(data_stocks, x='Date', y='CloseAAPL', title='AAPL Stock Prices'),
        id='controls-and-graph'
    )
])

@callback(
    Output('controls-and-graph', 'figure'),
    Input('controls-and-dropdown', 'value')
)
def update_graph(col_chosen):
    fig = px.line(data_stocks, x='Date', y=col_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)

'''MultiIndex([(       'Close', 'AAPL'),
            (       'Close', 'NVDA'),
            (       'Close', 'TSLA'),
            (   'Dividends', 'AAPL'),
            (   'Dividends', 'NVDA'),
            (   'Dividends', 'TSLA'),
            (        'High', 'AAPL'),
            (        'High', 'NVDA'),
            (        'High', 'TSLA'),
            (         'Low', 'AAPL'),
            (         'Low', 'NVDA'),
            (         'Low', 'TSLA'),
            (        'Open', 'AAPL'),
            (        'Open', 'NVDA'),
            (        'Open', 'TSLA'),
            ('Stock Splits', 'AAPL'),
            ('Stock Splits', 'NVDA'),
            ('Stock Splits', 'TSLA'),
            (      'Volume', 'AAPL'),
            (      'Volume', 'NVDA'),
            (      'Volume', 'TSLA')],
           names=['Price', 'Ticker'])'''
