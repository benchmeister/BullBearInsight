import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.backtesting.plot_candlestick import plot_candlestick
from src.components.stock.backtesting.plot_volume import plot_volume
from src.components.stock.backtesting.plot_profit_loss import plot_profit_loss
from src.components.stock.stock_layout_functions import get_stock_id_from_url
from src.components.stock.backtesting.sma_crossover import backtestSmaCrossover
from src.components.stock.single_stock_base_layout import stock_base_layout
from src.components.stock.backtesting.plot_equity import plot_equity
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


dash.register_page(__name__, path_template="/stocks/<stock_id>/backtesting")



@callback([Output("equity-figure","figure"), Output("profit-loss-figure","figure"),Output("candlestick-figure","figure"), Output("volume-figure","figure"),Output("subplot-figure","figure")], [Input("run-backtest", "n_clicks"), Input("url","pathname")])
def runSMA(n_clicks, url):

   fig = make_subplots(
         rows=4, cols=1,
         shared_xaxes=True,
         subplot_titles=("Equity Curve", "Profit/Loss", "Candlestick Chart", "Volume Chart"),
         vertical_spacing=0.1
      )

   if (n_clicks == 0 ):
      stock_id = get_stock_id_from_url(url)
      buy_amount = 10
      stats = backtestSmaCrossover(stock_id, averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=buy_amount)
      equity_curve = stats['Equity Curve']
      trades = stats["Trades"]
      candlestick = stats["Candlestick"]
      equity_curve = equity_curve.reset_index()
      # Merge the trades with the full dataset to expand the rows
      merged_data = pd.merge(equity_curve, trades, left_on='Date', right_on='EntryTime', how='left')
      # Keep only the relevant trade columns after merging (and the Date column)
      trade_columns = ['Date', 'EntryPrice', 'ExitPrice', 'PnL', 'ReturnPct', "ExitTime", "EntryTime"]
      filtered_trade = merged_data[trade_columns]
      
      # Plot equity curve using Plotly
      equity_fig = plot_equity(equity_curve=equity_curve)
      pl_fig = plot_profit_loss(trades=filtered_trade)
      candlestick_fig = plot_candlestick(candlestick, filtered_trade)
      volume_fig = plot_volume(candlestick_data=candlestick)
      return equity_fig, pl_fig,candlestick_fig, volume_fig, fig
   else:
      fig = go.Figure()
      fig.update_layout(
         title='Equity Curve',
         xaxis_title='Time',
         yaxis_title='Equity Value',
         legend=dict(x=0.02, y=0.98),
         plot_bgcolor='#F1F1F1',
         paper_bgcolor='#F1F1F1',
      )
      return fig, fig


def layout(stock_id=None, **kwargs):
    return(
      stock_base_layout(stock_id),
      html.Button("Run Backtest", id="run-backtest", n_clicks=0),
      dcc.Graph(id = "subplot-figure"),
      dcc.Graph(id ="equity-figure"),
      dcc.Graph(id = "profit-loss-figure"),
      dcc.Graph(id= "candlestick-figure"),
      dcc.Graph(id = "volume-figure")
 
      #  backtestSmaCrossover('AAPL', averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
    )